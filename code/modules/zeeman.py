import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


class ZeemanLab():
    """
    Reads the fit parameters from output_data/calibration. Use the convert function to convert voltage data (mV) to 
    field strength (mTesla).
    """
    def __init__(self):
        self.fit = np.load('output_data/calibration/hall_sensor_fit.npy')
        self.err = np.sqrt(np.diag(np.load('output_data/calibration/hall_sensor_cov.npy')))

        self.f = lambda x, a,b: x*a + b
        self.t = 0.004 # The thickness of the FP interferometer in meters
        self.sigma_t = 0.0001 # Estimate of the error on the FP interferometer

    def convert_with_error(self, x, ex):
        """
        Converts voltage data in mV to field strength in mT. Also propagates the uncertainty
        """
        val = self.f(x, *self.fit)
        err = np.sqrt( (self.fit[0]*ex)**2+ (x*self.err[0])**2 + self.err[1]**2)
        return val,err

    def convert(self, x):
        """
        Converts voltage data in mV to field strength in mT. Use conver_with_error if you want to propagate error as well.
        """
        val = self.f(x, *self.fit)
        return val

    def compute_delta_nu(self, x):
        """
        Takes in an array of size 12 which has the radius values of the peaks (4 orders, each with 3 values) in order from closest to farthest. Returns a tuple with delta_nu and the error.
        """
        try:
            if x.size == 12:
                formatted_arr = np.resize(x, (4, 3))
                delta_ab = np.zeros(4)
                Delta = np.zeros(9)
                for i in range(len(delta_ab)):
                    delta_ab[i] = formatted_arr[i][1] - formatted_arr[i][0]
                for i in range(int(len(Delta) / 3)):
                    a, b, c = formatted_arr[(i+1)] - formatted_arr[i]
                    Delta[3*i] = a
                    Delta[3*i+1] = b
                    Delta[3*i+2] = c
            
                sigma_delta_ab = np.std(delta_ab) / np.sqrt(len(delta_ab))
                sigma_Delta = np.std(Delta) / np.sqrt(len(Delta))
                avg_delta_ab = np.mean(delta_ab)
                avg_Delta = np.mean(Delta)
            
                a = (1 / (2*self.t*avg_Delta))*sigma_delta_ab
                b = (avg_delta_ab / (2*self.t*avg_Delta**2)) * sigma_Delta
                c = (avg_delta_ab / (2*(self.t**2)*avg_Delta)) * self.sigma_t
            
                sigma_delta_nu = np.sqrt((a**2)+(b**2)+(c**2))
                delta_nu = np.mean(delta_ab) / (2*self.t*np.mean(Delta))
            
                return delta_nu, sigma_delta_nu 
            else:
                raise ValueError("Array is the wrong size! Expected a size 12 array")
        except:
            raise ValueError("Input must be an array!")