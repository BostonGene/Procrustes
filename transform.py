import json
import numpy as np
import pandas as pd

def apply_coeffs(expr, estimator_i, est):
    result_c = np.dot(expr[estimator_i[est.name]['genes']], estimator_i[est.name]['coef_']) + estimator_i[est.name]['intercept_']
    return result_c

def Procrustes_predict(ec_expression, path_to_coeffs=''):
    """
    Transforms log2-TPM expression resulted from EC-based library prep kit into polyA-based-like expression values. 
    
    ec_expression: Expression dataframe, samples in rows, genes in columns. Please, make sure expression values are 
    normalized into TPM and logarithmic by (log2 + 1). Genes named accordingly to Gencode v23.
    
    library_kit_version: Type of library prep kit used to make RNA-library. Possible types are 'V7_UTR' and 'V4'.
    For XT HS2 V7 (non-modified) please use 'V7_UTR'.
    
    """
    
    with open(path_to_coeffs, 'r') as file:
        estimators = json.load(file)
        
    expr_df = ec_expression.copy()
    
    expr_df = expr_df.apply(lambda x: apply_coeffs(expr_df, estimators, x))
    
    return expr_df.clip(lower=0, upper=18.5)

def concordance_correlation_coefficient(y_true, y_pred):
    sd_true = np.std(y_true)
    sd_pred = np.std(y_pred)

    if sd_true == 0 or sd_pred == 0:
        return 0

    else:
        cor = np.corrcoef(y_true, y_pred)[0][1]

        mean_true = np.mean(y_true)
        mean_pred = np.mean(y_pred)

        var_true = np.var(y_true)
        var_pred = np.var(y_pred)

        numerator = 2 * cor * sd_true * sd_pred
        denominator = var_true + var_pred + (mean_true - mean_pred) ** 2

        return numerator / denominator
    
def calculate_ccc(exp_ec, exp_polya):
    """
    exp_ec / exp_polya: gene expression dataframes with samples in rows, genes in columns.
    
    """
    
    result_ccc = pd.Series(map(concordance_correlation_coefficient, 
                               exp_ec[exp_polya.columns].T.values, 
                               exp_polya.T.values))
    
    result_ccc = result_ccc.fillna(0).clip(lower=0)
    
    return result_ccc