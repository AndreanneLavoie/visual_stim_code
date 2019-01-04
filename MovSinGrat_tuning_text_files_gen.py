from __future__ import print_function
import numpy as np

#this code will create text files for MovSinGrat inputs, INCLUDING:
#   - List of tuning features
#   - List for all possible values for each tuning feature

#creating list for each feature:
feature_list = ['ori', 'spat', 'temp', 'cont', 'loc']
spat_freq = [0.04, 0.08, 0.16, 0.32, 0.5]
temp_freq_lin = [0.5, 1.0, 2.0, 4.0, 8.0]
temp_freq_osc = [0.1, 0.2, 0.4, 0.8, 1.0]
angles = [angle for angle in np.linspace(0,330,12)]
locations = [n for n in xrange(12)]
contrast = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

#write a list into a text file: 

def List2File(fileName, list): 
    
    """ Will create a file with the content of the list.
    
    INPUT: fileName, list
    
    Note >> do not put .txt at the end of fileName, it will be added automatically
    """
    
    with open(fileName + '.txt', 'w') as f:
        for element in list:
            print (element, file = f)

List2File('tuning_feature_list', feature_list)
List2File('spat_freq', spat_freq)
List2File('temp_freq_lin', temp_freq_lin)
List2File('temp_freq_osc', temp_freq_osc)
List2File('angles_list', angles)
List2File('location_list', locations)
List2File('contrast_list', contrast)

#NOTE: to read each text file, use the following code: 

#with open('tuning_feature_list.txt') as tun_list:
#    feature_list = tun_list.read().split('\n')
#list = list[:-1] #remove empty element ' ' that is accidently created


#NOTE #2: to work with numpy matrix:
#from __future__ import print_function
#import numpy as np


#trying to write a text file that will save matrix... 
#x = [[1,2,3],[1,2,3],[1,2,3]]

#this will autmatically convert np matrix into csv file with specified delimiter:
#np.savetxt('np_test.txt', x, delimiter=',')

#to apend part of matrix to csv file:

#with open('append_np_test.txt', 'a') as f:
#    np.savetxt(f, x)

