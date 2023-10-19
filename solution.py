import datetime
from helper_functions import task_solver


begin_time = datetime.datetime.now()

# Define global variables
COMPANIES_LISTING_PATH = './matching_problem/companies_listing.csv'
MISSIONS_FOLDER = './matching_problem/missions/'
SHARED_FREELANCES_FOR_TASK = 10


# Obtain output dataframe
df_final = task_solver(COMPANIES_LISTING_PATH,
                       MISSIONS_FOLDER, SHARED_FREELANCES_FOR_TASK)

df_final.to_csv('solution.csv', index=False)

end_time = datetime.datetime.now()
running_time = end_time-begin_time
print(f'The number of unique valid pairs is {len(df_final)}.')
print('Script running time: ', running_time)
