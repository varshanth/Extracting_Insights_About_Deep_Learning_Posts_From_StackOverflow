###############################################################################

# REQUIRED: RUN rq1.1_ques.py and rq1.1_ans.py TO PRODUCE NECESSARY CSV FILES
# OUTPUT: rq1.1questions_output.csv:
#            How much posts of each tag have been asked by each designation              
#         rq1.1answers_output.csv
#            How much posts of each tag have been answered by each designation

###############################################################################

import pandas as pd

rq_1_1_ques_save_path =  './ProcessedCSV/rq1.1questions_raw.csv'
rq_1_1_ans_save_path =  './ProcessedCSV/rq1.1answers_raw.csv'

rq_1_1_ques_output_path = './ProcessedCSV/rq1.1questions_output.csv'
rq_1_1_ans_output_path = './ProcessedCSV/rq1.1answers_output.csv'


############################# LOAD DATAFRAMES #################################

rq1_1_ques_df = pd.read_csv(rq_1_1_ques_save_path)
rq1_1_ans_df = pd.read_csv(rq_1_1_ans_save_path)

ques_group_by_designation = rq1_1_ques_df.groupby('Designation')
ans_group_by_designation = rq1_1_ans_df.groupby('Designation')

###############################################################################

#################### PREPARE RQ1 QUESTION OUTPUT ##############################

rows = []
for designation, d_values in ques_group_by_designation:
    designation_ques_df = ques_group_by_designation.get_group(designation)
    tag_group_by_df = designation_ques_df.groupby('TagName')
    for tag, t_values in tag_group_by_df:
        tag_designation_df = tag_group_by_df.get_group(tag)
        rows.append((tag, designation, len(tag_designation_df)))
labels = ['TagName', 'Designation', 'DesignationStrength']
question_rq1_df = pd.DataFrame.from_records(rows, columns = labels)
question_rq1_df.to_csv(rq_1_1_ques_output_path)

###################### PREPARE RQ1 ANSWER OUTPUT ##############################

rows = []
for designation, d_values in ans_group_by_designation:
    designation_ans_df = ans_group_by_designation.get_group(designation)
    tag_group_by_df = designation_ans_df.groupby('TagName')
    for tag, t_values in tag_group_by_df:
        tag_designation_df = tag_group_by_df.get_group(tag)
        rows.append((tag, designation, len(tag_designation_df)))
labels = ['TagName', 'Designation', 'DesignationStrength']
ans_rq1_df = pd.DataFrame.from_records(rows, columns = labels)
ans_rq1_df.to_csv(rq_1_1_ans_output_path)

###############################################################################