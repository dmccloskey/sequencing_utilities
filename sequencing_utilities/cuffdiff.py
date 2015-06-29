from pandas import read_table
import os

def load_cuffdiff(filename):
    if os.path.isdir(filename):
        filename = os.path.join(filename, "isoform_exp.diff")
    table = read_table(filename, index_col="test_id",
        true_values=["yes"], false_values=["no"])
    table = table.rename(columns={"log2(fold_change)": "fold_change"})
    
    return table
