#!/usr/bin/env python3
"""
goose_value_recognition.py
==================================
This module implements the Automatic Goose Value Recognition (AVVR) pipeline.
It refines a raw GOS estimator using statistical variance reduction and bias-corrected likelihood functions to output an "estimated Goose Value".

The implementation adheres strictly to Python's standard library, utilizing only:
- numpy for numerical operations
- pstats for benchmarking statistics
"""

import argparse
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import traceback
import time
import os


# =============================================================================
# DATA TYPES & CONSTANTS
# =============================================================================

@dataclass
class GooseEstimator:
    """
    A class to encapsulate the raw GOS estimator.
    
    Attributes:
        gos_raw (float): The initial, unrefined estimate of the goose value.
            This can be derived from a simple linear regression or other baseline model.
        stats_summary (dict): Statistics summary for variance reduction and bias correction.
            Includes mean squared error, sample size, confidence interval width, etc.
    """

    gos_raw: float = 0.0
    stats_summary: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def compute_gos_variance(samples: List[float]) -> Tuple[float, float]:
    """
    Compute the sample variance of a list of values using NumPy's built-in functionality.
    
    Parameters:
        samples (list): A sorted list of numeric values representing observed goose prices or counts.
        
    Returns:
        tuple: A tuple containing two floats:
            - variance: The sample standard deviation squared (variance).
            - mean_sq_error: Mean Square Error between raw estimate and actual value, scaled by 1/N for unbiasedness estimation.
    
    This is a statistical variance reduction technique to mitigate the "mean of the means" bias in GOS estimates.
    """
    if not samples or len(samples) < 2:
        raise ValueError("At least two required values for variance computation.")

    # Sort and remove duplicates (optional but recommended for robustness)
    sorted_samples = sorted(set(samples))
    
    n = len(sorted_samples)
    mean_val = sum(sorted_samples) / n
    
    if abs(mean_val - 0.0) < 1e-9:
        return var, float('inf')

    # Compute variance using numpy's built-in function (more accurate than manual loops for large N)
    try:
        from scipy.stats import sample_mean_var as s_mv
        
        # For small samples (<5), use direct computation to ensure correctness with raw GOS estimates which might be non-continuous
        if n <= 10 and len(samples) > 2:
            variance = (sum((s - mean_val)**2 for s in sorted_samples) / n).sqrt()

    except ImportError:
        # Fallback if scipy is not installed, using a simplified approach with numpy's vectorized ops on small lists first. 
        # For larger N or specific distributions, use scipy which might be available via pip install scipy.
        variance = (sum((s - mean_val)**2 for s in sorted_samples) / n).sqrt()

    return variance, float(variance * 100.0)


def compute_gos_mean_squared_error(raw_est: float, actual_value: float) -> Tuple[float, float]:
    """
    Compute the Mean Square Error between a raw GOS estimator and an actual value (or observed count).

    Parameters:
        raw_est (float): The estimated goose cost.
        actual_value (int or float): The true value of the goose (e.g., price per unit, number of units sold).

    Returns:
        tuple: A tuple containing two floats:
            - mse: Mean Square Error between estimator and ground truth.
            - variance_estimate: Standard error estimate for this MSE term (calculated as sqrt(MSE / N)).
    
    This is a standard statistical correction to isolate the signal from noise in GOS estimation.
    """
    if actual_value < 0 or not isinstance(actual_value, int):
        raise ValueError("actual_value must be non-negative and an integer.")

    n = len(samples)
    mse = sum((raw_est - actual_value)**2 for raw_est, samples in zip(raw_est, samples)) / (n + 1) * 0.5
    
    variance_estimate = float(mse ** 0.5)
    
    return mse, variance_estimate


def compute_gos_likelihood(samples: List[float], gos_raw: float) -> Tuple[bool, Dict[str, Any]]
