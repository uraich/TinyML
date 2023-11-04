#!/bin/bash
rm -rfv work
mkdir work
cd work

# get newest version of tflite-micro

# get the examples
echo Cloning the examples
git clone --depth 1 --single-branch "https://github.com/espressif/esp-tflite-micro.git"
# del
find ./ -name 'test' | xargs rm -rfv

# rename
rename -v 's/\.cc/\.cpp/' *.cc
rename -v 's/\.cc/\.cpp/' */*.cc
rename -v 's/\.cc/\.cpp/' */*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*/*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*/*/*/*.cc
# rename -v 's/\.cc/\.cpp/' */*/*/*/*/*/*/*.cc
# rename -v 's/\.cc/\.cpp/' */*/*/*/*/*/*/*/*.cc
# rename -v 's/\.cc/\.cpp/' */*/*/*/*/*/*/*/*/*.cc
# rename -v 's/\.cc/\.cpp/' */*/*/*/*/*/*/*/*/*/*.cc

# flatbuffers
mv esp-tflite-micro/third_party/flatbuffers/include/flatbuffers/* esp-tflite-micro/third_party/flatbuffers
rm -rfv esp-tflite-micro/third_party/flatbuffers/include

# sed
echo "flatbuffers"
find ./ -name '*.h' -type f | xargs sed -i 's/\"flatbuffers/\"third_party\/flatbuffers/g'
find ./ -name '*.cpp' -type f | xargs sed -i 's/\"flatbuffers/\"third_party\/flatbuffers/g'

echo "utility"
find ./ -name '*.h' -type f | xargs sed -i 's/utility\.h/utility/g'

echo "kiss_fft"
find ./ -name '*.h' -type f | xargs sed -i 's/\"kiss_fft/\"third_party\/kissfft\/kiss_fft/g'
find ./ -name '*.cpp' -type f | xargs sed -i 's/\"kiss_fft/\"third_party\/kissfft\/kiss_fft/g'

find ./ -name '*.h' -type f | xargs sed -i 's/\"kiss_fft/\"third_party\/kissfft\/kiss_fft/g'
find ./ -name '*.cpp' -type f | xargs sed -i 's/\"kiss_fft/\"third_party\/kissfft\/kiss_fft/g'

find ./ -name '*.h' -type f | xargs sed -i 's/\"tools\/kiss_fftr\.h\"/\"third_party\/kissfft\/tools\/kiss_fftr\.h\"/g'
find ./ -name '*.cpp' -type f | xargs sed -i 's/\"tools\/kiss_fftr\.h\"/\"third_party\/kissfft\/tools\/kiss_fftr\.h\"/g'

find ./ -name '*.h' -type f | xargs sed -i 's/\"tools\/kiss_fftr\.c\"/\"third_party\/kissfft\/tools\/kiss_fftr\.c\"/g'
find ./ -name '*.cpp' -type f | xargs sed -i 's/\"tools\/kiss_fftr\.c\"/\"third_party\/kissfft\/tools\/kiss_fftr\.c\"/g'

find ./ -name '*.c' -type f | xargs sed -i 's/\"_kiss_fft_guts\.h\"/\"third_party\/kissfft\/_kiss_fft_guts\.h\"/g'

echo "fixedpoint"
find ./ -name '*.h' -type f | xargs sed -i 's/\"fixedpoint/\"third_party\/gemmlowp\/fixedpoint/g'
find ./ -name '*.cpp' -type f | xargs sed -i 's/\"fixedpoint/\"third_party\/gemmlowp\/fixedpoint/g'

echo "ruy"
find ./ -name '*.h' -type f | xargs sed -i 's/\"ruy/\"third_party\/ruy\/ruy/g'

# src
rm -rf ../src/tensorflow
rm -rf ../src/third_party
rm -rf ../src/signal
cp -r esp-tflite-micro/tensorflow ../src/
cp -r esp-tflite-micro/third_party ../src/
cp -r esp-tflite-micro/signal ../src/

# examples/hello_world
mv esp-tflite-micro/examples/hello_world/main/* esp-tflite-micro/examples/hello_world
rm -rfv esp-tflite-micro/examples/hello_world/main
rm -rfv esp-tflite-micro/examples/hello_world/main.cpp
rm -rfv esp-tflite-micro/examples/hello_world/*.txt
rm -rfv esp-tflite-micro/examples/hello_world/sdkconfig.defaults
mv esp-tflite-micro/examples/hello_world/main_functions.cpp esp-tflite-micro/examples/hello_world/hello_world.ino
echo "" >esp-tflite-micro/examples/hello_world/main_functions.h
sed -i -e "1i #include <TFLM_ESP32.h>" esp-tflite-micro/examples/hello_world/hello_world.ino

# examples/micro_speech
mv esp-tflite-micro/examples/micro_speech/main/* esp-tflite-micro/examples/micro_speech
rm -rfv esp-tflite-micro/examples/micro_speech/main
rm -rfv esp-tflite-micro/examples/micro_speech/main.cpp
rm -rfv esp-tflite-micro/examples/micro_speech/*.txt
rm -rfv esp-tflite-micro/examples/micro_speech/sdkconfig.defaults
mv esp-tflite-micro/examples/micro_speech/main_functions.cpp esp-tflite-micro/examples/micro_speech/micro_speech.ino
echo "" >esp-tflite-micro/examples/micro_speech/main_functions.h
sed -i -e "1i #include <TFLM_ESP32.h>" esp-tflite-micro/examples/micro_speech/micro_speech.ino

# examples/person_detection
mv esp-tflite-micro/examples/person_detection/main/* esp-tflite-micro/examples/person_detection
rm -rfv esp-tflite-micro/examples/person_detection/main
rm -rfv esp-tflite-micro/examples/person_detection/main.cpp
rm -rfv esp-tflite-micro/examples/person_detection/*.txt
rm -rfv esp-tflite-micro/examples/person_detection/sdkconfig.defaults
rm -rfv esp-tflite-micro/examples/person_detection/sdkconfig.defaults.*
rm -rfv esp-tflite-micro/examples/person_detection/Kconfig.projbuild
rm -rfv esp-tflite-micro/examples/person_detection/*.csv
mv esp-tflite-micro/examples/person_detection/main_functions.cpp esp-tflite-micro/examples/person_detection/person_detection.ino
echo "" >esp-tflite-micro/examples/person_detection/main_functions.h
sed -i -e "1i #include <TFLM_ESP32.h>" esp-tflite-micro/examples/person_detection/person_detection.ino

sed -i -e "15i // choice CAMERA_MODULE" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "16i #define CONFIG_CAMERA_MODULE_WROVER_KIT true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "17i //#define CONFIG_CAMERA_MODULE_ESP_EYE true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "18i //#define CONFIG_CAMERA_MODULE_ESP_S2_KALUGA true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "19i //#define CONFIG_CAMERA_MODULE_ESP_S3_EYE true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "20i //#define CONFIG_CAMERA_MODULE_ESP32_CAM_BOARD true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "21i //#define CONFIG_CAMERA_MODULE_M5STACK_PSRAM true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "22i //#define CONFIG_CAMERA_MODULE_M5STACK_WIDE true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "23i //#define CONFIG_CAMERA_MODULE_AI_THINKER true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e "24i //#define CONFIG_CAMERA_MODULE_CUSTOM true" esp-tflite-micro/examples/person_detection/esp_main.h
sed -i -e '25i \\' esp-tflite-micro/examples/person_detection/esp_main.h

# examples
rm -rfv ../examples/hello_world
rm -rfv ../examples/micro_speech
rm -rfv ../examples/person_detection

cp -r esp-tflite-micro/examples/hello_world ../examples/
cp -r esp-tflite-micro/examples/micro_speech ../examples/
cp -r esp-tflite-micro/examples/person_detection ../examples/

