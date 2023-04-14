
def preprocess_data(df):
    import pandas as pd
    import numpy as np
    import re
    # read the excel file and replace NaN values with 0
    data = pd.read_excel('Faculty-Scientist_Scheduling_Matrix.xlsx')
    data.replace(np.NaN, 0, inplace=True)

    # define a dictionary for regex replacements and replace using the dictionary
    regex_dict = {'Leave': '', "don't assign anything": '', 'Week-off': '', '\(': '', '\)': '', "(Don't assign anything 12PM-2PM)": '', "\n": ''}
    data = data.replace(regex_dict, regex=True)

    # create an empty dataframe for the final results
    finaldf = pd.DataFrame(columns=['Batch', 'Professor', 'Location', 'NumHours'])

    # loop through the columns of the data, skipping the 'Date' column
    for i in data.drop('Date', 1).columns:
        # loop through each value of the column
        for rowval in data[i]:
            if rowval == 0:
                # if the value is 0, skip it
                continue        
        
        
        
            elif "|" in rowval:
                # if the value contains '|', split it into left and right parts
                left_part, right_part = rowval.split("|")[0], rowval.split("|")[-1]
                if left_part.count("-") >= 2:
                    # if the left part contains at least two '-', split it into three parts and add to finaldf
                    newrow = {'Batch': left_part.split('-')[0], 'Professor': f'{i}', 'Location': left_part.split('-')[1], 'NumHours': left_part.split('-')[-1]}
                    finaldf = finaldf.append(newrow, ignore_index=True)
                    del newrow
                elif right_part.count("-") >= 2:
                    # if the right part contains at least two '-', split it into three parts and add to finaldf
                    newrow = {'Batch': right_part.split('-')[0], 'Professor': f'{i}', 'Location': right_part.split('-')[1], 'NumHours': right_part.split('-')[-1]}
                    finaldf = finaldf.append(newrow, ignore_index=True)
                    del newrow
        
        
            elif rowval.count("|") == 2:
                left_part, middle_part, right_part = rowval.split("|")[0], rowval.split("|")[1], rowval.split("|")[-1]
                if left_part.count("-") >= 2:
                    # if the left part contains at least two '-', split it into three parts and add to finaldf
                    newrow = {'Batch': left_part.split('-')[0], 'Professor': f'{i}', 'Location': left_part.split('-')[1], 'NumHours': left_part.split('-')[-1]}
                    finaldf = finaldf.append(newrow, ignore_index=True)
                    del newrow
            
                if middle_part.count("-") >= 2:
                    # if the left part contains at least two '-', split it into three parts and add to finaldf
                    newrow = {'Batch': middle_part.split('-')[0], 'Professor': f'{i}', 'Location': middle_part.split('-')[1], 'NumHours': middle_part.split('-')[-1]}
                    finaldf = finaldf.append(newrow, ignore_index=True)
                    del newrow
                
                elif right_part.count("-") >= 2:
                    # if the right part contains at least two '-', split it into three parts and add to finaldf
                    newrow = {'Batch': right_part.split('-')[0], 'Professor': f'{i}', 'Location': right_part.split('-')[1], 'NumHours': right_part.split('-')[-1]}
                    finaldf = finaldf.append(newrow, ignore_index=True)
                    del newrow
            
        
        
            elif rowval.count("-") >= 2:
                # if the value contains at least two '-', split it into three parts and add to finaldf
                newrow = {'Batch': rowval.split('-')[0], 'Professor': f'{i}', 'Location': rowval.split('-')[1], 'NumHours': rowval.split('-')[-1]}
                finaldf = finaldf.append(newrow, ignore_index=True)

    # convert 'NumHours' column to float data type
    finaldf['NumHours'] = finaldf['NumHours'].astype(float)

    # remove 'Location' column from the finaldf
    finaldf.drop("Location", 1, inplace=True)

    # group finaldf by 'Batch' and 'Professor' and sum the 'NumHours'
    groupeddf = finaldf.groupby(['Batch', 'Professor'], as_index=False)['NumHours'].agg('sum')

    # pivot the 'groupeddf' dataframe by 'Professor' and 'Batch', and calculate the sum of 'NumHours'
    FinalReport = groupeddf.pivot(index='Professor', columns='Batch', values='NumHours')

    # replace any NaN values with 0
    FinalReport.replace(np.NaN, 0, inplace=True)

    # add a new column 'TotalHrs' to the FinalReport dataframe containing the sum of each row
    FinalReport['TotalHrs'] = FinalReport.sum(axis=1)

    # return the final report
    return FinalReport
