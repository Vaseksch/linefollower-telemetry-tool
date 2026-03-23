from statsmodels.tsa.stattools import acf
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from pandas import DataFrame
from loguru import logger
import pandas as pd
import numpy as np

class Analyzer():
    def __init__(self):
        pass
    
    def calculate_dt(self, time):
        return np.median(np.diff(time))
    
    def analyse_data_acf(self,  dataframe: DataFrame):
        time = pd.to_numeric(dataframe["time"])
        error = pd.to_numeric(dataframe["error"])
        dt = self.calculate_dt(time)
        
        acf_vals = acf(error, nlags=len(error)//2)
        peaks, _ = find_peaks(acf_vals)
        period = peaks[0]
        period = period * dt
        
        return period
        
    def analyse_data_fft(self, dataframe: DataFrame):
        time = pd.to_numeric(dataframe["time"])
        error = pd.to_numeric(dataframe["error"])
        dt = self.calculate_dt(time)
        
        yf = fft(error)
        xf = fftfreq(len(error), d=dt)
        dominant_freq = xf[np.argmax(np.abs(yf[1:len(yf)//2])) + 1]
        period = 1 / dominant_freq
        
        return period
    
    def calculate_ziegler_nichols(self, dataframe: DataFrame, ku) -> tuple[float, float]:
        fft_period = self.analyse_data_fft(dataframe) / 10e5
        logger.debug(fft_period)
        acf_period = self.analyse_data_acf(dataframe) / 10e4
        logger.debug(acf_period)
        
        kp = ku * 0.8
        kd_fft = 0.1 * ku * fft_period
        kd_acf = 0.1 * ku * acf_period
        kd_combined = 0.1 * ku * ((fft_period + acf_period)/2)  
        
        logger.debug(f"KP: {kp}")
        logger.debug(f"KD ACF: {kd_acf}")
        logger.debug(f"KD FFT: {kd_fft}")
        logger.debug(f"KD COMBINED: {kd_combined}")
        
        return kp, kd_combined
        
        