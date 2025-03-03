# **Super Mario AI**

Super Mario AI is a modern reimagining of the classic Super Mario Bros game, built with the Phaser framework along with gesture control for controlling Mario. This project seeks to revive the nostalgia of the legendary platformer while making it accessible on contemporary web browsers along with using Computer Vision and Mediapipe for unique and challenging twist. A standout aspect of the game is its random level generation, guaranteeing that every session presents a fresh and engaging challenge.


## **Table of Contents**

- [TechStack](#TeckStack)
- [Controls](#Controls)

### TechStack

Technologies used here:

Flask
Phaser.js
HTML/CSS
Mediapipe
OpenCV

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
