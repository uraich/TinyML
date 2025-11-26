# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/esp-idf/esp-idf_v5.1/esp-idf/components/bootloader/subproject"
  "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader"
  "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix"
  "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix/tmp"
  "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix/src/bootloader-stamp"
  "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix/src"
  "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/Administrator/Desktop/ESP32-Exrenal-data/ESP32-CAM-S00X/ESP32-S3-MINI/ESP-IDF_v5.0.3/ESP32-S3MINI/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
