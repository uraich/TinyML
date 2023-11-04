#!/usr/bin/env bash
# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
# Creates the project file distributions for the TensorFlow Lite Micro test and
# example targets aimed at embedded platforms.

set -e -x

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
TFLITE_LIB_DIR="${ROOT_DIR}"

TEMP_DIR=$(mktemp -d)
cd "${TEMP_DIR}"

echo Cloning tflite-micro repo to "${TEMP_DIR}"
git clone --depth 1 --single-branch "https://github.com/tensorflow/tflite-micro.git"

echo Cloning the examples
git clone --depth 1 --single-branch "https://github.com/espressif/esp-tflite-micro.git"

# Create the TFLM base tree
echo Creating TFLM base tree
cd "${TEMP_DIR}"/tflite-micro
python3 tensorflow/lite/micro/tools/project_generation/create_tflm_tree.py \
	-e hello_world -e micro_speech -e person_detection "${TEMP_DIR}/tflm-out"

# Backup `micro/kernels/esp_nn` directory to new tree
/bin/cp -r "${TFLITE_LIB_DIR}"/src/tensorflow/lite/micro/kernels/esp_nn \
	"${TEMP_DIR}"/tflm-out/tensorflow/lite/micro/kernels/

cd ..

# flatbuffers
mv tflm-out/third_party/flatbuffers/include/flatbuffers/* tflm-out/third_party/flatbuffers
rm -rfv tflm-out/third_party/flatbuffers/include

# rename
rename -v 's/\.cc/\.cpp/' *.cc
rename -v 's/\.cc/\.cpp/' */*.cc
rename -v 's/\.cc/\.cpp/' */*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*/*/*.cc
rename -v 's/\.cc/\.cpp/' */*/*/*/*/*/*.cc

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

# examples/hello_world
mv esp-tflite-micro/examples/hello_world/main/* esp-tflite-micro/examples/hello_world
rm -rf esp-tflite-micro/examples/hello_world/main
rm -rf esp-tflite-micro/examples/hello_world/main.cpp
rm -rf esp-tflite-micro/examples/hello_world/*.txt
rm -rf esp-tflite-micro/examples/hello_world/sdkconfig.defaults
mv esp-tflite-micro/examples/hello_world/main_functions.cpp esp-tflite-micro/examples/hello_world/hello_world.ino
echo "" >esp-tflite-micro/examples/hello_world/main_functions.h
sed -i -e "1i #include <TFLM_ESP32.h>" esp-tflite-micro/examples/hello_world/hello_world.ino

# examples/micro_speech
mv esp-tflite-micro/examples/micro_speech/main/* esp-tflite-micro/examples/micro_speech
rm -rf esp-tflite-micro/examples/micro_speech/main
rm -rf esp-tflite-micro/examples/micro_speech/main.cpp
rm -rf esp-tflite-micro/examples/micro_speech/*.txt
rm -rf esp-tflite-micro/examples/micro_speech/sdkconfig.defaults
mv esp-tflite-micro/examples/micro_speech/main_functions.cpp esp-tflite-micro/examples/micro_speech/micro_speech.ino
echo "" >esp-tflite-micro/examples/micro_speech/main_functions.h
sed -i -e "1i #include <TFLM_ESP32.h>" esp-tflite-micro/examples/micro_speech/micro_speech.ino

# examples/person_detection
mv esp-tflite-micro/examples/person_detection/main/* esp-tflite-micro/examples/person_detection
rm -rf esp-tflite-micro/examples/person_detection/main
rm -rf esp-tflite-micro/examples/person_detection/main.cpp
rm -rf esp-tflite-micro/examples/person_detection/*.txt
rm -rf esp-tflite-micro/examples/person_detection/sdkconfig.defaults
rm -rf esp-tflite-micro/examples/person_detection/sdkconfig.defaults.*
rm -rf esp-tflite-micro/examples/person_detection/Kconfig.projbuild
rm -rf esp-tflite-micro/examples/person_detection/*.csv
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

# src
cd "${TFLITE_LIB_DIR}"/src
rm -rf tensorflow
rm -rf third_party
rm -rf signal
mv "${TEMP_DIR}/tflm-out/tensorflow" tensorflow

# For this repo we are forking both the models and the examples.
rm -rf tensorflow/lite/micro/models
mkdir -p third_party/
/bin/cp -r "${TEMP_DIR}"/tflm-out/third_party/* third_party/
mkdir -p signal/
/bin/cp -r "${TEMP_DIR}"/tflm-out/signal/* signal/

cd ..

# examples
rm -rf examples
cp -r "${TEMP_DIR}"/esp-tflite-micro/examples .

rm -rf "${TEMP_DIR}"
