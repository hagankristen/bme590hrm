import pytest
from PatientHeartRate import PatientInfo
from ReadECG import GetData
import os
import numpy as np
import scipy.signal as sig
import logging as lg
import warnings
import json


def test_calc_volt_ex():
    patient1 = PatientInfo(GetData('test_data/test_data1.csv'))
    assert(patient1.voltage_extremes == (-0.68, 1.05))
    patient2 = PatientInfo(GetData('test_data/test_data9.csv'))
    assert(patient2.voltage_extremes == (-1.07, 0.255))


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
    result1 = patient1.beat_times
    actual1 = np.array([0, .817, 1.617, 2.367, 3.372, 3.975, 4.797,
                        5.556, 6.54, 7.292, 8.097, 9.017, 9.769,
                        10.64, 11.46, 12.3, 13.15, 13.81,
                        14.61, 15.54, 16.32, 17.16, 18.02, 18.88,
                        19.64, 20.44, 21.22, 22.02, 22.79, 23.61,
                        24.44, 25.3, 26.11])
    diff1 = np.absolute(result1-actual1)
    assert(all(i <= 0.2 for i in diff1))
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
    result2 = patient2.beat_times
    actual2 = np.array([0, .749, 1.499, 2.249,  2.999, 3.746, 4.499,
                        5.249, 5.994, 6.749, 7.471, 8.224, 8.976, 9.729,
                        10.5, 11.25, 12, 12.69, 13.5])
    diff2 = np.absolute(result2-actual2)
    assert(all(i <= 0.2 for i in diff2))


def test_check_interp():
    intt = PatientInfo(GetData('test_data/test_data30.csv'))
    v = intt.volt
    t = intt.times
    assert(not np.isnan(v).any())
    assert(not np.isnan(t).any())


# def test_write_json():
#    patient1 = PatientInfo(GetData('test_data/test_data1.csv'))
#    name = os.path.basename(patient1.path)
#    name = os.path.splitext(name)[0]
#    json_name = name + '.json'
#    write_data = {
#        'ECG Duration': patient1.duration,
#        'Mean BPM': patient1.mean_hr_bpm,
#        'Number of Beats': patient1.num_beats,
#        'Times of Beats': patient1.beat_times.tolist(),
#        'Voltage Extremes': patient1.voltage_extremes
#    }
#    with open(json_name) as json_data:
#        d = json.load(json_data)
#    assert cmp(write_data, d) == 0
