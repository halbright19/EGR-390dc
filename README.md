# EGR 390dc Final Project
## LED Joystick Controlled Etch A Sketch
### Addie Hannan and Helen Albright

## Introduction:

We designed an Etch A Sketch of sorts using an LED dot matrix and an analog joystick. The main purpose was to create a fun toy and learn more about circuit components in the process. Our project has two modes of operation: move point and sketch. In the move point mode the lit up LED moves around the screen as controlled by the joystick. In sketch mode, the path stays lit up allowing the user to make designs.

## Circuit Components:

### Hardware Elements:
- (1) MAX7219 LED Dot Matrix Module
- (1) Analog Joystick Module
- (1) 10k ohm Potentiometer
- (1) Button switch
- (1) 10k ohm resistor
- (1) Arduino Uno
- Jumper cables

### Software Elements:
- StandardFirmata Arduino sketch
- Pyfirmata library
- led_matrix.py, Written by Sawyer McLane 
- Final.py (our main code)


## Circuit Diagrams for Individual Components:

 
MAX7219 LED Dot Matrix Module - Elegoo Lesson 15

 
Analog Joystick - Elegoo Lesson 1 
Pulldown Resistor Button Switch Circuit - roboticsbackend.com
 
Potentiometer Circuit - circuit.io

## Discussion:

The MAX9219 module consists of components we learned about in class including a multiplexer, BCD decoder, and RAM. Multiplexing enables us to control the 64 LEDs with the 16 pins on the 8 by 8 display. The 8 by 8 static ram is used to store each digit. This chip can also be used to control an 8 digit 7-segment display. The advantage to using this chip is to vastly simplify the wiring of our final circuit and avoid the need for numerous external resistors.  
One of the first problems we ran into was that the Arduino code for the MAX7219 LED Dot Matrix Module made use of an Arduino library. This proved to be the case for almost all of the complex sensors and output displays. During the exploration phase we also played with the RFID reader and components used in previous labs. Rewriting the Arduino library from scratch wasn’t feasible given the time constraints of this project. We observed the sequential nature of the circuit first hand when manually inputting 1s and 0s into the MAX7219 chip (via a nested for loop). Despite having the same input to the chip, each time we ran the test program the leds that lit up changed. For this reason we could not simply write values to the MAX7219 module. We almost scrapped the project but ultimately found a Python class for the MAX7219 LED Dot Matrix Module from game developer, Sawyer McLane.
After we got the dot matrix working with the Python code, we started implementing some functionality. We wanted to be able to move a single dot around the display, draw a line with the joystick, clear the screen and reset the position of the dot, and switch between the two operating modes. To switch between modes we used a 10k ohm potentiometer, with low resistance for the sketch mode and high resistance for the movePoint mode. To clear the screen we wanted to use a simple button switch. While the joystick module does have a button switch built-in it requires use of the Arduino’s internal pullup resistor. Arduino has a special pin mode called INPUT_PULLUP for this purpose, but pyFirmata does not support this pin mode. We also tried using a modified version of pyFirmata to support this pin mode, but ultimately had to use an external button switch with an external pulldown resistor for our clear screen functionality. 
 
Final circuit showcasing etch a sketch functionality

## Code Overview:

We programmed our Arduino in Python using the pyFirmata protocol and Sawyer McLane’s LedMatrix class. In the while loop of our main function we read in values from our button, potentiometer, joystick. When the button is pressed we call a custom reset function that clears the led matrix and returns the lit up dot to the upper left corner. To keep track of and update the operating mode we make use of the mode and oldMode Boolean variables in conjunction with the potentiometer values. To determine the direction from the joystick, we use a set of nested if, elif, and else statements. To keep the dot within bounds, we use our custom increment and decrement functions. For move point mode we use McLane’s maxSingle function to light up a single dot. For sketch mode, we use a Python matrix to store and update the pattern. We then display the matrix to the screen using McLanes draw_matrix function.

## Key Learning:

We learned how to integrate multiple sensors to create a fun and interactive project. We had to reference information from a variety of sources then adapt everything into Python code. We also gained a better understanding of each component by actually working with in and reading in input values. The next level would be focusing on a single component and designing it from the ground up. During this process we also got to dive deeper into thinking about and designing both combinational and sequential circuits. 

## Extensions:

If we had more time, we would have liked to design an actual game. Beyond just moving around the grid, the user could have an actual goal and means of winning. Additionally, we would have liked to integrate even more dot matrices and make the project more user friendly. For instance, we could create an enclosure out of laser cut chipboard. This would protect the circuit, improve aesthetics, and enhance usability.  

## Sources:

MAX7219 driver datasheet, https://cdn-shop.adafruit.com/datasheets/MAX7219.pdf

8x8 LED display datasheet, https://cdn-shop.adafruit.com/datasheets/454datasheet.pdf 

“Using PyFirmata to rewrite an Arduino sketch”, Sawyer McLane, 2018, https://samclane.dev/Python-Arduino-PyFirmata/

“Arduino INPUT_PULLUP Explained (pinMode)”, The Robotics Back-End, https://roboticsbackend.com/arduino-input_pullup-pinmode/

ELEGOO Arduino Mega 2560 The Most Complete Starter Kit Tutorial,
https://www.elegoo.com/blogs/arduino-projects/elegoo-mega-2560-the-most-complete-starter-kit-tutorial 
