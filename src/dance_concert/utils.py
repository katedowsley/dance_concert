import pandas as pd
def import_data(fname:str):
    if ".csv" in fname:
        data = pd.read_csv(fname)
    elif any(excl_ext in fname for excl_ext in ['.xlsx', '.xls', '.xlsm', '.xlsb']):
        data = pd.read_csv(fname)
    else:
        TypeError(f"Input data must be in the form of a csv or excel file")
    
    for column in data.columns:
        if "\n" in column:
            new_column_name = column.replace("\n", " ")
            data.rename(columns = {column: new_column_name}, inplace=True)

    return data