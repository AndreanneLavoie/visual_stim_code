from psychopy import visual
from psychopy import event
from win32api import GetSystemMetrics
from init_para import *
import socket
import numpy as np
import psychopy.core
import conv

'''
Note: DO NOT RUN THIS PROGRAM, only modify parameters and save it from the drop down menu 
If you do, just wait and the program will exit on its own. This may take a while.

Any constant paramters which will not be changed by user in front.py 
'''

#UDP Parameters
Remote_IP = '142.1.199.39'
Remote_Port = 9092
Local_IP = '142.1.199.56'
Local_Port = 9093


#Monitor Patameters
winWidth = GetSystemMetrics(0) #0 refers to width in pixels   
winHeight = GetSystemMetrics(1)#1 refers to height in pixels 
ScrnNum = 3
DisplayFrameWidth = 620.0
Dispwidth = 597.7
DispHeight = 336.2
PixelSize = (Dispwidth*ScrnNum)/float(winWidth)
winWidthofEachDisp = int(winWidth/ScrnNum)
winHeightofEachDisp = int(winHeight/ScrnNum)
fullscrn = True
origin_x = -1
origin_y = 1


#Pixel values of overlayed mask
mask = np.zeros((1,winWidth))
maskArea = 0.33 #area of stimulation to be displayed where 1 refers to 100% and 0 refers to 0%

for i in range(winWidth):
    
    if i < (maskArea*0.5*winWidth):
        mask[0,i] = -1
    
    elif i > (winWidth - maskArea*0.5*winWidth):
        mask[0,i] = -1
    
    else:
        mask[0,i] = 1
        

#directional grating parameters
directionalGrating_picBreak = 0 #location of the break for the grating. If 0.5 then the break will be in the middle, 0 refers to left side and 1 refers to right side
directionalGrating_convergence = 1 #convergence or divergence of grating. 1 refers to converging and 0 refers to diverging 
directionalGrating_rotate = 0 #if 0 then the barrel will appear to rotate clockwise and if 1 then the barrel will rotate counter clockwise
    


#drumgrating parameters that cannot be changed from front.py
drumgrating_addblank = 0 #if 1 a blank screen will appear during t_before and t_after, if 0 the first and last frame will appear for t_before and t_after respectively; if 2, continue the motion
drumgrating_Amp_sinu = 3 #amplitude of the gradient movement for motionmode = 0
drumgrating_controlmod = 'autoVS'
drumgrating_dirindex = 0 #this is the direction of movement for motionmode = 1 (note: this has not been implemented yet)
drumgrating_Ori = 1
drumgrating_parasize = 800 #number of repeats the stimulation will undergo
drumgrating_t_triginit = 1000
drumgrating_GammaFactor = 2.251
drumgrating_AmpFactor = 0.0007181
drumgrating_contrast = 1
drumgrating_MeanLum = 55

#drumgrating parameters that can be changed from front.py
drumgrating_Motionmode = 1 #0 refers to linear motion and 1 refers to sinusoidal motion
drumgrating_SpatFreqVal = 0.1
drumgrating_tempFreqVal = 1
drumgrating_t_beforeVal = 1000
drumgrating_t_DuringVal = 5000
drumgrating_t_afterVal = 1000
drumgrating_syncVal = False #change NAME


#MovSinGrat parameters that cannot be changed from front.py
MovSinGrat_addblank = 1 #if 0 a blank screen will appear during t_before and t_after, if 1 the first and last frame will appear for t_before and t_after respectively
MovSinGrat_Amp_sinu = 3 #amplitude of the gradient movement for motionmode = 0
MovSinGrat_controlmod = 'autoVS'
MovSinGrat_dirindex = 0 #this is the direction of movement for motionmode = 1 (note: this has not been implemented yet)
MovSinGrat_Ori = 1
MovSinGrat_parasize = 800 #number of repeats the stimulation will undergo
MovSinGrat_t_triginit = 1000
MovSinGrat_GammaFactor = 2.251
MovSinGrat_AmpFactor = 0.0007181
MovSinGrat_contrast = 0.8
MovSinGrat_MeanLum = 35
MovSinGrat_location = None

#Define function For MovSinGrat in order to import tuning features and feature values from text file into list format:
#For this to work, need to have run MovSinGrat_tuning_text_files_gen.py, which will create all txt files required to run stim
def text2list(fileName):
    """
    Convert text file to list. One item per line. 
    """
    with open(fileName + '.txt') as f:
        list = f.read().split('\n')
    list = list[:-1] #remove empty element ' ' that is accidently created
    return list

#for tuning features:
feature_list = text2list('tuning_feature_list')
#Dictionary containing all tuning features with corresponding numberical vale
MovSinGrat_features_dict = {feature:feature_list.index(feature) for feature in feature_list} # ori = 0, spat_freq = 1, temp_freq = 2, contrast = 3, location = 4

#create list of values for different tuning features:
MovSinGrat_angles_list = text2list('angles_list')
MovSinGrat_spat_list = text2list('spat_freq')
MovSinGrat_temp_lin_list = text2list('temp_freq_lin')
MovSinGrat_temp_osc_list = text2list('temp_freq_osc')
MovSinGrat_location_list = text2list('location_list')
MovSinGrat_contrast_list = text2list('contrast_list')


#MovSinGrat parameters that can be changed from front.py
MovSinGrat_Motionmode = 1 #0 refers to linear motion and 1 refers to sinusoidal motion
MovSinGrat_SpatFreqVal = 0.1
MovSinGrat_tempFreqVal = 1
MovSinGrat_t_beforeVal = 1000
MovSinGrat_t_stimVal = 5000
MovSinGrat_t_afterVal = 1000
MovSinGrat_contrast = 1
MovSinGrat_ori = 0
MovSinGrat_syncVal = False

#MovSinGrat for changing orientation parameters
MovSinGrat_Rep = 50
MovSinGrat_localflag = 0
MovSinGrat_ledstate = 1
MovSinGrat_randomseq = 1
MovSinGrat_angle0 = 0
MovSinGrat_angle1 = 330
MovSinGrat_DirNum = 4
MovSinGrat_angles = np.linspace(MovSinGrat_angle0,MovSinGrat_angle1,MovSinGrat_DirNum)
MovSinGrat_num_angles = range(0,len(MovSinGrat_angles))
MovSinGrat_features = int(MovSinGrat_features_dict['ori'])
ani_distance = DisplayFrameWidth*0.5
MovSinGrat_t_triginit = 1000
loop = 12
#To display vs on a single screen set one_screen = True:
one_screen = True 


#creating the window
winClr = 2*(np.exp(np.log(drumgrating_MeanLum/drumgrating_AmpFactor)/drumgrating_GammaFactor)/255.0) -1
win=visual.Window(fullscr=fullscrn,
    units = 'norm', 
    color = winClr
    )
FR = win.getActualFrameRate() #getting the frame rate from the monitors (NOTE: if running in fllscr = False mode for the window, the fps will be 30. if running in fullscr = True mode, the fps will be 60)


#texbox parameters
fontSize = 11
fontClr = [0.5, 0.5, 0.5]
boarderClr = [0.5, 0.5, 0.5]
front_textbox_size = (0.16/ScrnNum,0.1)
front_button_size = ((-0.5*front_textbox_size[0], -0.5*front_textbox_size[1]), (-0.5*front_textbox_size[0], 0.5*front_textbox_size[1]), 
                    (0.5*front_textbox_size[0], 0.5*front_textbox_size[1]), (0.5*front_textbox_size[0], -0.5*front_textbox_size[1]))
button_init_y = 0.04
button_spacing = 0.02


#setting the vertices for the squares in the bottom left corner
sqrHeight = 30.0/winHeight
sqrWidth = 30.0/winWidth
squareShape = np.array(([-sqrWidth, -sqrHeight], [-sqrWidth, sqrHeight], [sqrWidth, sqrHeight], [sqrWidth, -sqrHeight]))
#reshaping the array into a 4 by 2 matrix
squareShape.reshape(4, 2)

square1_Pos = (origin_x + sqrWidth, origin_y - 2 + sqrHeight)
square2_Pos = (origin_x + sqrWidth, origin_y - 2 + 3*sqrHeight) #the 3* is there to place the second square ontop of the first 

#setting up the squares at the bottom left corner
#Trigger signal
square1 = psychopy.visual.ShapeStim(
    win = win, 
    units = "norm",
    pos = square1_Pos,
    fillColor = [-1, -1, -1],
    vertices = squareShape, 
    lineWidth = 0
    )

#Duration of visual stimulation
square2 = psychopy.visual.ShapeStim(
    win = win, 
    units = "norm",
    pos = square2_Pos, 
    fillColor = [-1, -1, -1],
    vertices = squareShape, 
    lineWidth = 0)
    
#mask parameters
mask_L_shape = np.array(([-1, 1],[-1.0/3, 1],[-1.0/3, -1], [-1, -1]))
mask_R_shape = np.array(([1.0/3, 1],[1,1],[1, -1], [1.0/3, -1]))

mask_L_shape.reshape(4, 2)
mask_R_shape.reshape(4, 2)

mask_L_pos= (0, 0)
mask_R_pos= (0, 0)

#Draw mask for tuning code when running on single screen (block R and L screens)

mask_L = psychopy.visual.ShapeStim(
    win = win, 
    units = "norm",
    pos = mask_L_pos,
    fillColor = winClr,
    vertices = mask_L_shape, 
    lineWidth = 0
    )

mask_R = psychopy.visual.ShapeStim(
    win = win, 
    units = "norm",
    pos = mask_R_pos,
    fillColor = winClr,
    vertices = mask_R_shape, 
    lineWidth = 0
    )
