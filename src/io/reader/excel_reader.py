import pandas as pd
import numpy as np
import warnings

'''
Constants
'''

HEADER_ROW = 4

'''
Functions
'''

def read_excel(file_path, sheet, attr_map={}):
    warnings.filterwarnings('ignore', module='openpyxl')
    df = pd.read_excel(file_path, sheet_name=sheet)
    warnings.filterwarnings('default', module='openpyxl')
    df = df.replace({ np.nan: None })
    # Retrieve the column header mapping
    headers = df.iloc[HEADER_ROW - 2]
    keys = list(map(lambda x: attr_map[x] if x in attr_map else None, headers))
    # Read the table data
    result = []
    for j in range(HEADER_ROW - 1, len(df)):
        row = df.iloc[j]
        entry = {}
        for i in range(len(row)):
            if keys[i]:
                entry[keys[i]] = row[i]
        result.append(entry)
    return result