"""App to test time stamp accuracy compared with SCR collected from empatico.

Idea is simple, click a button when you start breathing in, another when you reach peak,
another when you start breathing out and last button click when your lungs aere empty.

Can try map this onto SCR timestamps.

KLP
09/2012"""


#NOTE: taken base code from blog example of animation using matplotlib
#https://gist.github.com/hugke729/ac3cf36500f2f0574a6f4ffe40986b4f.
#Major adaptations, including animation featues:
#Wrapped withing an animate function and added pause functionality
#And data features:
#added time stamping and other features.

#---------------------------------------------------------------------------
#Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from matplotlib.widgets import Button
import matplotlib.patches as patches
import time
import csv
import matplotlib as mpl



# Use matplotlib ggplot stylesheet if available
try:
    plt.style.use('ggplot')
except:
    pass

mpl.rcParams['toolbar'] = 'None'

# Create three-dimensional array of data G(x, z, t)
x = np.linspace(-4, 4, 91)
t = np.linspace(0, 25, 30)
y = np.linspace(-4, 4, 91)
X3, Y3, T3 = np.meshgrid(x, y, t)
sinT3 = np.sin(2*np.pi*T3 /
               T3.max(axis=2)[..., np.newaxis])
G = (X3**2 + Y3**2)*sinT3


# ----------------------------------------------------------------------------
# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# remove background
fig.patch.set_visible(False)
ax.axis('off')

# ----------------------------------------------------------------------------
# Set up options and animate function to apply these on repeat

contour_opts = {'levels': np.linspace(-9, 9, 12), 'cmap':'RdBu'}
cax = ax.contour(x, y, G[..., 0], **contour_opts)

def animate(i):
    ax.collections = []
    ax.contour(x, y, G[..., i], **contour_opts)
    time.sleep(0.2)


# ----------------------------------------------------------------------------
# Set up dictionary to hold data

timedata = {}

# Set up count variable to get number of clicks
count = 0


## set up animation function including play/pause

def run_animation():

    anim_running = True

    axpress = plt.axes([0.47, 0.45, 0.1, 0.075])
    bpress = Button(axpress, 'Press',
    color = "grey", hovercolor = "#489FA7")

    def onClick(event):
        global count
        count += 1
        current_datetime = datetime.now() # NOTE: Acquire the date time (to ms) on each click
        date = current_datetime.strftime('%Y-%m-%d')
        timenow = current_datetime.time().strftime('%H:%M:%S.%f')
        unix=time.mktime(current_datetime.timetuple())
        timedata[count] = date, timenow, unix
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            # add title
            plt.title("press to breathe")
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
            plt.title("press to hold")

    fig.canvas.mpl_connect('button_press_event', onClick)

    anim = FuncAnimation(fig, animate, interval=100, frames=len(t)-1, repeat=True)


    plt.show()

    # write the dictionary to csv
    with open('test_time.csv', 'w') as f:
        f.write("{0},{1},{2},{3}\n".format("ClickCount","Date","Time","Unix"))
        for key in timedata.keys():
            values = timedata[key]

            f.write("{0},{1},{2},{3}\n".format(key,values[0],values[1],values[2]))


#MsgBox = tk.messagebox.askokcancel(message='Welcome to breathing sync task. You will need to breathe in deeply, hold your breath, then breathe out again slowly.\n\nBefore beginning, press the start button in the centre of the moving circles. \nBreathe in as deeply as you can, then press the button again. Hold your breath for a count of 3, then press the button again and breathe out slowly.\n Press the button a final time.\n\n Please press OK to start the task. To exit, press cancel',
#icon='info',
#title='Welcome to breath sync task',
#default='ok')


#if MsgBox == True :
#
#    print("got here")

run_animation()
