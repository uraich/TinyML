/* Copyright 2022 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/
#include <TFLM_ESP32.h>
#include "tensorflow/lite/c/common.h"
#include "model_settings.h"
#include "no_person.h"
#include "person.h"
#include "person_detect_model_data.h"

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* input = nullptr;
  
  // In order to use optimized tensorflow lite kernels, a signed int8_t quantized
  // model is preferred over the legacy unsigned model format. This means that
  // throughout this project, input images must be converted from unsigned to
  // signed format. The easiest and quickest way to convert from unsigned to
  // signed 8-bit integers is to subtract 128 from the unsigned value to get a
  // signed value.
  
  // An area of memory to use for input, output, and intermediate arrays.
  constexpr int kTensorArenaSize = 136 * 1024;
  alignas(16) static uint8_t tensor_arena[kTensorArenaSize];
  
}  // namespace

void setup() {
  
  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  const tflite::Model* model = ::tflite::GetModel(g_person_detect_model_data);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    MicroPrintf(
        "Model provided is schema version %d not equal "
        "to supported version %d.\n",
        model->version(), TFLITE_SCHEMA_VERSION);
  }

  // Pull in only the operation implementations we need.
  // This relies on a complete list of all the ops needed by this graph.
  // An easier approach is to just use the AllOpsResolver, but this will
  // incur some penalty in code space for op implementations that are not
  // needed by this graph.
  tflite::MicroMutableOpResolver<5> micro_op_resolver;
  micro_op_resolver.AddAveragePool2D(tflite::Register_AVERAGE_POOL_2D_INT8());
  micro_op_resolver.AddConv2D(tflite::Register_CONV_2D_INT8());
  micro_op_resolver.AddDepthwiseConv2D(
      tflite::Register_DEPTHWISE_CONV_2D_INT8());
  micro_op_resolver.AddReshape();
  micro_op_resolver.AddSoftmax(tflite::Register_SOFTMAX_INT8());

  // Build an interpreter to run the model with.
  tflite::MicroInterpreter interpreter(model, micro_op_resolver, tensor_arena,
                                       kTensorArenaSize);
  interpreter.AllocateTensors();

  // Get information about the memory area to use for the model's input.
  TfLiteTensor* input = interpreter.input(0);

  // Copy an image with a person into the memory area used for the input.
  // convert the pixels from uint8_t to int8_t (unsigned to signed) as
  // expected by the model
  /*
  uint8_t* ptr = const_cast<uint8_t*>(g_person_data); 
  for (int j=0; j<g_person_data_size; j++) {
    input->data.int8[j] = *ptr ^ 0x80; 
    ptr++;
  }
  */
  memcpy(input->data.int8, g_person_data, input->bytes);

  // Run the model on this input and make sure it succeeds.
  TfLiteStatus invoke_status = interpreter.Invoke();
  if (invoke_status != kTfLiteOk) {
    MicroPrintf("Invoke failed\n");
  }

  // Get the output from the model, and make sure it's the expected size and
  // type.
  TfLiteTensor* output = interpreter.output(0);

  // Make sure that the expected "Person" score is higher than the other class.
  int8_t person_score = output->data.int8[kPersonIndex];
  int8_t no_person_score = output->data.int8[kNotAPersonIndex];
  
  float person_score_f =
    (person_score - output->params.zero_point) * output->params.scale;
  float no_person_score_f =
    (no_person_score - output->params.zero_point) * output->params.scale;
    
  MicroPrintf("person data.  person score: %d, no person score: %d\n",
              person_score, no_person_score);
  
  MicroPrintf("person data.  person score: %5.2f, no person score: %5.2f\n",
              person_score_f, no_person_score_f);
  
  // convert the pixels from uint8_t to int8_t (unsigned to signed) as
  // expected by the model
  /*
  ptr = const_cast<uint8_t*>(g_no_person_data); 
  for (int j=0; j<g_no_person_data_size; j++) {
    input->data.int8[j] = *ptr ^ 0x80; 
    ptr++;
  }
  */
  memcpy(input->data.int8, g_no_person_data, input->bytes);

  // Run the model on this "No Person" input.
  invoke_status = interpreter.Invoke();
  if (invoke_status != kTfLiteOk) {
    MicroPrintf("Invoke failed\n");
  }

  // Get the output from the model, and make sure it's the expected size and
  // type.
  output = interpreter.output(0);

  // Make sure that the expected "No Person" score is higher.
  person_score = output->data.int8[kPersonIndex];
  no_person_score = output->data.int8[kNotAPersonIndex];

  person_score_f =
    (person_score - output->params.zero_point) * output->params.scale;
  no_person_score_f =
    (no_person_score - output->params.zero_point) * output->params.scale;
  
  MicroPrintf("no person data.  person score: %d, no person score: %d\n",
              person_score, no_person_score);
  
  MicroPrintf("person data.  person score: %5.2f, no person score: %5.2f\n",
              person_score_f, no_person_score_f);
  
}
void loop() {
}
