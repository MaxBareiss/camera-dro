# Camera DRO

The basic idea here is that you can use a camera to sense the change in position
of a milling machine table, simulating a Digital Read Out (DRO).

This project is in pre-alpha stage (it just barely works).

# Procedure

1. Print out `board.pdf`.
2. Make sure the capture number is right in `calib.py` and `main.py`.
2. Run `calib.py` for your camera to get the calibration parameters.
3. Copy-paste those into `main.py`.
4. Run `main.py`.
5. Make sure the board printout is attached to something rigid and flat, and 
then attached to the mill table. Make sure the webcam is securely fastened to
the mill head and can see the board printout.
6. Press the spacebar in the window that comes up to zero the machine.

# Dependencies

* Python 3
* OpenCV with aruco
