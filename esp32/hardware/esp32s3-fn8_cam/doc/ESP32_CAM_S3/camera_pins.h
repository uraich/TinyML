#if defined(ESP32_CAM_S3)
#define PWDN_GPIO_NUM    -1
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM    10
#define SIOD_GPIO_NUM    21
#define SIOC_GPIO_NUM    14

#define Y9_GPIO_NUM      11
#define Y8_GPIO_NUM      9
#define Y7_GPIO_NUM      8
#define Y6_GPIO_NUM      6
#define Y5_GPIO_NUM      4
#define Y4_GPIO_NUM      2
#define Y3_GPIO_NUM      3
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM   13
#define HREF_GPIO_NUM    12
#define PCLK_GPIO_NUM    7

#define LED_GPIO_NUM     34

#else
#error "Camera model not selected"
#endif
