import pytest
from PatientHeartRate import PatientInfo
from ReadECG import GetData
import os
import numpy as np
import scipy.signal as sig
import logging as lg
import warnings


# def test_calc_volt_ex():
#    patient1 = PatientInfo('test_data/test_data1.csv')
#    print(patient1.voltage_extremes)

def test_check_volt_range():
    with pytest.raises(ValueError):
        PatientInfo('test_data/test_data32.csv')


# def test_calc_duration():
#    patient2 = PatientInfo('test_data/test_data1.csv')
#    print(patient2.duration)
