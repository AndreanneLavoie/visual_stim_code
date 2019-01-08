#def calibration(win):
    
'''

This function will generate static grating will changing luminance (using log scale). 
This visual stim will be used to calibrate the eye tracking system.


'''
import numpy as np
from psychopy import event, visual, core 

from init_para import (MovSinGrat_Amp_sinu, MovSinGrat_GammaFactor, MovSinGrat_AmpFactor, MovSinGrat_contrast, MovSinGrat_MeanLum, win,
winWidth , winHeight, ScrnNum, PixelSize, winWidthofEachDisp, DisplayFrameWidth, FR, square1, square2, fontSize, fontClr, win, Local_IP, Local_Port, Remote_IP, Remote_Port)


#define parameters

white = MovSinGrat_AmpFactor*255**MovSinGrat_GammaFactor #check this
black =  0
gray = 20
stepgray = 15
Contrast = 1
inc = gray* Contrast #increase the step by this variable 

SpatFreqDeg = 0.1
MeanLum = (white + black)/2
WholeWinwidth = winWidth
WinWidthofEachdisp = winWidth/ScrnNum
phase = 0 #in radius 


#generating matrix that will be the place holder for every pixel 
pixelangle = np.empty(shape=[1, winWidth]) #pixel has to be 2D since the image is 2D
temp = np.array(range(winWidthofEachDisp)) 
temp.reshape(1,winWidthofEachDisp)# the temp must be 2D 
tempPixelAngle = np.degrees(np.arctan((temp - (winWidthofEachDisp/2.0))*PixelSize*(2.0/DisplayFrameWidth))) + 45 #calculating the pixel angle for first monitor

for i in range(ScrnNum):
    pixelangle[:,i*winWidthofEachDisp: (i + 1)*winWidthofEachDisp ] = tempPixelAngle + 90*i #taking specific ranges within the full winWidth and replacing the values with the corresponding angles

#creating the list that will hold all frames
texdata1D = []

#generating the pixel values for vertical stimulus 
texdata1DTmp = np.exp(np.log((gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase))/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)
pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1

#setting up the grating
DrawTexture = visual.GratingStim(
    win=win,
    size = [winWidth, winHeight],
    units = 'pix',
    tex=pixVal
    )

#display current lumninance value
lum_text = visual.TextBox(
    window=win,
    text=(str(gray)),
    font_size = fontSize,
    font_color=fontClr,
    pos=(-2690 ,475),
    size=(300,37),
    units='pix',
    grid_horz_justification='center',
    grid_vert_justification='center')

#draw grating and lum val
DrawTexture.draw()
lum_text.draw()

#flip window and display gratting and lum val
win.flip()

mouse = event.Mouse(
        visible = True, 
        win = win
        )

#display grating; and allow user to modify luminance of the grating according to right and left clic  
while True:
    core.wait(0.1)
    
    #get keys
    currMouse = mouse.getPressed()
    
     #clicking the middle button causes program to close
    if currMouse[1]:
        break
    
    #left clic: increase lum
    if currMouse[0]: 
        
        if gray + stepgray <= MeanLum:
            gray = gray + stepgray
        else: 
            gray = MeanLum
            
        #increase by increment value
        inc = gray*Contrast
        
        #regenerating the pixel values 
        texdata1DTmp = np.exp(np.log((gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase))/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)
        pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1
        
        #redraw texture and new lum val
        #setting up the grating
        DrawTexture = visual.GratingStim(
            win=win,
            size = [winWidth, winHeight],
            units = 'pix',
            tex=pixVal  
            )

        #display current lumninance value
        lum_text = visual.TextBox(
            window=win,
            text=(str(gray)),
            font_size = fontSize,
            font_color=fontClr,
            pos=(-2690 ,475),
            size=(300,37),
            units='pix',
            grid_horz_justification='center',
            grid_vert_justification='center')

        #draw grating and lum val
        DrawTexture.draw()
        lum_text.draw()

        #flip window and display gratting and lum val
        win.flip()
        
        while any(currMouse):
            currMouse = mouse.getPressed()
    
    if currMouse[2]: #right clic: decrease lum
        
        if gray - stepgray >= 0:
            gray = gray - stepgray
        else:
            gray = 0
        
        #increase by increment value
        inc = gray*Contrast
        
        #regenerating the pixel values from luminance val 
        texdata1DTmp = np.exp(np.log((gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase))/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)
        pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1
        
        
        #redraw texture and new lum val
        #setting up the grating
        DrawTexture = visual.GratingStim(
            win=win,
            size = [winWidth, winHeight],
            units = 'pix',
            tex=pixVal
            )

        #display current lumninance value
        lum_text = visual.TextBox(
            window=win,
            text=(str(gray)),
            font_size = fontSize,
            font_color=fontClr,
            pos=(-2690 ,475),
            size=(300,37),
            units='pix',
            grid_horz_justification='center',
            grid_vert_justification='center')

        #draw grating and lum val
        DrawTexture.draw()
        lum_text.draw()

        #flip window and display gratting and lum val
        win.flip()
        
        
        while any(currMouse):
            currMouse = mouse.getPressed()

while any(currMouse):
    currMouse = mouse.getPressed()
 
win.close()