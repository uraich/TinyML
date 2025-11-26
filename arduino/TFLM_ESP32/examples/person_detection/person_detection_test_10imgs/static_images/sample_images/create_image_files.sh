#!/bin/bash
# The shell script concatenates the image files image(0--9).cpp and
# image(0--9).h in 1 file respectively
# It also removes the
# #include <cstdint> line from all files except thee first one
# Copyright (c) U. Raich, Nov 2023
# This shell script  is part of the course on TinyML
# at the University of Cape Coast, Ghana

# Create the cpp and h files from the binary image data
for i in 0 1 2 3 4 5 6 7 8 9; do
    python3 convertToCpp.py image$i
done

cp image0.cpp tmp_img0.cpp
cp image0.h img0.h
sed 's/image0.h/images.h/' tmp_img0.cpp > img0.cpp
rm tmp_img0.cpp

# remove the #include <cstdint> line from all image files except the first one
for i in 1 2 3 4 5 6 7 8 9; do
    sed '/include/d' image$i.cpp > img$i.cpp
    sed '/include/d' image$i.h > img$i.h
done
rm -f images.cpp
rm -f images.h
# concatenate all image files into images.cpp and images.h
for i in 0 1 2 3 4 5 6 7 8 9; do
    # echo 'cat img'$i'.cpp >> images.cpp'
    cat  img$i.cpp >> images.cpp
    cat  img$i.h >> images.h
    rm img$i.cpp
    rm img$i.h
done
