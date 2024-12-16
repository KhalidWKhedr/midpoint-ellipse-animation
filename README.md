Animated Ellipse Motion Using Midpoint Algorithm

This repository implements a graphical simulation of an ellipse with animated motion based on the midpoint ellipse drawing algorithm. It allows users to input various parameters for the ellipse's center, radii, and rotation time via a Tkinter form, and generates an animated plot using Matplotlib. The animation simulates an object moving along the ellipse's path, with adjustable rotation time and visual elements such as the center, foci, and ellipse axes.

Key Features:

    User-friendly interface built with Tkinter to configure ellipse parameters.
    Real-time animation using Matplotlib, demonstrating motion along the ellipse.
    Adjustable parameters like center coordinates, radii, and rotation time.
    Support for limited functionality if ffmpeg is not installed.
    Visual enhancements like foci and axis markers.

Dependencies:

    matplotlib: For creating the animated plot.
    cv2 and numpy: For numerical operations and graphical calculations.
    tkinter: For the input form and UI.
    ffmpeg (optional): For enhanced animation functionality.

Installation:

    Install the required dependencies:

    pip install matplotlib opencv-python numpy

    If you wish to use full animation functionality, ensure ffmpeg is installed on your system.

Usage:

    Run the Python script.
    Use the Tkinter form to input ellipse parameters.
    Press "Enter" to generate the animated motion on an ellipse.
