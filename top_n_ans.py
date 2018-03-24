###############################################################################

# REQUIRED: StackOverFlow DataStackExchange Output of RQ1.1 Question-Answers
#           Query
# OUTPUT: rq1.1top_<N>_answer_raw.csv:
#            CSV Containing Question-Top N Answers according to answer score

###############################################################################

import pandas as pd

top_n_ans = 1
answer_file_path = './DSEOutputCSV/QuestionPostsWithAnswers.csv'
top_ans_file_path = './ProcessedCSV/rq1.1top_{0}_answer_raw.csv'.format(
        top_n_ans)


############################# LOAD DATAFRAMES #################################

df = pd.read_csv(answer_file_path)
group_by_question_df = df.groupby('Id')

###############################################################################

df_to_join = []
for question_id, values in group_by_question_df:
    question_df = group_by_question_df.get_group(question_id)
    top_n_answers_df = question_df.nlargest(top_n_ans, 'AnsScore')
    df_to_join.append(top_n_answers_df)


df = pd.concat(df_to_join)


df.to_csv(top_ans_file_path)
###############################################################################