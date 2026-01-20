"""
Analytics and calculation utilities for UIDAI Datathon project.
Includes Service Strain Index (SSI) calculation and gap analysis.
"""
import pandas as pd
import numpy as np


def calculate_ssi(df, demo_col='demo_age_5_17', bio_col='bio_age_5_17'):
    """
    Calculate Service Strain Index (SSI) for each row.
    SSI = Demographic Demand / (Biometric Supply + 1)
    
    Args:
        df (pd.DataFrame): Input dataframe
        demo_col (str): Column name for demographic data
        bio_col (str): Column name for biometric data
        
    Returns:
        pd.DataFrame: DataFrame with SSI column added
    """
    df = df.copy()
    df['SSI'] = df[demo_col] / (df[bio_col] + 1)
    return df


def calculate_gap_by_district(df, demo_col='demo_age_5_17', bio_col='bio_age_5_17', top_n=10):
    """
    Calculate gap analysis by district and return top N strained districts.
    
    Args:
        df (pd.DataFrame): Input dataframe
        demo_col (str): Column name for demographic demand
        bio_col (str): Column name for biometric supply
        top_n (int): Number of top strained districts to return
        
    Returns:
        pd.DataFrame: Top N districts sorted by gap (demand - supply)
    """
    dist_gap = df.groupby('district').agg({
        demo_col: 'sum',
        bio_col: 'sum'
    }).reset_index()
    
    dist_gap['gap'] = dist_gap[demo_col] - dist_gap[bio_col]
    top_strained = dist_gap.sort_values(by='gap', ascending=False).head(top_n)
    
    return top_strained


def calculate_coverage_ratio(df, enrolment_col, population_col, group_by='district'):
    """
    Calculate coverage ratio (enrolments / population) by grouping column.
    
    Args:
        df (pd.DataFrame): Input dataframe
        enrolment_col (str): Column name for enrolment data
        population_col (str): Column name for population data
        group_by (str): Column to group by (default: 'district')
        
    Returns:
        pd.DataFrame: Coverage ratio by group
    """
    grouped = df.groupby(group_by).agg({
        enrolment_col: 'sum',
        population_col: 'sum'
    }).reset_index()
    
    grouped['coverage_ratio'] = grouped[enrolment_col] / grouped[population_col]
    
    return grouped


def detect_anomalies_zscore(df, value_col, threshold=3):
    """
    Detect anomalies using Z-score method.
    Z = (x - μ) / σ
    
    Args:
        df (pd.DataFrame): Input dataframe
        value_col (str): Column to analyze for anomalies
        threshold (float): Z-score threshold (default: 3 for 3-sigma)
        
    Returns:
        pd.DataFrame: Rows identified as anomalies
    """
    df = df.copy()
    mean = df[value_col].mean()
    std = df[value_col].std()
    
    df['z_score'] = (df[value_col] - mean) / std
    anomalies = df[df['z_score'].abs() > threshold]
    
    return anomalies


def aggregate_by_state(df, value_cols):
    """
    Aggregate data by state for state-level analysis.
    
    Args:
        df (pd.DataFrame): Input dataframe
        value_cols (list): List of columns to aggregate
        
    Returns:
        pd.DataFrame: State-level aggregated data
    """
    agg_dict = {col: 'sum' for col in value_cols}
    state_data = df.groupby('state').agg(agg_dict).reset_index()
    
    return state_data
