# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:22:02 2023

@author: SP003DA2
"""
#import pandas
import datetime
#from helper_functions import load_companies, load_missions, map_companies_to_freelances, intersect_companies_sets, build_output
from helper_functions import task_solver


begin_time = datetime.datetime.now()

# Define global variables
COMPANIES_LISTING_PATH = 'companies_listing.csv'
MISSIONS_FOLDER = './missions/'
shared_freelances_for_task = 10


# Obtain output dataframe
df_final = task_solver(COMPANIES_LISTING_PATH, MISSIONS_FOLDER, shared_freelances_for_task)

df_final.to_csv('solution.csv', index=False)

end_time = datetime.datetime.now()
running_time = end_time-begin_time
print('The number of unique valid pairs is %d.' % len(df_final) )
print('Script running time: ', running_time)