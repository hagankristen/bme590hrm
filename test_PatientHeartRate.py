import pytest
from PatientHeartRate import PatientInfo
from ReadECG import GetData
import os
import numpy as np
import scipy.signal as sig
import logging as lg

def test_GetData():
    with pytest.raises(TypeError):
        GetData('testdata.json')
    with pytest.raises(ImportError):
        GetData('notreal.csv')

def test_load_ecg():
    with pytest.raises(TypeError):
        GetData('testdata.json')
    with pytest.raises(ImportError):
        GetData('notreal.csv')

def test_calc_volt_ex():
    patient = PatientInfo('test_data/test_data1.csv')
    assert patient.voltage_extremes == (-.68, 1.05)

def test_check_volt_range():
    with pytest.raises(ValueError):
        PatientInfo('test_data/test_data32.csv')

def test_calc_duration():
    patient = PatientInfo('test_data/test_data1.csv')
    assert(np.isclose(patient.duration, 27.775))

    
