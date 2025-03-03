# **Super Mario AI**

Super Mario AI is a modern reimagining of the classic Super Mario Bros game, developed using the Phaser framework with integrated gesture-based controls for Mario. This project aims to preserve the nostalgia of the iconic platformer while enhancing gameplay with Computer Vision and MediaPipe for a unique and immersive experience. Additionally, the game features random level generation, ensuring that each playthrough offers a dynamic and challenging environment.


## **Table of Contents**

- [TechStack](#TeckStack)
- [Controls](#Controls)

### TechStack

Technologies used here:

- Flask
- Phaser.js
- HTML/CSS
- Mediapipe
- OpenCV

### Controls

Controls are fully customizable, however default controls are:

**Jump:** ↑

**Move Left:** ←

**Move Right:** →

**Crouch:** ↓

**Fire:** Q

### Gesture Controls


**Jump:** Both hands open

**Move Left:** Left Fist only

**Move Right:** Right Fist only

**Crouch:** Both hands fist

**Fire:** Any hand fist with an open hand


<!-- ----------------------------added by priyanka------------------------------ -->

for hand tracking: use mediapipe since it has built-in handtracking
Use WebSockets or Flask-SocketIO to send real-time hand positions from the Python backend to the Phaser game.
