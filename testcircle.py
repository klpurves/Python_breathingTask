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
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

# add title
plt.title("breathe and click")

# remove background
fig.patch.set_visible(False)
ax.axis('off')

# ----------------------------------------------------------------------------
# Set up options and animate function to apply these on repeat
rect = patches.Rectangle((0.47, 0.45, 0.1, 0.075),2,2,linewidth=1,edgecolor='r',facecolor='none')

contour_opts = {'levels': np.linspace(-9, 9, 10), 'cmap':'RdBu'}
cax = ax.contour(x, y, G[..., 0], **contour_opts)

def animate(i):
    print(i)
    if i < 10:
        plt.pause(2)
        axwait = plt.axes([0.47, 0.45, 0.1, 0.075])
        bwait = Button(axwait, 'Wait',
        color = "grey", hovercolor = "#489FA7")
        ax.collections = []
        ax.contour(x, y, G[..., i], **contour_opts)
    else:
        bwait.remove()
        axplay = plt.axes([0.47, 0.45, 0.1, 0.075])
        bplay = Button(axplay, 'Press',
        color = "grey", hovercolor = "#489FA7")
        ax.collections = []
        ax.contour(x, y, G[..., i], **contour_opts)




# ----------------------------------------------------------------------------
# Set up dictionary to hold data

timedata = {}

# Set up count variable to get number of clicks
count = 0


## set up animation function including play/pause

def run_animation():

    anim_running = True

    def onClick(event):
        global count
        count += 1
        current_datetime = datetime.now() # NOTE: Acquire the date time (to ms) on each click
        date = current_datetime.strftime('%Y-%m-%d')
        time = current_datetime.time().strftime('%H:%M:%S.%f')
        timedata[count] = date, time
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True

    fig.canvas.mpl_connect('button_press_event', onClick)

    anim = FuncAnimation(fig, animate, interval=200, frames=len(t)-1, repeat=True)

    plt.show()

    # write the dictionary to csv
    with open('test_time.csv', 'w') as f:
        f.write("{0},{1},{2}\n".format("ClickCount","Date","Time"))
        for key in timedata.keys():
            values = timedata[key]

            f.write("{0},{1},{2}\n".format(key,values[0],values[1]))

run_animation()
