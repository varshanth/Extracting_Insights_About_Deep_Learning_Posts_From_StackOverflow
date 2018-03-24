###############################################################################

# REQUIRED: RUN top_n_ans.py with n=1 to get each question linked to the answer
#           with the most upvoted answer linked to it
# OUTPUT: rq1.1answers_raw.csv:
#            Augmented CSV containing mined designation of user and a measure
#            of his/her reputation within Deep Learning Answers community as
#            a Smoothed Weighted Upvote Downvote Ratio          

###############################################################################

import pandas as pd
import numpy as np

# REQUIRED TOP 1 ANSWER CSV
top_ans_file_path = './ProcessedCSV/rq1.1top_1_answer_raw.csv'
rq1_1_ans_save_path = './ProcessedCSV/rq1.1answers_raw.csv'


_designations = [
        'Professional',
        'Academia-Professional',
        'Academia-Ambiguous',
        'Academia-Pedagogical',
        'Academia-Student',
        'Online-User-Profile-Present'
        ]


_designation_map = {
        'Academia-Student' : {
                'student', 'freshman','sophomore', 'graduate student',
                'grad student', 'undergraduate student', 'undergrad',
                'bachelor', 'phd', 'post graduate', 'postgraduate',
                'academic', 'college senior', 'teaching assistant',
                'data science', 'computer science', 'intern',
                'computer science engineering', 'computer engineering',
                'cs engineering', 'research'},
        'Academia-Pedagogical' : {
                'professor', 'lecturer', 'teacher', 'teach'
                },
        'Academia-Ambiguous' : {
                'researcher', 'computer scientist', 'mathematician',
                'bioinformatician', 'statistician', 'physicist',
                'neuroscientist', 'biologist', 'scientist'
                },
        'Academia-Professional' : {
                'research engineer', 'data scientist', 'research scientist',
                'machine learning engineer'
                },
        'Professional' : {
                'developer', 'engineer', 'designer', 'analyst', 'contractor',
                'software engineer', 'software developer', 'data engineer',
                'graphic designer', 'cs engineer', 'computer engineer',
                'consultant', 'architect', 'manager', 'development',
                'professional', 'founder', 'leader', 'team lead', 'tech lead',
                'technical leader', 'work on'
                },
        'Online-User-Profile-Present' : {
                'http', 'www'
                }
        }


################### ASSIGN DESIGNATIONS TO USERS ##############################

df = pd.read_csv(top_ans_file_path)
len_df = len(df)
df['Designation'] = np.nan
df['SmoothedWeightedUpVoteDownVoteRatio'] = np.nan
parent_break = False
for idx in range(len_df):
    question_details = df.iloc[idx]
    if pd.isnull(question_details['AnsUserAboutMe']):
        df.ix[idx, 'Designation'] = 'Unknown'
        continue
    for parent_designation in _designations:
        for child_designation in _designation_map[parent_designation]:
            if child_designation in question_details['AnsUserAboutMe'].lower():
                df.ix[idx, 'Designation'] = parent_designation
                parent_break = True
                break
        if parent_break:
            parent_break = False
            break
        df.ix[idx, 'Designation'] = 'Unknown'

###############################################################################
        
cols_to_del = ['AnsUserAboutMe', 'ParentId', 'AnsDeletionDate', 'AnsViewCount']
df = df.drop(cols_to_del, axis = 1)

################ SMOOTHED WEIGHTED UPVOTE DOWNVOTE RATIO ######################

user_specific_group_by_df = df.groupby('AnsUserId')
num_users = len(user_specific_group_by_df)

user_post_details = {}
max_num_posts = 0
for user_id, values in user_specific_group_by_df:
    user_post_details[user_id] = {}
    user_posts_df = user_specific_group_by_df.get_group(user_id)
    user_post_details[user_id]['TotalPosts'] = len(user_posts_df)
    if user_post_details[user_id]['TotalPosts'] > max_num_posts:
        max_num_posts = user_post_details[user_id]['TotalPosts']
    user_post_details[user_id]['TotalUpVoteCount'] = user_posts_df[
            'UpVoteCount'].sum()
    user_post_details[user_id]['TotalDownVoteCount'] = user_posts_df[
            'DownVoteCount'].sum()
for user_id in user_post_details.keys():
    user_post_details[user_id]['SmoothedWeightedUpVoteDownVoteRatio'] = (
            ((user_post_details[user_id]['TotalUpVoteCount'] + 1) *
            user_post_details[user_id]['TotalPosts']) / (
                    (user_post_details[user_id]['TotalDownVoteCount'] + 1) *
                    max_num_posts))
for idx in range(len_df):
    user_id = df.ix[idx, 'AnsUserId']
    df.ix[idx, 'SmoothedWeightedUpVoteDownVoteRatio'] = (
            user_post_details[user_id]['SmoothedWeightedUpVoteDownVoteRatio'])
    
###############################################################################

df.to_csv(rq1_1_ans_save_path)

###############################################################################