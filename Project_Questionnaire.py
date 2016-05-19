import Downlink as module
from matplotlib.backends.backend_pdf import PdfPages 	# to make a pdf file for Bar Graphs
import numpy as np
import sys
try:
    pdf = PdfPages('STATISTICAL_SUMMARY.pdf')     # Initializing  a pdf file
except:
    print('Please Close the PDF FILE to start the simulation..!!!')
    sys.exit()

question_stats = []


############################# Question 1 ################################
print('\n****************************** START OF QUESTION 1 ***************************************')

U = 160
total_time = 6 	# in hrs
road_len = 6000
hom = 3

question = 1
stats = module.downlink(road_len, total_time, U, hom , question , pdf)

# what percentage of call attempts have a problem
total_attempts = len(stats['call_attempt']['alpha']) + len(stats['call_attempt']['beta'])
successful_calls = len(stats['completed_calls']['alpha']) + len(stats['completed_calls']['beta'])

problems_percentage = ((total_attempts - successful_calls ) / total_attempts )*100

print('\nPercentage of call attempts that have problem is : {}'.format( problems_percentage))


print('\n****************************** END OF QUESTION 1 *****************************************')

print('\n****************************** START OF QUESTION 2 ***************************************')

U = 160
total_time = 6
road_len = 8000
pdf_name = 'Question_1.pdf'
question = 2
stats = module.downlink(road_len, total_time, U ,hom , question , pdf) 
# what percentage of call attempts have a problem
total_attempts = len(stats['call_attempt']['alpha']) + len(stats['call_attempt']['beta'])
successful_calls = len(stats['completed_calls']['alpha']) + len(stats['completed_calls']['beta'])

problems_percentage = ((total_attempts - successful_calls ) / total_attempts )*100

print('\nPercentage of call attempts that have problem is : {}'.format( problems_percentage))

print('\n****************************** END OF QUESTION 2 ******************************************')

print('\n****************************** START OF QUESTION 3 ****************************************')

U = 320
total_time = 6
road_len = 6000
question = 3
stats = module.downlink(road_len, total_time, U ,hom, question , pdf)

# what percentage of call attempts have a problem
total_attempts = len(stats['call_attempt']['alpha']) + len(stats['call_attempt']['beta'])
successful_calls = len(stats['completed_calls']['alpha']) + len(stats['completed_calls']['beta'])

problems_percentage = ((total_attempts - successful_calls ) / total_attempts )*100

print('\nPercentage of call attempts that have problem is : {}'.format( problems_percentage))



print('\n****************************** END OF QUESTION 3 *******************************************')

print('\n****************************** START OF QUESTION 4 *****************************************')

U = 320
total_time = 6
road_len = 6000
question = 4

print('\n****************************** START OF QUESTION 4 PART A ***********************************')

hom = 5
stats = module.downlink(road_len, total_time, U ,hom, question , pdf)
total_handoffs_hom_5 = len(stats['handoff_attempt']['alpha']) + len(stats['handoff_attempt']['beta'])

print('\n****************************** START OF QUESTION 4 PART B ***********************************')

hom = 0
stats = module.downlink(road_len, total_time, U ,hom, question , pdf)
total_handoffs_hom_0 = len(stats['handoff_attempt']['alpha']) + len(stats['handoff_attempt']['beta'])

if (total_handoffs_hom_5 > total_handoffs_hom_0):
    print('Number of Handoff Attempts decreases when hom was reduced from 5 to 0\n')
else:
    print('Number of Handoff Attempts increased when hom was reduced from 5 to 0\n')


print('\n****************************** END OF QUESTION 4 ********************************************')

pdf.close() # Closes the PDF file which store the bar graph
