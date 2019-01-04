def drumgrating(SpatFreqDeg, TempFreq, t_before, t_During, t_after, Synch, Motionmode): #any paramter potentially changed by user in front.py 
    
    from psychopy import visual
    from psychopy import event
    from psychopy import clock
    from win32api import GetSystemMetrics

    from init_para import (drumgrating_addblank, drumgrating_Amp_sinu, drumgrating_controlmod, drumgrating_dirindex, drumgrating_Ori, 
    drumgrating_parasize, drumgrating_t_triginit, drumgrating_GammaFactor, drumgrating_AmpFactor, drumgrating_contrast, drumgrating_MeanLum, 
    winWidth , winHeight, ScrnNum, PixelSize, winWidthofEachDisp, DisplayFrameWidth, FR, square1, square2, fontSize, fontClr, win, Local_IP, Local_Port, Remote_IP, Remote_Port)
    
    import socket
    import numpy as np
    import conv
    
    #crating mouse functionality
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
        square1.draw()
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
        
        if drumgrating_controlmod == 'autoVS':
            
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
                paras[i, :] = temp
            
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
        
        elif drumgrating_controlmod == 'manualVS':
            return
    
    #if Synch is False, this else condition will make the parameters in the same format as if Synch was True
    else:
        
        #making the array in which the parameters will be added to
        paras = np.empty(shape=[drumgrating_parasize, 9])
        
        #adding the parameters to the array
        for i in range(drumgrating_parasize): #start from 0 to parasize[0] - 1
            
            #adding the parameters as an array at index i
            paras[i, :] = [SpatFreqDeg, TempFreq, drumgrating_contrast, drumgrating_MeanLum, drumgrating_dirindex, t_before, t_During, t_after, drumgrating_t_triginit]
        
        paratemp = [drumgrating_Ori, Motionmode, drumgrating_Amp_sinu, drumgrating_addblank]
        
        #setting up the parameters based on what was send in the paras variable
        drumgrating_Ori = int(paratemp[0])
        Motionmode = int(paratemp[1])
        drumgrating_Amp_sinu = paratemp[2]
        drumgrating_addblank = paratemp[3]
        
    if Synch:
        #get file name $$$$$$$$$$$$$$$$$$$$
        while True:
            try:
                info = sock.recv(1024)
            except:
                pass
            if info.strip(): #strip spaces
                print (info)
                sock.sendto(("nex"), (Remote_IP, Remote_Port))
                break
            if mouse.getPressed()[1]:
                sock.close()
                return
        #$$$$$$$$$$$$$$$$$$$$$$$$$$
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
    if drumgrating_Ori == 1:
        
        #generating matrix that will be the place holder for every pixel 
        pixelangle = np.empty(shape=[1, winWidth]) #pixel has to be 2D since the image is 2D
        temp = np.array(range(winWidthofEachDisp)) 
        temp.reshape(1,winWidthofEachDisp)# the temp must be 2D 
        tempPixelAngle = np.degrees(np.arctan((temp - (winWidthofEachDisp/2.0))*PixelSize*(2.0/DisplayFrameWidth))) + 45 #calculating the pixel angle for first monitor
        
        for i in range(ScrnNum):
            pixelangle[:,i*winWidthofEachDisp: (i + 1)*winWidthofEachDisp ] = tempPixelAngle + 90*i #taking specific ranges within the full winWidth and replacing the values with the corresponding angles
    
    else:
        return
    
        
    for m in range(drumgrating_parasize):
        
        tic = clock.getTime()
        
        if m == 0: 
            SpatFreqDeg = paras[m, 0]
            TempFreq = paras[m, 1]
            drumgrating_contrast = paras[m, 2]
            drumgrating_MeanLum = paras[m, 3]
            drumgrating_dirindex = paras[m, 4]
            t_before = paras[m, 5]
            t_During = paras[m, 6]
            t_after = paras[m, 7]
            drumgrating_t_triginit = paras[m, 8]
            pixelformeanlum = 2*(np.exp(np.log(drumgrating_MeanLum/drumgrating_AmpFactor)/drumgrating_GammaFactor)/255.0) -1
            drumgrating_gray = drumgrating_MeanLum
            inc = drumgrating_gray*drumgrating_contrast
            
            #frames to be calculated per period
            frames = round(FR/TempFreq)
            
            phase = np.array(range(int(frames)))
            
            if Motionmode == 1:
                phase = (phase/float(round(frames)))*(2.0*np.pi)
            
            elif Motionmode == 0:
                phase = drumgrating_Amp_sinu*np.sin((phase/frames)*2*np.pi)*SpatFreqDeg*2*np.pi
            
            #generating the pixel values for the stimulus depending on the orientation of the stimulus 
            if drumgrating_Ori == 1:
                
                #creating the list that will hold all frames
                texdata1D = []
                
                #generating the pixel values for vertical stimulus
                for i in range(int(frames)):
                    texdata1DTmp = np.exp(np.log((drumgrating_gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase[i]))/drumgrating_AmpFactor)/drumgrating_GammaFactor)
                    pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1
                    texdata1D.append(pixVal)
                
            
            else:
                return
        
        else:
            if sum(abs(paras[m, :] - paras[m-1, :])) > 1e-7:
            #if (not all([v == 0  for v in abs(paras[m, :] - paras[m-1, :])])):
                
                SpatFreqDeg = paras[m, 0]
                TempFreq = paras[m, 1]
                drumgrating_contrast = paras[m, 2]
                drumgrating_MeanLum = paras[m, 3]
                drumgrating_dirindex = paras[m, 4]
                t_before = paras[m, 5]
                t_During = paras[m, 6]
                t_afterVal = paras[m, 7]
                drumgrating_t_triginit = paras[m, 8]
                pixelformeanlum = 2*(np.exp(np.log(drumgrating_MeanLum/drumgrating_AmpFactor)/drumgrating_GammaFactor)/255.0) -1
                drumgrating_gray = drumgrating_MeanLum
                inc = drumgrating_gray*drumgrating_contrast
                
                #frames to be calculated per period
                frames = round(FR/TempFreq)
                
            
            phase = np.array(range(int(frames)))
            
            if Motionmode == 1:
                phase = (phase/float(round(frames)))*(2.0*np.pi)
            
            elif Motionmode == 0:
                phase = drumgrating_Amp_sinu*np.sin((phase/frames)*2*np.pi)*SpatFreqDeg*2*np.pi
            
            #generating the pixel values for the stimulus depending on the orientation of the stimulus 
            if drumgrating_Ori == 1:
                
                #creating the list that will hold all frames
                texdata1D = []
                
                #generating the pixel values for vertical stimulus
                for i in range(int(frames)):
                    texdata1DTmp = np.exp(np.log((drumgrating_gray + inc*np.sin(pixelangle*SpatFreqDeg*2*np.pi + phase[i]))/drumgrating_AmpFactor)/drumgrating_GammaFactor)
                    pixVal = 2*(texdata1DTmp/255) - 1 #converting the pixel values from 0:255 to -1:1
                    texdata1D.append(pixVal)
                
            
            else:
                return
        
        #creating the looping variable for the simulation depending on the value of drumgrating_addblank
        if drumgrating_addblank == 0 or drumgrating_addblank == 1:
            #this variable controls the looping and frame that is to be displayed
            frmNum = 0 #frame number within one cycle
            
        elif drumgrating_addblank == 2 and m == 0:
            #this variable controls the looping and frame that is to be displayed
            frmNum = 0 #frame number within one cycle
        
        #setting up the grating
        DrawTexture = visual.GratingStim(
            win=win,
            size = [winWidth, winHeight],
            units = 'pix',
            tex=texdata1D[0]
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
        
        if drumgrating_addblank == 1.0:
            win.color = pixelformeanlum
        
        elif drumgrating_addblank == 0.0:
            DrawTexture.draw()
        
        elif drumgrating_addblank == 2.0:
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
            
            if drumgrating_addblank == 2:
                
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
        for i in range(int(FR*drumgrating_t_triginit/1000.0)):
            if i < 3:
                square1.fillColor = [1,1,1]
                square2.fillColor = [-1,-1,-1]
            
            else:
                square1.fillColor = [-1,-1,-1]
                square2.fillColor = [-1,-1,-1]
            
            if drumgrating_addblank == 1.0:
                win.color = pixelformeanlum
            
            elif drumgrating_addblank == 0.0:
                DrawTexture.draw()
            
            elif drumgrating_addblank == 2.0:
                
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
            
            if drumgrating_addblank == 1.0:
                win.color = pixelformeanlum
                
            elif drumgrating_addblank == 0.0:
                DrawTexture.draw()
            
            elif drumgrating_addblank == 2:
                
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
            
            