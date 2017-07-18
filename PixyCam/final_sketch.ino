//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//
// This sketch is a good place to start if you're just getting started with 
// Pixy and Arduino.  This program simply prints the detected object blocks 
// (including color codes) through the serial console.  It uses the Arduino's 
// ICSP port.  For more information go here:
//
// http://cmucam.org/projects/cmucam5/wiki/Hooking_up_Pixy_to_a_Microcontroller_(like_an_Arduino)
//
// It prints the detected blocks once per second because printing all of the 
// blocks for all 50 frames per second would overwhelm the Arduino's serial port.
//

#include <SPI.h>  
#include <Pixy.h>
FILE* fp;
// This is the main Pixy object 
Pixy pixy;
int car1 = 0;
int car2 = 0;

void setup()
{
  Serial.begin(9600);
  fp = fopen("/home/root/SpotEV/HardwareSide/ultraSonicSensor/out.txt", "w+");
  Serial.print("Starting...\n");
  fprintf(fp, "starting\n");
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
    
    // do this (print) every 100 frames because printing every
    // frame would bog down the Arduino
    if (i%50==0)
    {
      sprintf(buf, "Detected %d:\n", blocks);
      Serial.print(buf);
      fprintf(fp, "time: %d\n", i);
      for (j=0; j<blocks; j++)
      {
        if (pixy.blocks[j].width > 30 && pixy.blocks[j].height > 30 && pixy.blocks[j].signature != 1
            && pixy.blocks[j].width < 300 && pixy.blocks[j].height < 180){
          sprintf(buf, "  block %d: ", j);
          Serial.print(buf); 
          pixy.blocks[j].print();
          int sig = pixy.blocks[j].signature;
          if (sig == 2){
            car1 = 1;
          }
          if (sig == 3){
            car2 = 1;
          }
           fprintf(fp, " block %d: ", j);
          fprintf(fp, "sig %d\n", sig);
          fprintf(fp, "width %d\n", pixy.blocks[j].width);
          fprintf(fp, "height %d\n", pixy.blocks[j].height);
        }
      }
      fprintf(fp, "status: %d,%d\n", car1, car2);
      car1 = 0;
      car1 = 0;
      fflush(fp);  
    }
  }
}

