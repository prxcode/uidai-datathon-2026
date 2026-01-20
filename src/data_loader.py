"""
Data loading and merging utilities for UIDAI Datathon project.
"""
import pandas as pd
import glob
import os


def load_and_merge_data(base_path="data/raw"):
    """
    Load demographic and biometric data from CSV files and merge them.
    
    Args:
        base_path (str): Base directory containing data subdirectories
        
    Returns:
        pd.DataFrame: Merged dataframe with demographic and biometric data
    """
    print("Loading Demographic Data...")
    demo_files = glob.glob(os.path.join(base_path, "demographic", "*.csv"))
    if not demo_files:
        print(f"No demographic CSV files found in {base_path}/demographic/")
        return pd.DataFrame()
        
    demo_dfs = [pd.read_csv(f) for f in demo_files]
    df_demo = pd.concat(demo_dfs, ignore_index=True)
    
    print("Loading Biometric Data...")
    bio_files = glob.glob(os.path.join(base_path, "biometric", "*.csv"))
    if not bio_files:
        print(f"No biometric CSV files found in {base_path}/biometric/")
        return pd.DataFrame()

    bio_dfs = [pd.read_csv(f) for f in bio_files]
    df_bio = pd.concat(bio_dfs, ignore_index=True)

    print("Merging Data...")
    # Merge based on common columns: state, district, pincode, date
    merge_cols = ['state', 'district', 'pincode', 'date']
    
    # Check if columns exist
    for col in merge_cols:
        if col not in df_demo.columns:
            print(f"Warning: Column '{col}' missing in Demographic data")
        if col not in df_bio.columns:
            print(f"Warning: Column '{col}' missing in Biometric data")

    df = pd.merge(df_demo, df_bio, on=merge_cols, how='inner')
    
    print(f"Data Loaded and Merged. Total Shape: {df.shape}")
    return df


def load_single_dataset(dataset_type, base_path="data/raw"):
    """
    Load a single dataset (demographic, biometric, or enrolment).
    
    Args:
        dataset_type (str): Type of dataset ('demographic', 'biometric', or 'enrolment')
        base_path (str): Base directory containing data subdirectories
        
    Returns:
        pd.DataFrame: Loaded and concatenated dataframe
    """
    print(f"Loading {dataset_type.title()} Data...")
    files = glob.glob(os.path.join(base_path, dataset_type, "*.csv"))
    
    if not files:
        print(f"No {dataset_type} CSV files found in {base_path}/{dataset_type}/")
        return pd.DataFrame()
    
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    
    print(f"{dataset_type.title()} Data Loaded. Shape: {df.shape}")
    return df
