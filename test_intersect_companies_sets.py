# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:06:01 2023

@author: SP003DA2
"""

import pytest
from helper_functions import intersect_companies_sets
    
def test_intersection_2_shared_freelances():
    assert len(intersect_companies_sets(dummy_example, shared_freelances=2)) == 1

def test_intersection_1_shared_freelances():
    assert len(intersect_companies_sets(dummy_example, shared_freelances=1)) == 3
    
    
dummy_example = {'company_1':{'freelance_1','freelance_2','freelance_3'},
                 'company_2':{'freelance_1','freelance_4'},
                 'company_3':{'freelance_1','freelance_3'}}