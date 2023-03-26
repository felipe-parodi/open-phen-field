# Open Field Tracking for Human Behavior Phenomenology in Virtual Reality
This repository contains scripts and results related to computer vision analyses for each camera used in open-field tracking experiments for studying the phenomenology of human behavior in virtual reality. Specifically, the repository includes scripts and results for the top-down camera and the side-view camera.

### Top-Down Camera
The top-down camera is used for person detection and subsequent kinematic analyses, including thigmotaxis and velocity tracking. The scripts included in this folder allow for the automated detection and tracking of individuals in the virtual reality environment, as well as the calculation of various kinematic measures, including:

Thigmotaxis: the degree to which individuals move around the edges of the virtual environment
Velocity: the speed and direction of movement of individuals throughout the virtual environment

### Side-View Camera
The side-view camera is used for person pose estimation and subsequent kinematic analyses, including 3D pose lifting, eye scanning, and upper limb velocity. The scripts included in this folder allow for the automated estimation of the 3D pose of individuals in the virtual reality environment, as well as the calculation of various kinematic measures, including:

3D Pose Lifting: the transformation of the 2D pose estimate to a 3D estimate of the position and orientation of the individual
Eye Scanning: the degree to which individuals scan the virtual environment with their eyes
Upper Limb Velocity: the speed and direction of movement of the upper limbs of individuals throughout the virtual environment

### Results
The "results" folder contains the output data and analysis results generated by the scripts in the "src" folder. These results can be used for further analysis and visualization of the kinematic measures calculated for each camera view.

### Getting Started
To get started with using the scripts in this repository, clone the repository to your local machine and install any necessary dependencies. Then, use the scripts in the "src" folder to analyze your own open-field tracking data for studying the phenomenology of human behavior in virtual reality.

### Contributing
Contributions to this project are welcome and encouraged. If you notice any bugs or have ideas for additional features, please submit a pull request or open an issue on the GitHub repository.

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.
