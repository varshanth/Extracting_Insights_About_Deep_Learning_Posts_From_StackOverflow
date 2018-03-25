###############################################################################

# REQUIRED: RUN rq1.1_ques.py and rq1.1_ans.py TO PRODUCE NECESSARY CSV FILES
# OUTPUT: rq1.2questions_output.csv:
#            Specify for each question within a tag, which score range is the
#            question in, which reputation range the questioner's reputation is
#            in, and which SmoothedWeightedUpVoteDownVote range the
#            questioner's SmoothedWeightedUpVoteDownVote is in
#         rq1.2answers_output.csv
#            Specify for each answer within a tag, which score range is the
#            answer in, which reputation range the answerer's reputation is
#            in, and which SmoothedWeightedUpVoteDownVote range the most
#            upvoted answerer's SmoothedWeightedUpVoteDownVote is in

###############################################################################

import pandas as pd
import numpy as np

rq_1_1_ques_save_path =  './ProcessedCSV/rq1.1questions_raw.csv'
rq_1_1_ans_save_path =  './ProcessedCSV/rq1.1answers_raw.csv'

rq_1_2_ques_output_path = './ProcessedCSV/rq1.2questions_output.csv'
rq_1_2_ans_output_path = './ProcessedCSV/rq1.2answers_output.csv'


############################# LOAD DATAFRAMES #################################

rq1_1_ques_df = pd.read_csv(rq_1_1_ques_save_path)
rq1_1_ans_df = pd.read_csv(rq_1_1_ans_save_path)

ques_group_by_tagname = rq1_1_ques_df.groupby('TagName')
ans_group_by_tagname = rq1_1_ans_df.groupby('TagName')

###############################################################################

def gen_3_ranges(min_val, max_val):
    if min_val == max_val:
        return [(min_val, max_val)]
    diff = max_val - min_val
    delta = diff / 3
    ranges = [(min_val, min_val + delta),
              (min_val + delta, min_val + 2 * delta),
              (min_val + 2 * delta, max_val + 1)]
    return ranges

def is_val_in_range(interval, val):
    min_val = interval[0]
    max_val = interval[1]
    return True if min_val <= val < max_val else False
'''
#################### PREPARE RQ1.2 QUESTION OUTPUT ############################

rq1_1_ques_df['ScoreRange'] = np.nan
rq1_1_ques_df['ReputationRange'] = np.nan
rq1_1_ques_df['SWUDRRange'] = np.nan

tag_to_ranges = {}
counter = 1
len_ques_tags = len(ques_group_by_tagname)
print('Ques: Start retrieving ranges for {0} tags'.format(len_ques_tags))
for tag, d_values in ques_group_by_tagname:
    print('Ques: Processing {0}/{1} tags'.format(counter, len_ques_tags))
    counter += 1
    tag_group_by_df = ques_group_by_tagname.get_group(tag)
    max_score = tag_group_by_df['Score'].max()
    min_score = tag_group_by_df['Score'].min()
    max_reputation = tag_group_by_df['Reputation'].max()
    min_reputation = tag_group_by_df['Reputation'].min()
    max_swudr = tag_group_by_df[
            'SmoothedWeightedUpVoteDownVoteRatio'].max()
    min_swudr = tag_group_by_df[
            'SmoothedWeightedUpVoteDownVoteRatio'].min()
    tag_to_ranges[tag] = {
            'Score' : gen_3_ranges(min_score, max_score),
            'Reputation' : gen_3_ranges(min_reputation, max_reputation),
            'SWUDR' : gen_3_ranges(min_swudr, max_swudr)
            }
print('Ques: Finished Retrieving Ranges. Start processing records')
len_ques_records = len(rq1_1_ques_df)
counter = 0
for idx in range(len_ques_records):
    if counter % 100 == 0:
        print('Ques: Processing {0}/{1} QuesRecords'.format(counter,
              len_ques_records))
    counter += 1
    score = rq1_1_ques_df.loc[idx, 'Score']
    reputation = rq1_1_ques_df.loc[idx, 'Reputation']
    swudr = rq1_1_ques_df.loc[idx, 'SmoothedWeightedUpVoteDownVoteRatio']
    tag = rq1_1_ques_df.loc[idx, 'TagName']
    score_ranges = tag_to_ranges[tag]['Score']
    reputation_ranges = tag_to_ranges[tag]['Reputation']
    swudr_ranges = tag_to_ranges[tag]['SWUDR']
    for score_range in score_ranges:
        if is_val_in_range(score_range, score):
            rq1_1_ques_df.loc[idx, 'ScoreRange'] = '[{0} - {1})'.format(
                    score_range[0], score_range[1])
    for reputation_range in reputation_ranges:
        if is_val_in_range(reputation_range, reputation):
            rq1_1_ques_df.loc[idx, 'ReputationRange'] = '[{0} - {1})'.format(
                    reputation_range[0], reputation_range[1])
    for swudr_range in swudr_ranges:
        if is_val_in_range(swudr_range, swudr):
            rq1_1_ques_df.loc[idx, 'SWUDRRange'] = '[{0} - {1})'.format(
                    swudr_range[0], swudr_range[1])

cols = ['Id', 'TagName', 'Score', 'ScoreRange', 'Reputation', 'ReputationRange',
        'SmoothedWeightedUpVoteDownVoteRatio', 'SWUDRRange']
question_rq1_2_df = rq1_1_ques_df.filter(cols, axis = 1)
question_rq1_2_df.to_csv(rq_1_2_ques_output_path)
'''
###################### PREPARE RQ1.2 ANSWER OUTPUT ############################

rq1_1_ans_df['ScoreRange'] = np.nan
rq1_1_ans_df['ReputationRange'] = np.nan
rq1_1_ans_df['SWUDRRange'] = np.nan

tag_to_ranges = {}
counter = 1
len_ans_tags = len(ans_group_by_tagname)
print('Ans: Start retrieving ranges for {0} tags'.format(len_ans_tags))
for tag, d_values in ans_group_by_tagname:
    print('Ans: Processing {0}/{1} tags'.format(counter, len_ans_tags))
    counter += 1
    tag_group_by_df = ans_group_by_tagname.get_group(tag)
    max_score = tag_group_by_df['AnsScore'].max()
    min_score = tag_group_by_df['AnsScore'].min()
    max_reputation = tag_group_by_df['AnsUserRep'].max()
    min_reputation = tag_group_by_df['AnsUserRep'].min()
    max_swudr = tag_group_by_df[
            'SmoothedWeightedUpVoteDownVoteRatio'].max()
    min_swudr = tag_group_by_df[
            'SmoothedWeightedUpVoteDownVoteRatio'].min()
    tag_to_ranges[tag] = {
            'Score' : gen_3_ranges(min_score, max_score),
            'Reputation' : gen_3_ranges(min_reputation, max_reputation),
            'SWUDR' : gen_3_ranges(min_swudr, max_swudr)
            }
print('Ans: Finished Retrieving Ranges. Start processing records')
len_ans_records = len(rq1_1_ans_df)
counter = 0
for idx in range(len_ans_records):
    if counter % 100 == 0:
        print('Ans: Processing {0}/{1} AnsRecords'.format(counter,
              len_ans_records))
    counter += 1
    score = rq1_1_ans_df.loc[idx, 'AnsScore']
    reputation = rq1_1_ans_df.loc[idx, 'AnsUserRep']
    swudr = rq1_1_ans_df.loc[idx, 'SmoothedWeightedUpVoteDownVoteRatio']
    tag = rq1_1_ans_df.loc[idx, 'TagName']
    score_ranges = tag_to_ranges[tag]['Score']
    reputation_ranges = tag_to_ranges[tag]['Reputation']
    swudr_ranges = tag_to_ranges[tag]['SWUDR']
    for score_range in score_ranges:
        if is_val_in_range(score_range, score):
            rq1_1_ans_df.loc[idx, 'ScoreRange'] = '[{0} - {1})'.format(
                    score_range[0], score_range[1])
    for reputation_range in reputation_ranges:
        if is_val_in_range(reputation_range, reputation):
            rq1_1_ans_df.loc[idx, 'ReputationRange'] = '[{0} - {1})'.format(
                    reputation_range[0], reputation_range[1])
    for swudr_range in swudr_ranges:
        if is_val_in_range(swudr_range, swudr):
            rq1_1_ans_df.loc[idx, 'SWUDRRange'] = '[{0} - {1})'.format(
                    swudr_range[0], swudr_range[1])

cols = ['AnsId', 'TagName', 'AnsScore', 'ScoreRange', 'AnsUserRep', 'ReputationRange',
        'SmoothedWeightedUpVoteDownVoteRatio', 'SWUDRRange']
ans_rq1_2_df = rq1_1_ans_df.filter(cols, axis = 1)
ans_rq1_2_df.to_csv(rq_1_2_ans_output_path)

###############################################################################