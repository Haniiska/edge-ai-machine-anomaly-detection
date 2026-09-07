#include "hal_data.h"
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

#define SAMPLE_WINDOW_SIZE  32
#define ADC_VREF_MV         3300.0f
#define ADC_MAX_COUNT       4095.0f

typedef enum {
    ANOMALY_NONE = 0,
    ANOMALY_OVERCURRENT
} anomaly_type_t;

/* Global Diagnostics for Direct SWD / UART Telemetry */
volatile anomaly_type_t g_anomaly_status = ANOMALY_NONE;
volatile float          g_live_rms       = 0.0f;
volatile float          g_anomaly_score  = 0.0f;
volatile uint32_t       g_anomaly_count  = 0;
volatile float          g_live_temp      = 29.4f;
volatile bool           g_uart_tx_done   = false;

static float g_base_mean   = 0.0f;
static float g_base_std    = 25.0f;
static bool  g_initialized = false;

/* Hardware UART Callback */
void user_uart_callback(uart_callback_args_t * p_args)
{
    if (UART_EVENT_TX_COMPLETE == p_args->event)
    {
        g_uart_tx_done = true;
    }
}

void hal_entry(void)
{
    R_BSP_PinAccessEnable();

    /* 1. Open ADC0 Channel 0 (Pin 6 / P000) */
    R_ADC_Open(&g_adc0_ctrl, &g_adc0_cfg);
    R_ADC_ScanCfg(&g_adc0_ctrl, &g_adc0_channel_cfg);

    /* 2. Configure Optical IR Sensor Digital Pin (Pin 7 / P001) as Active-Low Input */
    R_IOPORT_PinCfg(&g_ioport_ctrl, BSP_IO_PORT_00_PIN_01,
                    (IOPORT_CFG_PORT_DIRECTION_INPUT | IOPORT_CFG_PULLUP_ENABLE));

    /* 3. Open SCI9 UART Telemetry Channel @ 115200 Baud */
    R_SCI_UART_Open(&g_uart9_ctrl, &g_uart9_cfg);

    char tx_buf[128];

    while (1)
    {
        float sum_sq = 0.0f;

        /* 32-Sample High-Speed ADC Acquisition Window */
        for (int i = 0; i < SAMPLE_WINDOW_SIZE; i++)
        {
            R_ADC_ScanStart(&g_adc0_ctrl);
            adc_status_t status;
            do {
                R_ADC_StatusGet(&g_adc0_ctrl, &status);
            } while (status.state == ADC_STATE_SCAN_IN_PROGRESS);

            uint16_t raw_counts = 0;
            R_ADC_Read(&g_adc0_ctrl, ADC_CHANNEL_0, &raw_counts);

            float sample_mv = ((float)raw_counts * ADC_VREF_MV) / ADC_MAX_COUNT;
            sum_sq += (sample_mv * sample_mv);

            R_BSP_SoftwareDelay(100, BSP_DELAY_UNITS_MICROSECONDS);
        }

        /* 4. Discrete True RMS Computation (Single-Cycle FPU Math) */
        float calculated_rms = sqrtf(sum_sq / (float)SAMPLE_WINDOW_SIZE);
        g_live_rms = calculated_rms;

        /* 5. Adaptive Baseline Initialization & Exponential Moving Average */
        if (!g_initialized)
        {
            g_base_mean   = calculated_rms;
            g_initialized = true;
        }
        else
        {
            g_base_mean = (0.95f * g_base_mean) + (0.05f * calculated_rms);
        }

        /* 6. Gaussian Statistical Z-Score Divergence */
        float delta = fabsf(calculated_rms - g_base_mean);
        float z_score = delta / g_base_std;
        g_anomaly_score = z_score;

        /* 7. Active-Low Optical IR Obstacle Sensor Read */
        bsp_io_level_t ir_pin_level = BSP_IO_LEVEL_HIGH;
        R_IOPORT_PinRead(&g_ioport_ctrl, BSP_IO_PORT_00_PIN_01, &ir_pin_level);

        /* 8. Fault Classification Logic */
        if ((z_score >= 2.0f) || (ir_pin_level == BSP_IO_LEVEL_LOW))
        {
            g_anomaly_status = ANOMALY_OVERCURRENT;
            g_anomaly_count++;
        }
        else
        {
            g_anomaly_status = ANOMALY_NONE;
        }

        /* 9. Telemetry Transmission via UART */
        snprintf(tx_buf, sizeof(tx_buf),
                 "RMS:%.2f,MEAN:%.2f,Z:%.2f,TEMP:%.1f,STATE:%d\r\n",
                 g_live_rms, g_base_mean, g_anomaly_score, g_live_temp, (int)g_anomaly_status);

        g_uart_tx_done = false;
        R_SCI_UART_Write(&g_uart9_ctrl, (uint8_t *)tx_buf, strlen(tx_buf));

        /* 50 Hz Loop Delay (20 ms Period) */
        R_BSP_SoftwareDelay(20, BSP_DELAY_UNITS_MILLISECONDS);
    }
}
