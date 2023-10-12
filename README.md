# TinyML
These are demo programs for a course on TinyML at the University of Cape Coast, Ghana.

The repository is based on the examples in the [tflite micro repository](https://github.com/tensorflow/tflite-micro). There you find the following examples:
* Hello World
* memory_footprint
* mnist_lstm
* network_tester (not used)
* person_detection
* recipes

In addition the _magic wand_ examples from the [TinyML book](https://zlib.pub/book/tinyml-machine-learning-with-tensorflow-lite-on-arduino-and-ultra-low-power-microcontrollers-vshhregc28o0) will be ported to the ESP32.

The tflite micro repository now uses _bazel_ to build its programs. Some of the jupyter notebooks described in the TinyML book are not available any longer. I rebuilt these notbooks and included them in this repository.
The hardware I use is thee following:
![esp32s3_cpu](images/esp32s3_cpu.png)
The WeMos ESP32S3 CPU comes with 4 MBytes of flash and 2 MBytes of PSRAM. The pinout is shown below:


# This is work in progress and some of the programs may not work yet 
