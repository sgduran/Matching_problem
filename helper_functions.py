import os
import pandas as pd


def load_companies(companies_path):
    '''
    Function that loads the companies from the csv file.

    Arguments:
        companies_path -- path to the companies listing csv file

    Returns:
        df_companies -- Dataframe with the cleaned companies listing
    '''

    df_companies = pd.read_csv(companies_path)

    # Companies with no company_id can't be linked to missions
    df_companies.dropna(subset=['company_id'], inplace=True)
    df_companies.reset_index(inplace=True)

    # Drop columns we don't need
    df_companies.drop(columns=['index', 'country'], inplace=True)

    return df_companies


def load_missions(missions_path):
    '''
    Function that loads the missions from a csv file.

    Arguments:
        missions_path -- path to the missions csv file

    Returns:
        df_missions -- Dataframe with the cleaned missions list
    '''

    df_missions = pd.read_csv(missions_path)

    # Missions without company or freelance are not useful for our task
    df_missions.dropna(subset=['company_id', 'freelance_id'], inplace=True)
    df_missions.reset_index(inplace=True)

    # Drop columns we don't need
    df_missions.drop(columns=['index', 'start_date', 'end_date'], inplace=True)

    return df_missions


def map_companies_to_freelances(df_missions):
    '''
    From a given list of missions, build a mapping from each company
    to the set of freelances that worked for it.

    Arguments:
        df_missions -- Dataframe containing a list of missions.

    Returns:
        company_to_freelances -- Dictionary mapping each company to a set of freelances
    '''

    company_to_freelances = {}

    # Visit all missions
    for _, row in df_missions.iterrows():
        if row['company_id'] not in company_to_freelances:
            company_to_freelances[row['company_id']] = {row['freelance_id']}
        elif row['company_id'] in company_to_freelances:
            company_to_freelances[row['company_id']].add(row['freelance_id'])

    return company_to_freelances


def intersect_companies_sets(company_to_freelances, shared_freelances=10):
    '''
    For each pair of companies, do an intersection of their set of freelances. The intersection
    shows the shared freelances. Keep the record only when there is a minimum number of shared
    freelances.

    Arguments:
        company_to_freelances -- Dictionary mapping each company to the set of
                                 freelances that worked for it.
        shared_freelances -- int value. Sets the minimum amount of freelances a
                             pair of companies must share.

    Returns:
        df_pairs -- Dataframe with the valid pairs of companies and the number of shared freelances.
    '''

    # Dict company_pair_counts: assign to each pair of companies the count of
    # freelances that worked for both of them
    company_pair_counts = {}

    # Set visited: used to avoid visiting twice each pair and to avoid comparing
    #  a company to itself.
    visited = {(k, k) for k in company_to_freelances.keys()}

    for k1, v1 in company_to_freelances.items():
        for k2, v2 in company_to_freelances.items():
            if (k1, k2) not in visited:
                len_intersect = len(v1.intersection(v2))
                if len_intersect >= shared_freelances:
                    company_pair_counts[(k1, k2)] = len_intersect
            visited.add((k1, k2))
            visited.add((k2, k1))

    df_pairs = pd.DataFrame(company_pair_counts.items(), columns=[
                            'companies', 'pair_counts'])
    df_pairs[['company_a_id', 'company_b_id']] = pd.DataFrame(
        df_pairs['companies'].tolist())
    df_pairs = df_pairs[['company_a_id', 'company_b_id', 'pair_counts']]

    return df_pairs


def build_output(df_pairs, df_companies):
    '''
    From a Dataframe with pairs of companies and a number of shared freelances, build the final Dataframe.
    Add companies' names to the companies' ids using left join.
    Arguments:
        df_pairs -- Dataframe with pairs of companies and numbers of shared freelances.

    Returns:
        df_final -- Dataframe with the valid pairs of companies, with their ids and names, and the number of shared freelances.
    '''

    # Add companies' names using left join
    df_temp = df_pairs.join(df_companies.set_index(
        'company_id'), on='company_a_id', how='left')
    df_temp.rename(columns={'name': 'company_a_name'}, inplace=True)
    df_temp = df_temp.join(df_companies.set_index(
        'company_id'), on='company_b_id', how='left')
    df_temp.rename(columns={'name': 'company_b_name'}, inplace=True)

    # Build output dataframe
    df_final = df_temp.loc[:, ['company_a_name', 'company_b_name',
                               'company_a_id', 'company_b_id', 'pair_counts']]

    return df_final


def task_solver(companies_path, missions_folder, shared_freelances):
    '''
    Compile all previous functions to obtain the final solution. It works in 5 steps.

    Arguments: 
        companies_path -- path to the companies listing csv file
        missions_folder -- path to the missions folder with the csv files
        shared_freelances -- int value. Sets the minimum amount of freelances a pair of companies must share.

    Returns:
        df_final -- Dataframe with the valid pairs of companies, with their ids and names, and the number of shared freelances.
    '''
    # Step 1) Load companies.
    df_companies = load_companies(companies_path)

    # Step 2) Load missions.
    df_missions = pd.DataFrame()
    for filename in os.listdir(missions_folder):

        MISSIONS_PATH = missions_folder + filename
        df_temp = load_missions(MISSIONS_PATH)
        df_missions = pd.concat([df_missions, df_temp])

    # Step 3) Map companies to sets of freelances.
    company_to_freelances = map_companies_to_freelances(df_missions)

    # Step 4) Intersect set of freelances for each pair of companies.
    df_pairs = intersect_companies_sets(
        company_to_freelances, shared_freelances)

    # Step 5) Build final dataframe adding companies' names.
    df_final = build_output(df_pairs, df_companies)

    return df_final
