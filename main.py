import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import numpy as np
import datetime
import time
import tkinter as tk
import copy
import tkinter.font as font
import sys
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

###############################################################################
# The next section is using tkinter to create a an input form to input
# the needed values for animation
###############################################################################


def show_progress_message():  # function gets called when user press the NEXT button
    b1.configure(text="Generating Graphics - Please Wait", relief=tk.SUNKEN)  # change button label to progressing
    b1.update()     # display the new label
    master.quit()   # quit the form


master = tk.Tk()    # create new form
master.title("Configuration Parameters")

master.geometry("380x200")
tk.Label(master, text="X-coordinate of the ellipse Center in pixels:",    width=40, anchor=tk.W).grid(row=0)
tk.Label(master, text="Y-coordinate of the ellipse Center in pixels:",    width=40, anchor=tk.W).grid(row=1)
tk.Label(master, text="X-Radius in pixels (preferred Range is 50-1000):", width=40, anchor=tk.W).grid(row=2)
tk.Label(master, text="Y-Radius in pixels (preferred Range is 50-1000):", width=40, anchor=tk.W).grid(row=3)
tk.Label(master, text="Time in seconds for one full rotation(min=1sec):", width=40, anchor=tk.W).grid(row=4)

i_xc = tk.Entry(master, width=5)
i_yc = tk.Entry(master, width=5)
i_rx = tk.Entry(master, width=5)
i_ry = tk.Entry(master, width=5)
i_cycleTime = tk.Entry(master, width=5)

i_xc.insert(5, 100)          # initial value for xc
i_yc.insert(5, 100)          # initial value for yc
i_rx.insert(5, 300)          # initial value for rx
i_ry.insert(5, 150)          # initial value for ry
i_cycleTime.insert(10, 5)    # initial value for rotation time

i_xc.grid(row=0, column=1)
i_yc.grid(row=1, column=1)
i_rx.grid(row=2, column=1)
i_ry.grid(row=3, column=1)
i_cycleTime.grid(row=4, column=1)

# create a button labelled NEXT. Pressing it will call function show_progress_message
b1 = tk.Button(master, text=' Enter ', command=show_progress_message, bg='green', fg='white', width=26,
               activebackground='blue')
b1.grid(row=6)

Btn1Font = font.Font(size=8, slant=font.ITALIC)
checkBtn1 = tk.IntVar()
b2 = tk.Checkbutton(master, wraplength=300, justify=tk.LEFT, variable=checkBtn1,
                    text="check only if you cannot install ffmpeg. When checked, the running timer won't be displayed "
                         "and the desired rotation time won't be accomplished", font=Btn1Font)
b2.grid(row=7, sticky=tk.W)


master.mainloop()        # Loop to stay in the input form until user quits when pressing the NEXT button

######################################################################
# End of the input form above.
######################################################################
# get the check button value to see this will run with ffmpeg or not
######################################################################
no_ffmpeg_option = checkBtn1.get()
if no_ffmpeg_option:
    print('no ffmpeg option was chosen. This program will run with limited functionality.')
    print('The desired rotation time for animation won''t be achieved and the timer won''t be displayed')
############################################################
# Below, extracting the needed values from the form variables
############################################################
xc = int(i_xc.get())
yc = int(i_yc.get())
rx = int(i_rx.get())
ry = int(i_ry.get())
desiredRotationTimeInSec = max(int(i_cycleTime.get()), 1)  # get rotation time (min=1sec)

#############################################################
# MidPoint Ellipse Graphing Algorithm
#############################################################


def midpoint_graph_ellipse(p_xc, p_yc, p_rx, p_ry):
    list_points = []  # a list that will store all the calculated graph points
    ############################################################################
    # The list has five values: x & y of the calculated pixel, the quadrant (1,2,3,4),
    # an altered value of the x and y as explained in the my document
    # that are used with the quadrant to sort the pixels of the ellipse
    # in the array to start from x=rx,y=0 going all the way counter clockwise
    # until it reaches the starting point
    ############################################################################

    # starting point
    xk = 0
    yk = p_ry

    # calculate initial decision parameter of region 1
    pk1 = ((ry * ry) - (rx * rx * ry) + (0.25 * rx * rx))

    # region-1
    # looping to calculate the graph points
    while ry * ry * xk < rx * rx * yk:

        # Add four points to the list based on symmetry
        list_points.append((xk + p_xc, yk + p_yc, 1, -xk, yk))
        list_points.append((-xk + p_xc, yk + p_yc, 2, xk, -yk))
        list_points.append((-xk + p_xc, -yk + p_yc, 3, -xk, yk))
        list_points.append((xk + p_xc, -yk + p_yc, 4, xk, -yk))

        # calculate new points and updating value of
        # decision parameter using midpoint algorithm
        if pk1 < 0:
            xk = xk + 1
            pk1 = pk1 + 2 * p_ry * p_ry * xk + p_ry * p_ry
        else:
            xk = xk + 1
            yk = yk - 1
            pk1 = pk1 + 2 * p_ry * p_ry * xk + + p_ry * p_ry - 2 * p_rx * p_rx * yk

    # calculate initial decision parameter of region 2
    pk2 = (p_ry * p_ry) * (xk + 0.5) * (xk + 0.5) + (p_rx * p_rx) * (yk - 1) * (yk - 1) - p_rx * p_rx * p_ry * p_ry

    # region-2
    # looping to calculate the graph points
    while yk >= 0:
        list_points.append((xk + p_xc, yk + p_yc, 1, -xk, yk))
        list_points.append((-xk + p_xc, yk + p_yc, 2, xk, -yk))
        list_points.append((-xk + p_xc, -yk + p_yc, 3, -xk, yk))
        list_points.append((xk + p_xc, -yk + p_yc, 4, xk, -yk))

        # calculate new points and updating value of
        # decision parameter using midpoint algorithm
        if pk2 > 0:
            yk = yk - 1
            pk2 = pk2 - (2 * p_rx * p_rx * yk) + (p_rx * p_rx)
        else:
            yk = yk - 1
            xk = xk + 1
            pk2 = pk2 - (2 * p_rx * p_rx * yk) + (p_rx * p_rx) + 2 * p_ry * p_ry * xk

    return list_points


#########################################################################################
# Calculate the coordinate of the foci
#########################################################################################
fociLength = int(math.sqrt(abs(pow(rx, 2) - pow(ry, 2))))

if rx >= ry:
    foci_1_x = xc + fociLength
    foci_1_y = yc
    foci_2_x = xc - fociLength
    foci_2_y = yc
else:
    foci_1_x = xc
    foci_1_y = yc + fociLength
    foci_2_x = xc
    foci_2_y = yc - fociLength

# call the midpoint function to calculate the pixels and load them back
# in list pointsList
pointsList = midpoint_graph_ellipse(xc, yc, rx, ry)


#print(*pointsList, sep = "\n")

# sort the pixels using the last three tuples, check the documentation for details
pointsList.sort(key=lambda t: (t[2], t[3], t[4]))

# load the values from the list to new array called PixelList
PixelList = np.array(pointsList)

# print(PixelList.shape)
print('Number of generated pixels for the ellipse = ' + str(PixelList.shape[0]))
print('Maximum number of frames that can be animated = ' + str(PixelList.shape[0]))

rotatingCircleRadius = max(int((rx + ry) / 16), 2)  # create proportional circle based on rx & ry with minimum radius=2
patchCircle = plt.Circle((rx + xc, 0), rotatingCircleRadius, fc='green', ec='black')  # show circle

####################################################
# create figure to display the ellipse and animation
####################################################
config_line_txt = 'xc=' + str(xc) + ', yc=' + str(yc) + ', rad-x=' + str(rx) + \
                  ', rad-y=' + str(ry) + ', rotation time=' + str(desiredRotationTimeInSec)
fig1, ax1 = plt.subplots()
fig1.set_dpi(100)
fig1.set_size_inches(8, 6)

x_min = xc - rx - rotatingCircleRadius * 2  # calculate the minimum value of x in the graph
x_max = xc + rx + rotatingCircleRadius * 2  # calculate the maximum value of x in the graph
y_min = yc - ry - rotatingCircleRadius * 2  # calculate the minimum value of y in the graph
y_max = yc + ry + rotatingCircleRadius * 2  # calculate the maximum value of y in the graph

# make the two ranges of x and y to be same and equal to the biggest one
axis_min = min(x_min, y_min)  # find the smallest value
axis_max = max(x_max, y_max)  # find the biggest value

ax1 = plt.axes(xlim=(axis_min, axis_max), ylim=(axis_min, axis_max + 40))  # draw the axis
ax1.set(xlabel='X-Axis', ylabel='Y-Axis', title=config_line_txt)
fig1.suptitle('Animated Motion on an Ellipse Path Generated Using Midpoint Algorithm', fontsize=12)
# Enable minor ticks
ax1.minorticks_on()

# Enable and style minor gridlines with red color, solid line style, and a linewidth of 2
ax1.grid(which='minor', axis='both', color='r', linestyle='-', linewidth=2, alpha=0.1)

# Enable and style major gridlines with black color, solid line style, and a linewidth of 2
ax1.grid(which='major', axis='both', color='k', linestyle='-', linewidth=2, alpha=0.4)

plt.axis('equal')  # make the x and y axis the same size

# draw the ellipse axis (the major and minor axis)
ax1.plot([xc - rx, xc + rx], [yc, yc], color='red', linestyle='--')
ax1.plot([xc, xc], [yc - ry, yc + ry], color='red', linestyle='--')

# Mark the center and central points
ax1.plot(xc, yc, marker='+', color='black')  # mark the center point
ax1.plot(foci_1_x, foci_1_y, marker='o', color='black')  # mark the fist foci
ax1.plot(foci_2_x, foci_2_y, marker='o', color='black')  # mark the second foci

####################################################################################
# Display a message to explain what to press to quit
# Press Escape if using ffmpeg
# close the window if not using ffmpeg
####################################################################################
if no_ffmpeg_option:
    how_to_exit_txt = 'Close The Window to Quit'
else:
    how_to_exit_txt = 'Press Escape to Quit'

plt.text(0.5 * (x_min + x_max), 0.5 * (y_min + y_max) + ry * 0.25, how_to_exit_txt, size=15, color='purple',
         horizontalalignment='center',
         verticalalignment='center')

###########################################################################
# draw the ellipse using the array of generated points
# the x values are in column 1 of the array
# and the y values are in column 2 of the array
# it is one call using the array and specifying the two columns for x & y
###########################################################################
ax1.plot(PixelList[:, 0], PixelList[:, 1], marker='.', color='blue')


##########################################################################
# Below code to animate the circle
##########################################################################

def init_circle():      # The first frame draw the circle with its center on the first point of the ellipse
    xa = PixelList[0, 0]  # the x value of the first ellipse point
    ya = PixelList[0, 1]  # the y value of the first ellipse point
    patchCircle.center = (xa, ya)
    ax1.add_patch(patchCircle)
    return patchCircle,


def animate_circle(i):  # animate the circle moving its center on the next points of the ellipse changing value of i
    xa = PixelList[i * scaleFactor, 0]  # next point of ellipse is determined by the calculated scaleFactor
    ya = PixelList[i * scaleFactor, 1]  # if scaleFactor = 1, then all the ellipse points will be used
    patchCircle.center = (xa, ya)  # draw the circle using the new center
    return patchCircle,


ellipseTotalPoints = PixelList.shape[0]  # get the total number of points of the ellipse

#################################################################################
# I like to have 30 fps as the basis for the calculation below
#################################################################################
desiredNumberOfFrames = 30 * desiredRotationTimeInSec
print('Requested rotation time in seconds = ' + str(desiredRotationTimeInSec))
print('Desired Number of Frames using 30 fps = ' + str(desiredNumberOfFrames))

scaleFactor = max(int(ellipseTotalPoints / desiredNumberOfFrames), 1)
print('Desired scale factor (number of ellipse points to skip in each frame) = ' + str(scaleFactor))

# adjusting the desired number of frames to avoid a big jump in the last frame
desiredNumberOfFrames = int(ellipseTotalPoints / scaleFactor)
print('Adjusted desired Number of Frames = ' + str(desiredNumberOfFrames))

adjusted_fps = int(desiredNumberOfFrames / desiredRotationTimeInSec)
print('Adjusted frames per second to achieve requested rotation time = ' + str(adjusted_fps))

frameInterval = int(1000 / adjusted_fps)  # time for each frame in ms

# animate the circle with number of iterations = desiredNumberOfFrames
anim1 = animation.FuncAnimation(fig1, animate_circle, init_func=init_circle, frames=desiredNumberOfFrames,
                                repeat=True, save_count=20,
                                interval=frameInterval,
                                blit=True)

# Disabled because it does not work in Jupyter
# if no_ffmpeg_option:
#     master.destroy()
#     plt.show()
#     sys.exit(0)  # exit the program

###################################################################################
# code below does the following:
# writing the animation to a video file using ffmpeg
# make sure you have ffmpeg installed and it is in your SYSTEM PATH variable
# you can install any of the releases available here:
# https://github.com/BtbN/FFmpeg-Builds/releases
# if you have trouble to get ffmpeg installed and in the path
# you can comment te line above "plt.show" and you will see the animation
# but it will not run in the desired rotation time and won't have a timer
###################################################################################
myWriter = animation.FFMpegWriter(fps=adjusted_fps)
anim1.save(r'movie.mp4', writer=myWriter)

####################################################################################
# open the video file
# read all the frames and cache them all in a list called "frames_list"
####################################################################################
cap = cv2.VideoCapture(r'movie.mp4')
file_fps = cap.get(cv2.CAP_PROP_FPS)
frame_wait = int(round(1000 / file_fps))  # frame wait in milliseconds
print("Frames per second found in video file using video.get(cv2.CV_CAP_PROP_FPS): {0}".format(file_fps))
frames_list = []
while True:
    ret, frame = cap.read()
    if ret:
        frames_list.append(frame)   # expand the list and add all the frames until the end of the file
    else:
        break
cap.release()

# above, done caching all the frames

# below, starting to show the frames
master.destroy()  # close the input form (tkinter window)
while True:
    isclosed = 0
    next_frame_time = datetime.datetime.utcnow()
    for single_frame in frames_list:
        t0 = datetime.datetime.utcnow()
        if cv2.waitKey(1) == 27:
            # When esc is pressed set isclosed to 1 to break the outer loop
            isclosed = 1
            break
        while datetime.datetime.utcnow() < next_frame_time:
            time.sleep(0.001)
        t1 = datetime.datetime.utcnow()
        sleep_error = int((t1 - next_frame_time).microseconds / 1000)
        datetime_str = str(datetime.datetime.now().strftime("%H:%M:%S.%f"))
        # copy the frame by value instead of reference to single_frame_new
        single_frame_new = copy.deepcopy(single_frame)
        # add the timestamp to the displayed frame
        single_frame_new = cv2.putText(single_frame_new, datetime_str, (100, 100), cv2.FONT_HERSHEY_PLAIN, 2,
                                       (255, 0, 0), 2,
                                       cv2.LINE_AA)
        # show the frame with the timestamp
        cv2.imshow('frame', single_frame_new)
        t2 = datetime.datetime.utcnow()
        frameShowTime = int((t2 - t1).microseconds / 1000)
        # compensate for the inaccuracy in time.sleep() function
        next_frame_time = datetime.datetime.utcnow() + datetime.timedelta(
            milliseconds=(frame_wait - frameShowTime - sleep_error))

    # To break the loop if the user pressed ESCAPE

    if isclosed:
        # master.destroy()          # close tkinter window
        cv2.destroyAllWindows()   # close the file input resources
        break                     # exit the animation loop and quit

# version 1.6
