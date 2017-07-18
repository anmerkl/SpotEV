FILE* fp; 
#include <SPI.h>  
#include <Pixy.h>

// This is the main Pixy object 
Pixy pixy;

void setup()
{
  Serial.begin(9600);
  fp = fopen("rslt2.txt", "a");
  fprintf(fp, "Starting...\n");
  pixy.init();
}

void loop()
{ 
  static int i = 0;
  int j;
  uint16_t blocks;
  char buf[32]; 
  
  // grab blocks!
  blocks = pixy.getBlocks();
  
  // If there are detect blocks, print them!
  if (blocks)
  {
    i++;
    
    // do this (print) every 50 frames because printing every
    // frame would bog down the Arduino
    if (i%150==0)
    {
      fprintf(fp, "Detected %d:\n", blocks);
      Serial.print(buf);
      for (j=0; j<blocks; j++)
      {
        //if (pixy.blocks[j].width > 30 && pixy.blocks[j].height > 30 && pixy.blocks[j].signature != 1){
        fprintf(fp, "  block %d: ", j);
         Serial.print(buf); 
          pixy.blocks[j].print();
          Serial.print("signature:\n");
         // Serial.print(pixy.blocks[j].signature);
          fprintf(fp, "signature:\n%s", pixy.blocks[j].signature);
          Serial.print("\n"); 
        //}
      }
      fprintf(fp, "End of blocks\n\n\n");
    }
  }  
  
  fflush(fp);
}


