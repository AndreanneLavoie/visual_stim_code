def rf6x8(win):

    from psychopy import visual, event, clock, gui
    from win32api import GetSystemMetrics
    from datetime import datetime

    from init_para import (MovSinGrat_addblank, MovSinGrat_Amp_sinu, MovSinGrat_controlmod, MovSinGrat_dirindex, MovSinGrat_ori, 
    MovSinGrat_t_triginit, MovSinGrat_GammaFactor, MovSinGrat_AmpFactor, MovSinGrat_contrast, MovSinGrat_MeanLum,
    winWidth , winHeight, ScrnNum, PixelSize, winWidthofEachDisp, DisplayFrameWidth, FR, square1, square2, fontSize, fontClr, win, ani_distance)

    import socket
    import numpy as np
    import conv


    #PARAMETERS

    #stim time parameters
    t_before = 1000
    t_during = 3000
    t_after = 1000

    #contrast (stim colour) parameters
    meanLum = 55
    minLum = 0
    maxLum = meanLum * 2
    gammaFactor = 2.251
    ampFactor = 0.0007181
    
    winClr = 2*(np.exp(np.log(meanLum/ampFactor)/gammaFactor)/255.0) -1  #colour of background (in pix val)
    white = 2*(np.exp(np.log(maxLum/ampFactor)/gammaFactor)/255.0) -1 #convert maxLum into pix value
    black =  -1

    #stim order parameters
    repetition = 2
    num_dif_stim = 48*2 #number of location the stimulus (6 x 8 = 48) will be displayed in two colours values with 100% contrast => 48*2 = 96
    tot_num_stim = repetition * num_dif_stim #total number of stiumuli that will be displayed in one experiment 

    index = range(num_dif_stim) #number 0-95 representing each location in 6 x 8 screen and black or white colour
    x_pos = ([0]*6 + [1]*6 +[2]*6 +[3]*6 +[4]*6 +[5]*6 +[6]*6 +[7]*6) * 2  #list of all possible x-coordinate for stim
    y_pos = range(6)*8*2  #list of all possible y-coordinate for stim
    colour_list = [white]*48 + [black]*48 

    #reshape data into numpy array
    x_pos = np.asarray(x_pos)
    y_pos = np.asarray(y_pos)
    colour_list = np.asarray(colour_list)

    #creating a matrix to store all stim ID (index), position and colour information
    loc_order = np.ones((96,3), dtype=int)
    colour_order = np.ones((96,1), dtype=float)
    
    loc_order[:,0] = index
    loc_order[:,1] = x_pos
    loc_order[:,2] = y_pos
    colour_order[:,0] = colour_list
    
    stim_order = np.concatenate((loc_order, colour_order),axis=1)

    #create ramdom order for stimuli presentation
    np.random.shuffle(index) #this function automatically shuffles the input (no need to assign a new var)


    #stim shape parameters
    tot_stim = 96
    stim_vertices = np.array(([-1./3, 1],[-1./4, 1], [-1./4, 2./3], [-1.0/3, 2./3]))
    stim_vertices.reshape(4, 2) #reshape to fit psychopy texture requirements 


    #creating visual stimulation display functionality 

    #creating mouse functionality
    mouse = event.Mouse(
        visible = True, 
        win = win
        )
        
    #Naming the experiment to create fileName (at the end of this function)
    instruction_text = visual.TextStim(win, text = u'Name experiment and press enter to start.', pos=(0, 0.5))
    answer_text = visual.TextStim(win)

    #show instructions
    win.color = winClr
    instruction_text.draw()
    square1.draw()  #have to draw trigger squ; otherwise transient white will happen$$$$$$$$$$$$$$$
    square2.draw()
    win.flip()

    #get users input for experiment name
    now = True
    answer_text.text = ''
    while now:
        key = event.waitKeys()[0]
        # Add a new number
        if key in '1234567890abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-':
            answer_text.text += key

        # Delete last character, if there are any chars at all
        elif key == 'backspace' and len(answer_text.text) > 0:
            answer_text.text = answer_text.text[:-1]

        # Stop collecting response and return it
        elif key == 'return':
            expName = answer_text.text
            print ('expName IN here: ', expName)
            now = False
        
        # Show current answer state
        instruction_text.draw()
        answer_text.draw()
        square1.draw()  #have to draw trigger squ; otherwise transient white will happen$$$$$$$$$$$$$
        square2.draw()
        win.flip()
            
    #setting name of file which will be used to save order of vs stim displayed; 
    date = datetime.today().strftime('%Y%m%d_%H%M%S') #extract today's date
    fileName = expName + '_vs_Rf6x8' + date  



    #loop over each stim and display it
    for rep in range(len(index)*repetition):  #will loop around for total Repetitions (96*repetition)
        
        tic = clock.getTime()
        
        stim_ind = rep % len(index)  #give a number between 0 and 95 which represents each stimuli, allowing to continuouly loop around for total repetitions
        
        #assign postion of stimulus
        i, j = stim_order[index[stim_ind]][1], stim_order[index[stim_ind]][2]
        #assing colour of stimulus
        colour = stim_order[index[stim_ind]][3]
        
        #Create stimulus with changing : a single rect with x = screenwdth/8 and y = screenheight/6
        stim = visual.ShapeStim(
            win = win, 
            units = "norm",
            pos = (i * (1.0/12.0) , j * (-1.0/3.0)),  #moves the stim by 1/9th to the right and 1/4th down (relative to screen size); if (i,j) = (0,0); display middle screen @ top left corner
            fillColor = colour,
            vertices = stim_vertices, 
            lineWidth = 0
            )
        
        #save vs data in .csv format
        #create a temp list variable that stores array values that will be appended
        save_row = stim_order[index[stim_ind]].tolist()
        
        #open and append values to new file
        with open(fileName + '.csv', 'a') as f: 
            
            for i in range(len(save_row)):
                
                f.write(str(save_row[i]) + ',')
            
            f.write('\n')
        
        #Display stimulation using a series of while loops 
        win.color = winClr
        square1.draw()
        square2.draw()
        win.flip()

        #time before the stimulation
        toc = clock.getTime() - tic
        
        while toc < (t_before/1000.0):
            
            toc = clock.getTime() - tic 
            
            #this if statement is for existing the stimulation
            if mouse.getPressed()[1]:
                return
            
            #display trigger squares 
            square1.draw()
            square2.draw()
            win.flip()
            
        #t_triger initial timing for triggerin the camera
        for i in range(int(FR*MovSinGrat_t_triginit/1000.0)):
            
            if mouse.getPressed()[1]:
                return
                
            if i < 3:
                square1.fillColor = [1,1,1]
                square2.fillColor = [-1,-1,-1]
            
            else:
                square1.fillColor = [-1,-1,-1]
                square2.fillColor = [-1,-1,-1]
                
            win.color = winClr
            square1.draw()
            square2.draw()
            win.flip()
            
        #making the top square white
        square1.fillColor = [-1,-1,-1]
        square2.fillColor = [1,1,1]
        
        
        #drawing the stimulus on the window
        for frm in range(int(FR*t_during/1000.0)):
            
            if mouse.getPressed()[1]:
                return
            
            stim.draw()
            
            square1.draw()
            square2.draw()
            win.flip()
            
        #changing the characteristics of the two squares at the bottom left corner
        square1.fillColor = [-1,-1,-1]
        square2.fillColor = [-1,-1,-1]
            
        #time after the stimulation
        for toc in range(int(t_after*FR/1000.0)):
            
            #win.color = winClr
            
            square1.draw()
            square2.draw()
            win.flip()
