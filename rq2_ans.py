###############################################################################

# REQUIRED: RUN top_n_ans.py with n=3 to get each question linked to the answer
#           with the 3 most upvoted answer linked to it
# OUTPUT: rq2_output.csv:
#            CSV Containing each TagName with its TagStrength (indicating the 
#            fraction of answers associated with that tag), and 1st, 2nd and
#            3rd order Mean Response Times as MTMUA (Mean Time for Most Upvoted
#            Answer)         

###############################################################################

import pandas as pd

# REQUIRED TOP 3 ANSWERS CSV
top_ans_file_path = './ProcessedCSV/rq1.1top_3_answer_raw.csv'
rq_2_ans_output_path = './ProcessedCSV/rq2_output.csv'

############################# LOAD DATAFRAMES #################################

ans_df = pd.read_csv(top_ans_file_path)

###############################################################################

ans_df['CreationDate'] = pd.to_datetime(ans_df['CreationDate'],
      format = '%d/%m/%y %H:%M')
ans_df['AnsCreationDate'] = pd.to_datetime(ans_df['AnsCreationDate'],
      format = '%d/%m/%y %H:%M')
ans_df['BestAnswerTurnAroundTime'] = (ans_df['AnsCreationDate'] - 
            ans_df['CreationDate']).dt.days

###############################################################################
      
################# FLATTEN RECORDS WITH TOP 3 TURNAROUND TIMES #################

rows = []
labels = ['Id', 'TagName', 'FirstBestAnswerTurnAroundTime',
          'SecondBestAnswerTurnAroundTime', 'ThirdBestAnswerTurnAroundTime']
question_group_by_df = ans_df.groupby('Id')
for question_id, values in question_group_by_df:
    question_df = question_group_by_df.get_group(question_id)
    len_ans = len(question_df)
    tag_name = question_df.iloc[0]['TagName']
    first_best = 0 if len_ans < 1 else question_df.iloc[0][
            'BestAnswerTurnAroundTime']
    second_best = 0 if len_ans < 2 else question_df.iloc[1][
            'BestAnswerTurnAroundTime']
    third_best = 0 if len_ans < 3 else question_df.iloc[2][
            'BestAnswerTurnAroundTime']
    rows.append((question_id, tag_name, first_best, second_best, third_best))

flattened_df = pd.DataFrame.from_records(rows, columns = labels)
len_flattened_df = len(flattened_df)
###############################################################################

################# FLATTEN RECORDS WITH TOP 3 TURNAROUND TIMES #################

rows = []
# MTMUA = Mean Time for Most Upvoted Answer
labels = ['TagName', 'TagStrength', 'FirstMTMUA (Days)', 'SecondMTMUA (Days)',
          'ThirdMTMUA (Days)']
tag_group_by_df = flattened_df.groupby('TagName')
for tag, t_values in tag_group_by_df:
    tag_df = tag_group_by_df.get_group(tag)
    rows.append((tag,
                 len(tag_df)/len_flattened_df,
                 tag_df['FirstBestAnswerTurnAroundTime'].mean(),
                 tag_df['SecondBestAnswerTurnAroundTime'].mean(),
                 tag_df['ThirdBestAnswerTurnAroundTime'].mean()))
    
rq2_ans_df = pd.DataFrame.from_records(
        rows, columns = labels).sort_values(by = ['TagStrength'],
                              ascending = False)
rq2_ans_df.to_csv(rq_2_ans_output_path)

###############################################################################