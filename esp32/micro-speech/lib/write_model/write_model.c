#include <stdio.h>

int main(int argc, char ** argv) {
  FILE *f;
  const int file_length = 18712;
  unsigned char buf[18800];
  f = fopen("../model.tflite","rb");
  fread(buf,file_length,1,f);
  fclose(f);
  // write to a text file
  f = fopen("model.txt","w");
  
  for (int i=0;i<file_length;i++) {
    if (!(i % 16) && (i != 0))
      fprintf(f,"\n");
    fprintf(f,"0x%02x, ",buf[i]);
  }
  fclose(f);
}
