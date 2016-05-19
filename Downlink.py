import numpy as np
import Module_Util as util
import math
import matplotlib.pyplot as plt                         # To plot the bar graphs      
from matplotlib.backends.backend_pdf import PdfPages    # to make a pdf file for Bar Graphs

# This function contains the flow of the base station working 
def downlink(road_len, total_time, U , hom, question , pdf):
    time_step = 1 #in sec
    past_time = 0
    past_time_hr = 0

    # Each sector of basestation will have
    h_b = 50             #meters
    b_dist_frm_road = 20 #meters
    P_tx = 43            #dBm
    loss = 2             #line or connector loss
    AG_tx = 15           #dBi
    N_ch = {'alpha': 15, 'beta': 15}
    frequency = {'alpha':860, 'beta':865}

    #proferties of mobiles
    h_m = 1.5            #meters
    rsl_threshold = -102 #dBm
    rsl = {'alpha': 0 , 'beta':0}  # will store rsl for alpha nad beta sectors

    #characteristics of users uniformly spread along the road
    call_rate = 2        #lambda is 2 calls per hour   # not used yet
    H = 3                #average call duration is 3min per call
    v = 15               #user speed in meters per sec

    # Declaration of few dictionaries and variableused in the program
    x_mobile = 20        # y mobile will be changing every time
    y_mobile = 0
    call_len = 0
    i = 0
    a = 0                # used for seed function
    b = 0                # used for seed function
    c = 0                # used for seed function

    active_calls = []    #Initiliazing with NO ACTIVE USER #####
    call_attempt = {'alpha':[], 'beta':[]}              # To store call attempts
    handoff_attempt = {'alpha':[], 'beta':[]}           # To store handoff attempts
    successful_handoff = {'alpha':[], 'beta':[]}        # To store successful hanfdoffs
    handoff_failure = {'alpha':[], 'beta':[]}           # To store call handoff failures
    blocked_calls = {'alpha':[], 'beta':[]}             # To store call blocked calls
    dropped_slg_strength = {'alpha':[], 'beta':[]}      # To store call dropped due to signal strength
    dropped_capacity = {'alpha':[], 'beta':[]}          # To store call dropped due to cappacity
    completed_calls = {'alpha':[], 'beta':[]}           # To store call completed calls
    count = 0


    l_CA = {'alpha':0, 'beta':0}                        # Length of dictionary Call attempts
    l_SC= {'alpha':0, 'beta':0}                         # Length of dictionary successful Calls
    l_HA = {'alpha':0, 'beta':0}                        # Length of dictionary Handoff Attempts
    l_SH = {'alpha':0, 'beta':0}                        # Length of dictionary Successfull Handoff
    l_HF = {'alpha':0, 'beta':0}                        # Length of dictionary Handoff Failure      
    l_DC = {'alpha':0, 'beta':0}                        # Length of dictionary Dropped due to capacity
    l_DS = {'alpha':0, 'beta':0}                        # Length of dictionary Dropped due to signal strength 
    l_BC = {'alpha':0, 'beta':0}                        # Length of dictionary Blocked due to capacity

    ###################### EIRP BORESIGHT #####################

    eirp_boresight = P_tx + AG_tx - loss    # eirp at bore sight

    ################# SHADOWING VALUES ########################

    shadowing = util.lognormal_shadowing(road_len)

    ################Run every thing for  n  hr#################

    while(past_time <= total_time*3600):
                     
        ######################### FOR EACH USER WHO HAVE A CALL UP ########################

        i = 0
        for j in active_calls[:]:
            
            i = active_calls.index(j)
            active_calls[i]['y_mobile'] = active_calls[i]['y_mobile'] + (active_calls[i]['velocity'])*time_step   #updating location
            
            active_calls[i]['call_time_left'] = active_calls[i]['call_time_left'] - time_step     #updatingcall time
            
            # Disconnecting call if calltime hand ended
            if (active_calls[i]['call_time_left'] < 0):
                count = count +1
                completed_calls[active_calls[i]['sec_server']].append(active_calls[i])              # record a complete call
                N_ch[active_calls[i]['sec_server']] = N_ch[active_calls[i]['sec_server']] + 1       # free a channel in this sector
                del active_calls[i]                                                                 # remover the calls whose time ends
                continue

            #check if location is beyond the road
            if (active_calls[i]['y_mobile'] > (road_len/2.0) or active_calls[i]['y_mobile'] < -(road_len/2.0)):
                N_ch[active_calls[i]['sec_server']] = N_ch[active_calls[i]['sec_server']] + 1       # free a channel on this server sector
                completed_calls[active_calls[i]['sec_server']].append(active_calls[i])              # record a complete call
                del active_calls[i]                                                                 # remove the user            
                continue

            #Updating the RSL values
            rsl[active_calls[i]['sec_server']]= util.rsl(shadowing, eirp_boresight, frequency[active_calls[i]['sec_server']],active_calls[i]['y_mobile'],h_m, h_b)
            
            # If RSL drops below threshold
            if (rsl[active_calls[i]['sec_server']] < rsl_threshold):
                dropped_slg_strength[active_calls[i]['sec_server']].append(active_calls[i])         #call dropped recorded
                N_ch[active_calls[i]['sec_server']] = N_ch[active_calls[i]['sec_server']] + 1       #free the channel form the resp server sector

                del active_calls[i]                                                                 #delete entry from the active call list and put it in archive lsit of callers            
                continue           
            
            # if RSL other > RSL server Attempt handoff
            if (rsl[active_calls[i]['sec_server']] >= rsl_threshold):
                
                #Calculating rsl for the non-serving sector
                rsl[active_calls[i]['sec_not_serving']]  = util.rsl(shadowing, eirp_boresight, frequency[active_calls[i]['sec_not_serving']],active_calls[i]['y_mobile'],h_m, h_b)  # Calculating RSL
                      
                if (rsl[active_calls[i]['sec_not_serving']] > (rsl[active_calls[i]['sec_server']] + hom )):
                    #Recording handoff attempt from serving sector to other sector
                    handoff_attempt[active_calls[i]['sec_server']].append(active_calls[i])           #record as a handoff attempt from serving sector

                    if (N_ch[active_calls[i]['sec_not_serving']] !=0 ):
                        successful_handoff[active_calls[i]['sec_server']].append(active_calls[i])    # successful handoff out of old sector
                        
                        N_ch[active_calls[i]['sec_not_serving']] = N_ch[active_calls[i]['sec_not_serving']] - 1          # occupying a channel on the new server
                        N_ch[active_calls[i]['sec_server']] = N_ch[active_calls[i]['sec_server']] + 1                    # releasing a channel on old server

                        # swapping the serving and non serving sector
                        temp = active_calls[i]['sec_not_serving']
                        active_calls[i]['sec_not_serving'] = active_calls[i]['sec_server']
                        active_calls[i]['sec_server'] = temp 

                    else:  # No channels available with other sector
                        handoff_failure[active_calls[i]['sec_server']].append(active_calls[i])  # handoff failure    
                        
             
        ################### SECTION 2 FOR USER WHO DOES NOT HAVE A CALL UP #####################
        
        # selecting a user who makes a call request  
        
        p = 0

        #For Question number 4 to generate SAME random numbers for hom = 5 and 0
        if (question == 4):
            np.random.seed(a)
            a = a + 1
         
        n_list = np.random.uniform(-(road_len/2),(road_len/2), (U))    # Generating list of U users along the road uniformly
        
        for j in range(U):
            
            #User details to be appended for each user
            user_details = {'y_mobile_start':0 ,'y_mobile':0 , 'velocity': 0 , 'direction': '' , 'sec_server': ''  , 'sec_not_serving': '' , 'call_len': 3  , 'call_time_left':3 , 'ID':0} 
            
            # To avoid picking user which is on an active call
            flag = 0
            for i in range(len(active_calls)):
                if (active_calls[i]['ID'] == j):                        # check if the user is already on a call
                    flag = 1
            if (flag == 1 and (j!=0)):                                  # IF user is on call, continue to the loop and pick next user
                continue       
            n = n_list[j]                                               # selecting a user
       
            # checking if user makes a call request
            if (question == 4):                                         ##For Question number 4 to generate SAME random numbers for hom = 5 and 0
                np.random.seed(b)
                b = b + 1
           
            # Making a call with probablity time_Step * Call rate 
            p = np.random.uniform()
            if(p < (time_step*(call_rate/3600))):

                y_mobile = n                                            # location of user
                user_details['y_mobile'] = y_mobile                     #Updating user details 
                user_details['y_mobile_start'] = y_mobile
                user_details['ID'] = j
                              
                #Determining users direction and setting velocity   
                if (question == 4):                                     ##For Question number 4 to generate SAME random numbers for hom = 5 and 0
                    np.random.seed(c)
                    c = c + 1

                test = np.random.rand()
                if (test < 0.5): #Going north
                    user_details['direction'] = 'North'
                    user_details['velocity'] = v            
                else:           # Going South
                    user_details['direction'] = 'South'
                    user_details['velocity'] = -v
                    
                #Calculating rsl for each sector   
                rsl['alpha']= util.rsl(shadowing, eirp_boresight, frequency['alpha'], y_mobile,h_m, h_b)
                rsl['beta']= util.rsl(shadowing, eirp_boresight, frequency['beta'], y_mobile,h_m, h_b)
                 
                # pick sector with highest RSL            
                if rsl['alpha'] >= rsl['beta'] :        
                    user_details['sec_server'] = 'alpha'
                    user_details['sec_not_serving'] = 'beta'
                    rsl_server = rsl['alpha']            
                else:
                    user_details['sec_server'] = 'beta'
                    user_details['sec_not_serving'] = 'alpha'
                    rsl_server = rsl['beta']                           # pick sector with highest RSL #####           

                call_attempt[user_details['sec_server']].append(user_details)                   # record call attempt at the particular sector
                                 
                # 1-c-iv) 
                if (rsl[user_details['sec_server']] < rsl_threshold):
                    dropped_slg_strength[user_details['sec_server']].append(user_details)       # regestered as a call dropped due to slg strength for this sector
                    continue
                else:# rsl_server >= rsl_threshold attempt to make a calll
      
                    if (N_ch[user_details['sec_server']]!= 0):
                        N_ch[user_details['sec_server']] = N_ch[user_details['sec_server']] - 1
                        user_details['call_len']= math.ceil(np.random.exponential(H*60))
                        user_details['call_time_left'] = user_details['call_len']
                        active_calls.append(user_details)
                        
                    else: #call not setup
                        blocked_calls[user_details['sec_server']].append(user_details)          #record as call blocked for that particular sector
                              
                        if(rsl[user_details['sec_not_serving']]>= rsl_threshold):
                                                
                            if (N_ch[user_details['sec_not_serving']] != 0):
                                N_ch[user_details['sec_not_serving']] = N_ch[user_details['sec_not_serving']] - 1
                                user_details['call_len']= math.ceil(np.random.exponential(H*60))
                                user_details['call_time_left'] = user_details['call_len']
                                # swap the serving sector data in user details
                                temp = user_details['sec_not_serving']
                                user_details['sec_not_serving'] = user_details['sec_server']
                                user_details['sec_server'] = temp
                                active_calls.append(user_details)
                            else:
                                dropped_capacity[user_details['sec_server']].append(user_details)     
            else:
                continue   

        #################################Section 2 ends here###########################

        # Printing the statistics for each hour
        if ((past_time % 3600) == 0  and (past_time !=0)):
            past_time_hr =past_time_hr + 1   

            print('\n\n                        STATISTICS FOR HOUR : {}\n'.format(past_time_hr))
            
            print('{0}          :     {1}              {2}                {3}'.format('Statistics','Alpha', 'Beta','Total'))      # number of channels left
            print('---------------------------------------------------------------------------')
            #record all details after every one hr

            print('Channels In Use     :      {0}                  {1}                  {2}'.format((15-N_ch['alpha']), (15-N_ch['beta']) , (30-(N_ch['alpha']+ N_ch['beta']))))                   # number of channels left


            print('Channels Available  :      {0}                  {1}                  {2}'.format(N_ch['alpha'], N_ch['beta'] , N_ch['alpha']+ N_ch['beta']))                   # number of channels left

            # number of call attempts
            print('Call Attempts       :      {0}                {1}                 {2}'.format(len(call_attempt['alpha']) - l_CA['alpha'] , len(call_attempt['beta']) - l_CA['beta'], len(call_attempt['alpha']) + len(call_attempt['beta']) - l_CA['alpha'] - l_CA['beta'] ))
            l_CA['alpha'] = len(call_attempt['alpha'])
            l_CA['beta'] =len(call_attempt['beta'])

            # completed / sucessfull callls
            print('Successful Call     :      {0}                {1}                 {2}'.format(len(completed_calls['alpha']) - l_SC['alpha'], len(completed_calls['beta']) - l_SC['beta'], len(completed_calls['alpha']) - l_SC['alpha']+ len(completed_calls['beta']) - l_SC['beta'] ))
            l_SC['alpha'] = len(completed_calls['alpha'])
            l_SC['beta'] =len(completed_calls['beta'])

            # Handoff attempts from
            print('Handoff Attempt From:      {0}                 {1}                {2}'.format(len(handoff_attempt['alpha']) - l_HA['alpha'], len(handoff_attempt['beta']) - l_HA['beta'], len(handoff_attempt['alpha']) - l_HA['alpha']+ len(handoff_attempt['beta']) - l_HA['beta']))
            l_HA['alpha'] = len(handoff_attempt['alpha'])
            l_HA['beta'] =len(handoff_attempt['beta'])

            # successful handoffs
            print('Success Handoff Out :      {0}                 {1}                {2}'.format(len(successful_handoff['alpha']) - l_SH['alpha'], len(successful_handoff['beta']) - l_SH['beta'], len(successful_handoff['alpha']) - l_SH['alpha']+ len(successful_handoff['beta']) - l_SH['beta']))
            l_SH['alpha'] = len(successful_handoff['alpha'])
            l_SH['beta'] =len(successful_handoff['beta'])

            # handoff failures
            print('Handoff failures Out:      {0}                  {1}                  {2}' .format(len(handoff_failure['alpha']) - l_HF['alpha'] ,len(handoff_failure['beta']) - l_HF['beta'], len(handoff_failure['alpha']) - l_HF['alpha']+ len(handoff_failure['beta']) - l_HF['beta']))
            l_HF['alpha'] = len(handoff_failure['alpha'])
            l_HF['beta'] =len(handoff_failure['beta'])

            ## number of call drops capacity 
            print('Drop Capacity       :      {0}                  {1}                  {2}'.format(len(dropped_capacity['alpha']) - l_DC['alpha'], len(dropped_capacity['beta']) - l_DC['beta'], len(dropped_capacity['alpha']) - l_DC['alpha']+ len(dropped_capacity['beta']) - l_DC['beta'] ))
            l_DC['alpha'] = len(dropped_capacity['alpha'])
            l_DC['beta'] =len(dropped_capacity['beta'])

            ## number of call drops
            print('Drop Signal Strength:      {0}                  {1}                  {2}'.format(len(dropped_slg_strength['alpha']) - l_DS['alpha'],len(dropped_slg_strength['beta']) - l_DS['beta'],  len(dropped_slg_strength['alpha']) - l_DS['alpha']+len(dropped_slg_strength['beta']) - l_DS['beta']))
            l_DS['alpha'] = len(dropped_slg_strength['alpha'])
            l_DS['beta'] =len(dropped_slg_strength['beta'])

            ## number of call blocked
            print('Blocked Capacity    :      {0}                  {1}                  {2}'.format(len(blocked_calls['alpha']) - l_BC['alpha'] ,len(blocked_calls['beta']) - l_BC['beta'], len(blocked_calls['alpha']) - l_BC['alpha']+ len(blocked_calls['beta']) - l_BC['beta']))
            l_BC['alpha'] = len(blocked_calls['alpha'])
            l_BC['beta'] =len(blocked_calls['beta'])

        past_time = past_time + time_step                # updating time

    ################################### while loop ends here##############################################

    stats = {'N_ch': N_ch , 'call_attempt':call_attempt , 'completed_calls':completed_calls, 'handoff_attempt':handoff_attempt, 'successful_handoff':successful_handoff,'handoff_failure':handoff_failure, 'dropped_capacity':dropped_capacity , 'dropped_slg_strength':dropped_slg_strength , 'blocked_calls':blocked_calls}
    print('')
    print('\n\n             FINAL STATISTICS AFTER {0} HOURS FOR QUESTION {1}\n'.format(past_time_hr, question))

    print('{0}          :     {1}              {2}                {3}'.format('Statistics','Alpha', 'Beta','Total'))                   # number of channels left
    print('---------------------------------------------------------------------------')
    #record all details after every one hr

    print('Channels In Use     :      {0}                  {1}                  {2}'.format((15-N_ch['alpha']), (15-N_ch['beta']) , (30-(N_ch['alpha']+ N_ch['beta']))))                   # number of channels left


    print('Channels Available  :      {0}                  {1}                  {2}'.format(N_ch['alpha'], N_ch['beta'] , N_ch['alpha']+ N_ch['beta']))                   # number of channels left

    # number of call attempts
    print('Call Attempts       :      {0}                {1}                 {2}'.format(len(call_attempt['alpha']) , len(call_attempt['beta']), len(call_attempt['alpha']) + len(call_attempt['beta']) ))

    # completed / sucessfull callls
    print('Successful Call     :      {0}                {1}                 {2}'.format(len(completed_calls['alpha']), len(completed_calls['beta']), len(completed_calls['alpha'])+ len(completed_calls['beta'])))

    # Handoff attempts from
    print('Handoff Attempt From:      {0}                 {1}                {2}'.format(len(handoff_attempt['alpha']), len(handoff_attempt['beta']), len(handoff_attempt['alpha'])+ len(handoff_attempt['beta'])))

    # successful handoffs
    print('Success Handoff Out :      {0}                 {1}                {2}'.format(len(successful_handoff['alpha']), len(successful_handoff['beta']), len(successful_handoff['alpha'])+ len(successful_handoff['beta'])))

    # handoff failures
    print('Handoff failures Out:      {0}                  {1}                  {2}' .format(len(handoff_failure['alpha']),len(handoff_failure['beta']), len(handoff_failure['alpha'])+ len(handoff_failure['beta'])))

    ## number of call drops capacity 
    print('Drop Capacity       :      {0}                  {1}                  {2}'.format(len(dropped_capacity['alpha']), len(dropped_capacity['beta']), len(dropped_capacity['alpha'])+ len(dropped_capacity['beta']) ))

    ## number of call drops
    print('Drop Signal Strength:      {0}                  {1}                  {2}'.format(len(dropped_slg_strength['alpha']),len(dropped_slg_strength['beta']),  len(dropped_slg_strength['alpha'])+len(dropped_slg_strength['beta'])))
        
    ## number of call blocked
    print('Blocked Capacity    :      {0}                  {1}                  {2}'.format(len(blocked_calls['alpha']) ,len(blocked_calls['beta']), len(blocked_calls['alpha']) + len(blocked_calls['beta'])))
      
    # calling statistics function to print the statistics as  a bar graph
    util.statistics(pdf, call_attempt, completed_calls, handoff_attempt ,successful_handoff, handoff_failure, dropped_capacity ,dropped_slg_strength, blocked_calls , question)   

    return stats
