def movSinGrat(MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, Synch, MovSinGrat_Motionmode, MovSinGrat_features, MovSinGrat_ledstate):
    ''' 
    INPUT: paramterS that are potentially changed by user in front.py by clicking buttons on the UI
    
    OUTPUT: vs stimuli for tuning, depending on the feature selected; default is 'ori' which can be changed in init_para.py;
    
    Note >> TUNING FEATURE VALUES are defined as follows:  # ori = 0, spat_freq = 1, temp_freq = 2, contrast = 3, location = 4

    
    '''
    
    from psychopy import visual, event, clock, gui
    from win32api import GetSystemMetrics
    from datetime import datetime

    from init_para import (MovSinGrat_addblank, MovSinGrat_Amp_sinu, MovSinGrat_controlmod, MovSinGrat_dirindex, MovSinGrat_ori, 
    MovSinGrat_t_triginit, MovSinGrat_GammaFactor, MovSinGrat_AmpFactor, MovSinGrat_contrast, MovSinGrat_MeanLum, win,
    winWidth , winHeight, ScrnNum, PixelSize, winWidthofEachDisp, DisplayFrameWidth, FR, square1, square2, fontSize, fontClr, win, Local_IP, Local_Port, Remote_IP, Remote_Port, ani_distance,
    MovSinGrat_Rep, MovSinGrat_randomseq, MovSinGrat_features_dict, MovSinGrat_angles_list, MovSinGrat_temp_lin_list, MovSinGrat_temp_osc_list, MovSinGrat_location_list, MovSinGrat_contrast_list)
    
    import socket
    import numpy as np
    import conv
    
    
    #creating mouse functionality
    mouse = event.Mouse(
        visible = True, 
        win = win
        )
    if Synch:
        
        #creating the socket in which communications will take place
        sock = socket.socket(
            socket.AF_INET, 
            socket.SOCK_DGRAM
        )
        
        #binding the local IP address and local port 
        sock.bind((Local_IP, Local_Port))
        
        #creating textbox showing that this VS computer is waiting for UDP signal
        standBy= visual.TextBox(
            window=win,
            text=("Waiting for starting the control computer."),
            font_size = fontSize,
            font_color=fontClr,
            pos=(-2690 ,475),
            size=(300,37),
            units='pix',
            grid_horz_justification='center',
            grid_vert_justification='center')
        
        standBy.draw()
        square1.draw() #have to draw trigger squ; otherwise transient white will happen
        square2.draw()
        win.flip()
        
        try:
            #wait for the command 'gammacorrection'
            info = sock.recv(1024)
        except Exception:
            sock.close()
            print("Did not recieve info, connection timeout.")
            return
            
        
        #sending 'gammafloatampfloat' to the second PC
        sock.sendto(("gamma" + str(drumgrating_GammaFactor) + "amp" + str(drumgrating_AmpFactor)), (Remote_IP, Remote_Port))
        
        #creating textbox showing that this VS computer is waiting for UDP signal
        standBy= visual.TextBox(
            window=win,
            text=("Control Computer is Ready."),
            font_size = fontSize,
            font_color=fontClr,
            pos=(-2690 ,475),
            size=(300,37),
            units='pix',
            grid_horz_justification='center',
            grid_vert_justification='center')
        standBy.draw()
        
        try:
            #waiting for the signal autoVs
            drumgrating_controlmod = sock.recv(1024)
        except Exception:
            sock.close()
            print("Did not recieve drumgrating_controlmod, connection timeout.")
            return
        
        #sending 'Wait for parameters' to the second PC
        sock.sendto("Wait for parameters", (Remote_IP, Remote_Port))
        
        if MovSinGrat_controlmod == 'autoVS':
            
            try:
                drumgrating_parasize = sock.recv(1024)
            except Exception:
                sock.close()
                print("Did not recieve parasize, connection timeout.")
                return
            
            #sending a completion transcript
            sock.sendto("read parasize", (Remote_IP, Remote_Port))
            
            #converting the string recieved into int
            drumgrating_parasize = conv.deleteParasize(drumgrating_parasize)
            
            #making the array in which the parameters will be added to
            paras = np.empty(shape=[drumgrating_parasize, 9])
            
            #adding the parameters to the array
            
            #this for loop receives the 9 parameters for all the stimulations and adds them to an array
            for i in range(drumgrating_parasize): #start from 0 to parasize[0] - 1
                temp = sock.recv(1024)
                temp =conv.convStr2Dig(temp)
                #adding the parameters to the array (temp) at position index
                #paras[i, :] = temp
            
            sock.sendto("Para DONE", (Remote_IP, Remote_Port))
            
            try:
                #recieving all orientation for stimuli 1 for veritcal, 0 for horizontal
                paratemp = sock.recv(1024)
            except Exception:
                sock.close()
                print("Did not recieve message, connection timeout.")
                return
            
            paratemp = conv.convStr2Dig(paratemp)
            
            #setting up the parameters based on what was send in the paras variable
            drumgrating_Ori = int(paratemp[0])
            Motionmode = int(paratemp[1])
            drumgrating_Amp_sinu = paratemp[2]
            drumgrating_addblank = paratemp[3]
            
            sock.sendto("Para DONE", (Remote_IP, Remote_Port))
            
            
            #creating generalized sequence of randomely shuffled stimuli for tuning, given a particular feature 
            
            #This firt if loop will create two varialbes: 
            #tuning_stim_val and tuning_stim_ind which contains all unique stimulus and corresponding index, respectively, given the tuning feature selected.
            if MovSinGrat_features == 0: #ori
                
                tuning_stim_val = map(float, MovSinGrat_angles_list) #map applies the float() function to all elements of the list, therefore converting strings to float
                tuning_stim_ind = range(len(tuning_stim_val))
                
            elif MovSinGrat_features == 1: #spat_freq
                 
                tuning_stim_val = map(float, MovSinGrat_spat_list)
                tuning_stim_ind = range(len(tuning_stim_val))
                
            elif MovSinGrat_features == 2: #temp_freq
                
                #assign temp freq depending on Motionmode (lin vs osc motion)
                if MovSinGrat_Motionmode == 0:
                    tuning_stim_val = map(float, MovSinGrat_temp_lin_list) #SHOULD THIS BE DEPENDENT ON MOTIONMODE???
                    tuning_stim_ind = range(len(tuning_stim_val))
                else: 
                    tuning_stim_val = map(float, MovSinGrat_temp_osc_list) #SHOULD THIS BE DEPENDENT ON MOTIONMODE???
                    tuning_stim_ind = range(len(tuning_stim_val))
                    
            elif MovSinGrat_features == 3: #contrast
                tuning_stim_val = MovSinGrat_contrast_list #HAS NOT BEEN CREATED IN INIT_PARA YET; 
                tuning_stim_ind = range(len(tuning_stim_val))
                
            elif MovSinGrat_features == 4: #location
                
                tuning_stim_val = map(float, MovSinGrat_location_list) 
                tuning_stim_ind = range(len(tuning_stim_val))
                
            else:
                print 'ERROR: MovSinGrat_features outside range. Tuning Feature Value must an integer be between 0 and 4.'
                
            
            #calculating total number of stimuli that will be presented (based on number of repetitions for each stimulus*ledstate combo)
            tot_num_stim = MovSinGrat_Rep*MovSinGrat_ledstate*len(tuning_stim_ind)
            
            #defining the variable and array shape in which the parameters will be added to; each column will represent on parameter (spat_freq, temp_freq, stimId etc.) for each presented stimulus (row)
            paras = np.empty(shape=[tot_num_stim, 11])
            
            #adding the parameters to the array
            # Generating sequence of order of presenting stimID that will ONLY change the TUNING FEATURE PARAMETER of the stimulus:
            for repind in xrange(MovSinGrat_Rep): 
                
                stimId = np.empty(len(tuning_stim_ind)*MovSinGrat_ledstate)
                stimId = map(int, stimId)
                
                if MovSinGrat_randomseq:
                    
                    for iled in xrange(0,MovSinGrat_ledstate): #for each ledstate, one of each angle will be assoign in random order
                        np.random.shuffle(tuning_stim_ind)
                        
                        for n in xrange(iled,len(stimId),MovSinGrat_ledstate): #assign tuning_stim_ind elements to stimId by hops of size ledstate (if ledstate = 1), stimId = tuning_stim_ind;
                            stimId[n] = tuning_stim_ind[n/MovSinGrat_ledstate] #
                                    
                else:
                    for iled in xrange(0,MovSinGrat_ledstate): 
                                               
                        for n in xrange(iled,len(stimId),MovSinGrat_ledstate):
                            stimId[n] = tuning_stim_ind[n/MovSinGrat_ledstate]
                    
                    
                #adding the parameters as an array at index i
                for localstimid in xrange(0,(len(stimId))):
                
                    if MovSinGrat_features == 0: #0 = ori
                        paras[repind*(len(stimId))+localstimid, :] = [MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                        MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, tuning_stim_val[stimId[localstimid]], MovSinGrat_ledstate] # ADD LOCATION 
                    
                    elif MovSinGrat_features == 1 : #1 = spat
                        paras[repind*(len(stimId))+localstimid, :] = [tuning_stim_val[stimId[localstimid]], MovSinGrat_tempFreqVal, MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                        MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
                        
                    elif MovSinGrat_features == 2: # and movSinGrat_motionMode == 0: #2 = TempFreq
                        paras[repind*(len(stimId))+localstimid, :] = [MovSinGrat_SpatFreqVal, tuning_stim_val[stimId[localstimid]], MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                        MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
                                            
                    elif MovSinGrat_features == 3: #3 = contrast
                        paras[repind*(len(stimId))+localstimid, :] = [ MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, tuning_stim_val[stimId[localstimid]], MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                        MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
                    
                    #elif MovSinGrat_features == 4: #4 = location
                    #    paras[repind*(len(stimId))+localstimid, :] = [MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                    #    MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
            
            paratemp = [drumgrating_Ori, Motionmode, drumgrating_Amp_sinu, drumgrating_addblank] 
        
            #setting up the parameters based on what was send in the paras variable
            drumgrating_Ori = int(paratemp[0])
            Motionmode = int(paratemp[1])
            drumgrating_Amp_sinu = paratemp[2]
            drumgrating_addblank = paratemp[3]
                
            
        elif MovSinGrat_controlmod == 'manualVS':
            return
    
    #if Synch is False, this else condition will make the parameters in the same format as if Synch was True
    else:
        
        #Naming the experiment to create fileName (at the end of this function)
        instruction_text = visual.TextStim(win, text = u'Name experiment and press enter to start.', pos=(0, 0.5))
        answer_text = visual.TextStim(win)

        #show instructions
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
        
        print ('expName up here: ', expName)
        #creating generalized sequence of randomely shuffled stimuli for tuning, given a particular feature 
        
        #This firt if loop will create two varialbes: 
        #tuning_stim_val and tuning_stim_ind which contains all unique stimulus and corresponding index, respectively, given the tuning feature selected.
        if MovSinGrat_features == 0: #ori
            
            tuning_stim_val = map(float, MovSinGrat_angles_list) #map applies the float() function to all elements of the list, therefore converting strings to float
            tuning_stim_ind = range(len(tuning_stim_val))
            
        elif MovSinGrat_features == 1: #spat_freq
             
            tuning_stim_val = map(float, MovSinGrat_spat_list)
            tuning_stim_ind = range(len(tuning_stim_val))
            
        elif MovSinGrat_features == 2: #temp_freq
            
            #assign temp freq depending on Motionmode (lin vs osc motion)
            if MovSinGrat_Motionmode == 0:
                tuning_stim_val = map(float, MovSinGrat_temp_lin_list) 
                tuning_stim_ind = range(len(tuning_stim_val))
            else: 
                tuning_stim_val = map(float, MovSinGrat_temp_osc_list)
                tuning_stim_ind = range(len(tuning_stim_val))
                
        elif MovSinGrat_features == 3: #contrast
        
            tuning_stim_val = MovSinGrat_contrast_list 
            tuning_stim_ind = range(len(tuning_stim_val))
            
        elif MovSinGrat_features == 4: #location
            
            tuning_stim_val = map(float, MovSinGrat_location_list) 
            tuning_stim_ind = range(len(tuning_stim_val))
            
        else:
            print 'ERROR: MovSinGrat_features outside range. Tuning Feature Value must an integer be between 0 and 4.'
            
        
        #calculating total number of stimuli that will be presented (based on number of repetitions for each stimulus*ledstate combo)
        tot_num_stim = MovSinGrat_Rep*MovSinGrat_ledstate*len(tuning_stim_ind)
        
        #defining the variable and array shape in which the parameters will be added to; each column will represent on parameter (spat_freq, temp_freq, stimId etc.) for each presented stimulus (row)
        paras = np.empty(shape=[tot_num_stim, 11])
        
        #adding the parameters to the array
        # Generating sequence of order of presenting stimID that will ONLY change the TUNING FEATURE PARAMETER of the stimulus:
        for repind in xrange(MovSinGrat_Rep): 
            
            stimId = np.empty(len(tuning_stim_ind)*MovSinGrat_ledstate)
            stimId = map(int, stimId)
            
            if MovSinGrat_randomseq:
                
                for iled in xrange(0,MovSinGrat_ledstate): #for each ledstate, one of each angle will be assoign in random order
                    np.random.shuffle(tuning_stim_ind)
                    
                    for n in xrange(iled,len(stimId),MovSinGrat_ledstate): #assign tuning_stim_ind elements to stimId by hops of size ledstate (if ledstate = 1), stimId = tuning_stim_ind;
                        stimId[n] = tuning_stim_ind[n/MovSinGrat_ledstate] 
                                
            else:
                for iled in xrange(0,MovSinGrat_ledstate): 
                                           
                    for n in xrange(iled,len(stimId),MovSinGrat_ledstate):
                        stimId[n] = tuning_stim_ind[n/MovSinGrat_ledstate]
                
                
            #adding the parameters as an array at index i
            for localstimid in xrange(0,(len(stimId))):
            
                if MovSinGrat_features == 0: #0 = ori
                    paras[repind*(len(stimId))+localstimid, :] = [MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                    MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, tuning_stim_val[stimId[localstimid]], MovSinGrat_ledstate] # ADD LOCATION 
                
                elif MovSinGrat_features == 1 : #1 = spat
                    paras[repind*(len(stimId))+localstimid, :] = [tuning_stim_val[stimId[localstimid]], MovSinGrat_tempFreqVal, MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                    MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
                    
                elif MovSinGrat_features == 2: # and movSinGrat_motionMode == 0: #2 = TempFreq
                    paras[repind*(len(stimId))+localstimid, :] = [MovSinGrat_SpatFreqVal, tuning_stim_val[stimId[localstimid]], MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                    MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
                                        
                elif MovSinGrat_features == 4: #4 = contrast
                    paras[repind*(len(stimId))+localstimid, :] = [ MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, tuning_stim_val[stimId[localstimid]], MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                    MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
                
                #elif MovSinGrat_features == 5: #5 = location
                #    paras[repind*(len(stimId))+localstimid, :] = [MovSinGrat_SpatFreqVal, MovSinGrat_tempFreqVal, MovSinGrat_contrast, MovSinGrat_MeanLum, MovSinGrat_dirindex, 
                #    MovSinGrat_t_before, MovSinGrat_t_During, MovSinGrat_t_after, MovSinGrat_t_triginit, MovSinGrat_ori, MovSinGrat_ledstate] #ADD LOCATION 
        
        #paratemp = [drumgrating_Ori, Motionmode, drumgrating_Amp_sinu, drumgrating_addblank]
        
        #setting up the parameters based on what was send in the paras variable
        #drumgrating_Ori = int(paratemp[0])
        #Motionmode = int(paratemp[1])
        #drumgrating_Amp_sinu = paratemp[2]
        #drumgrating_addblank = paratemp[3]
        
    if Synch:
        
        #waiting for "STR"
        while True:
            try:
                info = sock.recv(1024)
            except:
                pass
            if info == "STR":
                sock.sendto(("VS is running"), (Remote_IP, Remote_Port))
                break
            if mouse.getPressed()[1]:
                sock.close()
                return
    
    #generating the pixel angles relaive to the mouse position based on the orientation of the stimulus
    #generating matrix that will be the place holder for every pixel 
    pixelangle = np.empty(shape=[1, winWidth]) #pixel has to be 2D since the image is 2D
    temp = np.array(range(winWidthofEachDisp)) 
    temp.reshape(1,winWidthofEachDisp)# the temp must be 2D 
    #tempPixelAngle = np.degrees(np.arctan((temp - (winWidthofEachDisp/2.0))*PixelSize*(2.0/DisplayFrameWidth))) + 45 #calculating the pixel angle for first monitor
    spatangperpix = np.degrees(np.arctan(PixelSize/ani_distance))
    tempPixelAngle = spatangperpix*temp
    
    for i in range(ScrnNum):
        pixelangle[:,i*winWidthofEachDisp: (i + 1)*winWidthofEachDisp ] = tempPixelAngle + 90*i #taking specific ranges within the full winWidth and replacing the values with the corresponding angles
    
    
    #Genereating the VS based on the parameters in paras 
    for m in xrange(tot_num_stim):
        
        tic = clock.getTime()
        
        if m == 0:
            SpatFreqDeg = paras[m, 0]
            TempFreq = paras[m, 1]
            contrast = paras[m, 2]
            MeanLum = paras[m, 3]
            dirindex = paras[m, 4]
            t_before = paras[m, 5]
            t_During = paras[m, 6]
            t_after = paras[m, 7]
            t_triginit = paras[m, 8]
            orientation = paras[m, 9]
            ledstate = paras[m, 10]
            
            pixelformeanlum = 2*(np.exp(np.log(MovSinGrat_MeanLum/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)/255.0) -1
            MovSinGrat_gray = MovSinGrat_MeanLum
            inc = MovSinGrat_gray*MovSinGrat_contrast
            
            #frames to be calculated per period
            frames = round(FR/TempFreq)
            
            phase = np.array(range(int(frames)))
            
            if MovSinGrat_Motionmode == 1:
                phase = (phase/float(round(frames)))*(2.0*np.pi)
            
            elif MovSinGrat_Motionmode == 0:
                phase = MovSinGrat_Amp_sinu*np.sin((phase/frames)*2*np.pi)*SpatFreqDeg*2*np.pi
            
            #generating the pixel values for the stimulus  
                
            #creating the list that will hold all frames
            texdata1D = []
            
            #generating the pixel values for vertical stimulus
            for i in range(int(frames)):
                texdata1DTmp = np.exp(np.log((MovSinGrat_gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase[i]))/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)
                pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1
                texdata1D.append(pixVal)
        
        
        else:               
            if sum(abs(paras[m, :] - paras[m-1, :])) > 1e-7:
            #if (not all([v == 0  for v in abs(paras[m, :] - paras[m-1, :])])):
                
                SpatFreqDeg = paras[m, 0]
                TempFreq = paras[m, 1]
                MovSinGrat_contrast = paras[m, 2]
                MovSinGrat_MeanLum = paras[m, 3]
                MovSinGrat_dirindex = paras[m, 4]
                t_before = paras[m, 5]
                t_During = paras[m, 6]
                t_afterVal = paras[m, 7]
                MovSinGrat_t_triginit = paras[m, 8]
                orientation = paras[m, 9]
                ledstate = paras[m, 10]
                
                pixelformeanlum = 2*(np.exp(np.log(MovSinGrat_MeanLum/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)/255.0) -1
                MovSinGrat_gray = MovSinGrat_MeanLum
                inc = MovSinGrat_gray*MovSinGrat_contrast
                
                #frames to be calculated per period
                frames = round(FR/TempFreq)
                
            
            phase = np.array(range(int(frames)))
            
            if MovSinGrat_Motionmode == 1:
                phase = (phase/float(round(frames)))*(2.0*np.pi)
            
            elif MovSinGrat_Motionmode == 0:
                phase = MovSinGrat_Amp_sinu*np.sin((phase/frames)*2*np.pi)*SpatFreqDeg*2*np.pi
            
            
            
            #generating the pixel values for the stimulus 
                
            #creating the list that will hold all frames
            texdata1D = []
            
            #generating the pixel values for vertical stimulus
            for i in range(int(frames)):
                texdata1DTmp = np.exp(np.log((MovSinGrat_gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase[i]))/MovSinGrat_AmpFactor)/MovSinGrat_GammaFactor)
                pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1
                texdata1D.append(pixVal)
        
        #creating the looping variable for the simulation depending on the value of MovSinGrat_addblank
        if MovSinGrat_addblank == 0 or MovSinGrat_addblank == 1:
            #this variable controls the looping and frame that is to be displayed
            frmNum = 0 #frame number within one cycle
            
        elif MovSinGrat_addblank == 2 and m == 0:
            #this variable controls the looping and frame that is to be displayed
            frmNum = 0 #frame number within one cycle
        
        #setting up the grating
        DrawTexture = visual.GratingStim(
            win=win,
            size = [2*winWidth, 2*winWidth],
            units = 'pix',
            tex=texdata1D[0],
            ori= orientation
            )
        
        if Synch:
            
            #waiting for "TRLstart", if TRLstart is sent this loop will send "TRLstart m" then break
            sock.settimeout(0.5)
            comm = [""]
            while True:
                try:
                    comm = sock.recvfrom(1024)
                except Exception:
                    pass
                    
                if comm[0] == "TRLstart":
                    sock.sendto(("TRLstart " + str(m +1)), (Remote_IP, Remote_Port))
                    break
                    
                elif comm[0] == "ESC1": #if 'ESC1' is in the buffer, return to front
                    sock.close()
                    return
                    
                if mouse.getPressed()[1]:
                    sock.close()
                    print("Exit at ESC1")
                    return
        
        
        
        if MovSinGrat_addblank == 1.0:
            win.color = pixelformeanlum
        
        elif MovSinGrat_addblank == 0.0:
            DrawTexture.draw()
        
        elif MovSinGrat_addblank == 2.0:
            DrawTexture.tex = texdata1D[frmNum]
            DrawTexture.draw()
            frmNum = frmNum + 1
            
            if frmNum >= len(texdata1D):
                    frmNum = 0
        
        square1.draw()
        square2.draw()
        win.flip()
        
        #time before the stimulation
        toc = clock.getTime() - tic
        
        while toc < (t_before/1000.0):
            
            toc = clock.getTime() - tic
            
            if MovSinGrat_addblank == 2:
                
                #assigning the texture using the corrusponding frame
                DrawTexture.tex = texdata1D[frmNum]
                #this if statement is for existing the stimulation
                if mouse.getPressed()[1]:
                    
                    if Synch:
                        sock.close()
                    return
                
                frmNum = frmNum + 1
                
                if frmNum >= len(texdata1D):
                    frmNum = 0
                
                DrawTexture.draw()
                square1.draw()
                square2.draw()
                win.flip()
                
        
        #t_triger initial timing for triggerin the camera
        for i in range(int(FR*MovSinGrat_t_triginit/1000.0)):
            if i < 3:
                square1.fillColor = [1,1,1]
                square2.fillColor = [-1,-1,-1]
            
            else:
                square1.fillColor = [-1,-1,-1]
                square2.fillColor = [-1,-1,-1]
            
            if MovSinGrat_addblank == 1.0:
                win.color = pixelformeanlum
            
            elif MovSinGrat_addblank == 0.0:
                DrawTexture.draw()
            
            elif MovSinGrat_addblank == 2:
                
                #assigning the texture using the corrusponding frame
                DrawTexture.tex = texdata1D[frmNum]
                
                frmNum = frmNum + 1
                
                if frmNum >= len(texdata1D):
                    frmNum = 0
                
                DrawTexture.draw()
            
            if mouse.getPressed()[1]:
                if Synch:
                    sock.close()
                return
            
            square1.draw()
            square2.draw()
            win.flip()
        
        #making the top square white
        square1.fillColor = [-1,-1,-1]
        square2.fillColor = [1,1,1]
        
        
        
        #drawing the frames on the window
        for frm in range(int(FR*t_During/1000.0)):
            
            #assigning the texture using the corrusponding frame
            DrawTexture.tex = texdata1D[frmNum]
            #this if statement is for existing the stimulation
            if mouse.getPressed()[1]:
                
                if Synch:
                    sock.close()
                return
            
            frmNum = frmNum + 1
            
            if frmNum >= len(texdata1D):
                frmNum = 0
            
            DrawTexture.draw()
            square1.draw()
            square2.draw()
            win.flip()
        
        
        if Synch:
            sock.sendto(("TRLdone " + str(m +1)), (Remote_IP, Remote_Port))
        
        #changing the characteristics of the two squares at the bottom left corner
        square1.fillColor = [-1,-1,-1]
        square2.fillColor = [-1,-1,-1]
        
        #time after the stimulation
        for toc in range(int(t_after*FR/1000.0)):
            
            if MovSinGrat_addblank == 1.0:
                win.color = pixelformeanlum
                
            elif MovSinGrat_addblank == 0.0:
                DrawTexture.draw()
            
            elif MovSinGrat_addblank == 2:
                
                #assigning the texture using the corrusponding frame
                DrawTexture.tex = texdata1D[frmNum]
                frmNum = frmNum + 1
                
                if frmNum >= len(texdata1D):
                    frmNum = 0
                
                DrawTexture.draw()
                
            square1.draw()
            square2.draw()
            win.flip()
        
        
        
        if Synch:
            
            #checking for stop button
            while True:
                
                try:
                    comm = sock.recvfrom(1024)
                except:
                    pass
                
                if comm[0] == "ESC1":
                    sock.close()
                    return 
                
                elif comm[0] == "ESC0":
                    break
                
                elif mouse.getPressed()[1]:
                    sock.close()
                    print("Exit at ESC2")
                    return 
    #save vs data in .npy format
    #name file MVS (movSinGrat) + type of tuning feature manipulated in experiment + datetime
    feature = MovSinGrat_features_dict.keys() 
    date = datetime.today().strftime('%Y%m%d_%H%M%S') #extract today's date
    
    print ('expName down here: ', expName)
    fileName = expName + '_vs_'+ feature[MovSinGrat_features] + '_' + date  #exp name defined above either by user (if not synch) or by eye tracking software (if user)
    
    np.save(fileName + '.npy', paras)
    #let user know data was saved:
    print 'vs data saved in file named:', '-vs-', feature[MovSinGrat_features], date,'.npy'