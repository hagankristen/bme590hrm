import pytest
from PatientHeartRate import PatientInfo
from ReadECG import GetData
import os
import numpy as np
import scipy.signal as sig
import logging as lg
import warnings


def test_calc_volt_ex():
    patient1 = PatientInfo(GetData('test_data/test_data1.csv'))
    assert(patient1.voltage_extremes == (-0.68, 1.05))


def test_check_volt_range():
    with pytest.raises(ValueError):
        PatientInfo(GetData('test_data/test_data32.csv'))


def test_calc_duration():
    patient2 = PatientInfo(GetData('test_data/test_data1.csv'))
    assert(np.isclose(patient2.duration, 27.775))
    patient3 = PatientInfo(GetData('test_data/test_data30.csv'))
    assert(np.isclose(patient3.duration, 39.996))


def test_calc_beats():
    patient1 = PatientInfo(GetData('test_data/test_data1.csv'))
    if patient1.mean_hr_bpm in range(70, 75):
        flag = True
    else:
        flag = False
    assert(flag)
    if patient1.num_beats in range(30, 35):
        flag = True
    else:
        flag = False
    assert(flag)
    patient2 = PatientInfo(GetData('test_data/test_data18.csv'))
    if patient2.num_beats in range(15, 20):
        flag = True
    else:
        flag = False
    assert(flag)
    if patient2.mean_hr_bpm in range(80, 85):
        flag = True
    else:
        flag = False
    assert(flag)
