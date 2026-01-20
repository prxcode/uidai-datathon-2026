"""
UIDAI Datathon 2026 - Source Package
Production-ready modules for Aadhaar data analysis.
"""

__version__ = "1.0.0"
__author__ = "Priyanshu"

from .data_loader import load_and_merge_data, load_single_dataset
from .analytics import (
    calculate_ssi,
    calculate_gap_by_district,
    calculate_coverage_ratio,
    detect_anomalies_zscore,
    aggregate_by_state
)

__all__ = [
    'load_and_merge_data',
    'load_single_dataset',
    'calculate_ssi',
    'calculate_gap_by_district',
    'calculate_coverage_ratio',
    'detect_anomalies_zscore',
    'aggregate_by_state'
]
