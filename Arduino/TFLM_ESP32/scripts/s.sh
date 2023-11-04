#!/bin/bash
rm -rfv work
mkdir work
cd work

# get the examples
git clone --depth 1 --single-branch "https://github.com/edgeimpulse/tflite-micro-esp-examples.git"
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
mv tflite-micro-esp-examples/components/esp-tflite-micro/third_party/flatbuffers/include/flatbuffers/* tflite-micro-esp-examples/components/esp-tflite-micro/third_party/flatbuffers
rm -rfv tflite-micro-esp-examples/components/esp-tflite-micro/third_party/flatbuffers/include

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
rm -rfv ../src/tensorflow
rm -rfv ../src/third_party
rm -rfv ../src/signal
cp -r tflite-micro-esp-examples/components/esp-tflite-micro/tensorflow ../src/
cp -r tflite-micro-esp-examples/components/esp-tflite-micro/third_party ../src/
cp -r tflite-micro-esp-examples/components/esp-tflite-micro/signal ../src/

