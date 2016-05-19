import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Converts in to db
def db(value):
    value_db = 10* math.log(value,10)
    return value_db    

# Calculating lognormal shadowing
def lognormal_shadowing(road_len):
    key_shadow = []
    value_shadow=[]
   
    n = np.random.normal(0,2,int(road_len/2)+1)                     # Generates Shadowing values for every 10 meters and saves in a list 
    j=0
    for i in range(-(int(road_len/2.0)),int(road_len/2.0)+1,10):    #Assigning keys and values for the two lists  
        key_shadow.append(i) 
        value_shadow.append(n[j])
        j = j + 1

    ln_loss = dict(zip(key_shadow, value_shadow))                   # dictionary with loss values for each 10 meter from -3000 to 3000
    return(ln_loss)
   
# Calculates eirp_d (after substraction of discrimination factor of antenna)
def eirp_d(eirp_boresight, freq,y_mobile):

    vector_1 = [20 , y_mobile]
    vector_2 = []
    if (freq == 860) : # for sector alpha
        vector_2 = [0,1]
    else:                               
        vector_2 = [(math.sqrt(3)/2),-0.5]  # for sector beta 
    
    # calculating discriminating loss
    a_discrimination= {0.00:0.00,1.00: 0.02,2.00:0.04,3.00:0.06,4.00:0.09,5.00:0.12,6.00:0.15,7.00:0.19,8.00:0.24,9.00:0.30,10.00:0.35,11.00:0.41,12.00:0.48,13.00:0.55,14.00:0.63,15.00:0.71,16.00:0.80,17.00:0.89,18.00:0.98,19.00:1.09,20.00:1.19,21.00:1.30,22.00:1.42,23.00:1.54,24.00:1.66,25.00:1.79,26.00:1.93,27.00:2.07,28.00:2.21,29.00:2.36,30.00:2.50,31.00:2.66,32.00:2.83,33.00:2.99,34.00:3.15,35.00:3.32,36.00:3.50,37.00:3.68,38.00:3.88,39.00:4.06,40.00:4.26,41.00:4.46,42.00:4.67,43.00:4.87,44.00:5.08,45.00:5.29,46.00:5.50,47.00:5.73,48.00:5.96,49.00:6.20,50.00:6.44,51.00:6.67,52.00:6.91,53.00:7.15,54.00:7.39,55.00:7.64,56.00:7.91,57.00:8.17,58.00:8.43,59.00:8.71,60.00:8.98, 61.00	:9.24,62.00:	9.51,63.00: 9.79,64.00:	10.07,65.00:10.35,66.00:	10.65,67.00:	10.94,68.00:11.24,69.00:	11.53,70.00:	11.83,71.00:	12.11,72.00:	12.40,73.00:	12.79,74.00:	13.10,75.00:	13.43,76.00:	13.75,77.00:	14.10,78.00:	14.44,79.00:	14.78,80.00:	15.13,81.00:	15.48,82.00:	15.84,83.00:	16.19,84.00:	16.56,85.00:	16.95,86.00:	17.33,87.00:	17.73,88.00:	18.12,89.00:	18.51,90.00:	18.90,91.00:	19.33,92.00:	19.76,93.00:	20.16, 94.00:	20.61,95.00:	21.04,96.00:	21.48,97.00:	21.92,98.00:	22.36,99.00:	22.82,100.00:	23.26,101.00:	23.72,102.00:	24.17,103.00:	24.62,104.00:	25.08,105.00:	25.52,106.00:25.98,107.00:26.43,108.00:26.85,109.00:27.28,110.00:27.70,111.00:28.04,112.00:28.40,113.00:28.73,114.00:29.06,115.00:29.42,116.00:29.73,117.00:30.03,118.00:30.34,119.00:30.57,120.00:30.81,121.00:31.00,122.00:31.22,123.00:31.41,124.00:31.65,125.00:31.86,126.00:32.06,127.00:32.28,128.00:32.47,129.00:32.68,130.00:32.94,131.00:33.21,132.00:33.41,133.00:33.60,134.00:33.89,135.00:34.04,136.00:34.32,137.00:34.65,138.00:34.98,139.00:35.26,140.00:35.51,141.00:35.80,142.00:36.09,143.00:36.29,144.00:36.48,145.00:36.69,146.00:36.84,147.00:37.03,148.00:37.12,149.00:37.08,150.00:37.13,151.00:37.03,152.00:36.97,153.00:36.76,154.00:36.56,155.00:36.33,156.00:35.98,157.00:35.68,158.00:35.28,159.00:34.89,160.00:34.44,161.00:34.04,162.00:33.63,163.00:33.24,164.00:32.83,165.00:32.50,166.00:32.16,167.00:31.81,168.00:31.48,169.00:31.23,170.00:30.96,171.00:30.66,172.00:30.36,173.00:30.15,174.00:29.93,175.00:29.74,176.00:29.56,177.00:29.36,178.00:29.20,179.00:29.06,180.00:29.04}    
    angle = np.arccos(np.dot(vector_1, vector_2)/(np.linalg.norm(vector_1) * np.linalg.norm(vector_2)))   # Angle between the antenna direction and user
    angle_degree = (180*angle)/math.pi
    angle = round(angle_degree)                                     # rounding off the angle to match with given dictionary
    # eirp after substracting discrimination loss
    eirp_d = eirp_boresight - a_discrimination[angle]
    return eirp_d

# Calculates the path loss for given location of user
def path_loss(freq, y_mobile,h_m, h_b):

    dist_m_b_meters = math.sqrt(math.pow(20,2) + math.pow(y_mobile,2))  
    oh_loss_urban = 69.55 +26.16*math.log(freq,10) - 13.82*math.log(h_b,10) + (44.9 -6.55*math.log(h_b,10))*math.log((dist_m_b_meters/1000),10)   # Okamura HAta Model
    oh_loss_sm_city = oh_loss_urban - ((1.1*math.log(freq,10)-0.7)*h_m - ((1.56*math.log(freq,10))-0.8))   # for small city 
    return(oh_loss_sm_city)

# Calculates the fading values randomly
def fading():

    mean = 0
    variance = 1 
    x = np.random.normal(mean, math.sqrt(variance),10)              # Real part
    y = np.random.normal(mean, math.sqrt(variance),10)              # Imaginary Part
    z = []
    z = np.add(x , y*(1j))                                          #Creating an array of Complex Numbers
    mag = np.absolute(z)                                            #Magnitude of complex numbers in the array
    mag.sort()
    return db(mag[1])                                               # Converts the fading value in db and returns it

# Computing rsl value afters substracting the pathloss and adding the faiding and shadowing values to eirp_d
def rsl(shadowing, eirp_boresight, freq ,y_mobile, h_m, h_b):
    # calculatin rsl by substracting the pathloss and adding the faiding and shadowing values
    rsl = eirp_d(eirp_boresight, freq ,y_mobile) - path_loss(freq, y_mobile, h_m, h_b) + shadowing[round(y_mobile,-1)] + fading()  # calculating RSL
    return rsl

# Making a BAR GRAPH for the given values and exporting it to a pdf file
def statistics(pdf,call_attempt, completed_calls,handoff_attempt, successful_handoff, handoff_failure, dropped_capacity ,dropped_slg_strength, blocked_calls, question_no):

    stat = plt.subplots()
    N = 8
    index = np.arange(N)

    a = 0
    # Contents of the graph
    alpha_content = [len(call_attempt['alpha']), len(completed_calls['alpha']), len(handoff_attempt['alpha']),len(successful_handoff['alpha']), len(handoff_failure['alpha']),len( dropped_capacity['alpha']), len(dropped_slg_strength['alpha']),len( blocked_calls['alpha'])]
    beta_content = [len(call_attempt['beta']),len(completed_calls['beta']), len(handoff_attempt['beta']),len(successful_handoff['beta']), len(handoff_failure['beta']), len(dropped_capacity['beta']),len(dropped_slg_strength['beta']),len(blocked_calls['beta'])]
    width = 0.35       # the width of the bars
    content_1 = plt.bar(index, alpha_content, width, color='r',align='center', label = 'Alpha Sector')          # MAking a bar
    content_2 = plt.bar(index + width, beta_content, width, color='g',align='center' , label = 'Beta Sector')   # Making a bar

    # adding text labels
    plt.ylabel('COUNT')
    plt.xlabel('ACTIVITY')
    plt.title('STATISTICS FOR QUESTION NO.: {}'.format(question_no))

    # Adding axis ticks
    labels = plt.xticks(index + width/2, ('Call Attempt','Successful Calls', 'Handoff Attempt Out','Successful Handoff Out','Handoff Failure Out', 'Drop Capacity','Drop Signal Strength','Blocked Calls Capacity') , rotation= 'vertical' )
    plt.autoscale() 
    plt.grid(True)                              # Grids on the plot
    plt.tight_layout(h_pad = 10)                # Giving paddign to the plot form above
    

    # Defining a function to label each bar of the plot
    def label_for_bars(content):
    # attach some text labels
        for item in content:
            height = item.get_height()
            plt.text(item.get_x() + item.get_width()/2., 1.01*height, '%d' % int(height), ha='center', va='bottom')

    # Adding labels for each bar
    label_for_bars(content_1)
    label_for_bars(content_2)

    #label = ('Alpha', 'Beta')
    plt.legend(bbox_to_anchor=(1, 1), loc=1, fontsize = 8)


    # for displaying total of the alpha and beta sectors
    for i in range(len(content_1)):

        # Defining the height  of the label above the bars
        if((question_no == 1 ) or ((question_no == 2 ))):
            height_total_tag = (60.0 + max(content_1[i].get_height() , content_2[i].get_height()))
        else:
            height_total_tag = (150.0 + max(content_1[i].get_height() , content_2[i].get_height()))

        # Assigning labels for each bar
        height_total = content_1[i].get_height() + content_2[i].get_height()
        plt.text(content_1[i].get_x() + content_1[i].get_width(),height_total_tag , '%d' % int(height_total), ha='center', va='bottom')
            
    #Saving the figure to the pdf
    plt.savefig(pdf, format='pdf')
    
