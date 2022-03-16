# RB-CODE-Prototype-1

##### This code runs the rolling block display. 

### The rolling blocks display is a mechanically multiplexed 2-bit display
#### The multiplexing works by locking rows and rotating columns such that only pixels in the unlocked rows are turned. This allows for the display's pixels to be articulated to show whatever image. A clever algorithim would optimize the actuation of the row and column servos to change the image in as few moves as possible. Astar (weighting actuation time and progress towards final image) would get you the most optimized path, but it is extremely computionally expensive.

### Why
#### I want to make more robots that illustrate some sort of computation in their movement. I hope the animations (path between images) are mesmerizing to watch.

### Electronics
#### The system is run by a bank of servos one on the side and one on the top or bottom. The servos have no feedback and run off postion control. Although servos with feedback would be wonderful, they are not worth the added cost. The feedbackless servos actuation time is very predictable. If the lack of position sensing proves to be an issue, I will add it.
#### Groups of 16 servos go into a daughter board with an stm32 on it. The stm32 communicate over I2C to the main controller, a rasberrypi 4

### Re-Zeroing
#### I will write out the mechanical novelties of this design on my blog Zekebuild.com when the project is complete.

### First Full Working Simulation 3/16 4:00am
