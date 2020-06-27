# Prerequisitions:
    - OpenCV, at least 4.1.2
    - C++ Complier, recommending MSVC
    - Python 3, at least 3.6
    - IDE of choice, recommeding Microsoft Visual Studio
    - DirectShow driver, usually pre-installed in any Windows system.

# Installation guide
    - Install Python3, C++ Complier and any preferred IDE
    - Build OpenCV from source code in debug mode, as well as adding OpenCV to PATH
    - Open the \src folder and comply main.cpp and Piece.cpp in Debug mode, go back to \x64\Debug, there should be a PieceRecog.exe there.

# Running the program
    - Connect the camera and the system to the laptop. In case of using a PC with no other camera, change the  cv::VideoCapture camera(1 + cv::CAP_DSHOW); in main.cpp to  cv::VideoCapture camera(0 + cv::CAP_DSHOW); , then recomply the program.
    - Go to **PieceRecog-ChessEngine\x64\Debug-USE THIS FILE TO RUN** and open a terminal here.
    - Type in python main.py, the program should start running and showing "Waiting for user input".
    - Move a piece and then hit the green button next to the system to alert the system of move completion, the program will capture image and commit the next move.

# Other document 
    - In this repository also include the thesis file,readme for scara arm and 3d scara model 