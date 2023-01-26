# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 14:44:50 2023

@author: SP003DA2
"""

import pytest
from helper_functions import task_solver

def test_no_na_id():
    
    COMPANIES_LISTING_PATH = 'companies_listing.csv'
    MISSIONS_FOLDER = './missions/'
    shared_freelances_for_task = 10

    output = task_solver(COMPANIES_LISTING_PATH, MISSIONS_FOLDER, shared_freelances_for_task)
    
    assert sum(output['company_a_id'].isna()) == 0 and sum(output['company_b_id'].isna()) == 0 and sum(output['pair_counts'] < 10) == 0

