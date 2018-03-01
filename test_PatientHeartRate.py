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
    assert pytest.approx(patient1.num_beats, 5) == 32
    assert pytest.approx(patient1.mean_hr_bpm, 5) == 72
    result1 = patient1.beats
    actual1 = np.array([0.108, 0.792, 1.636, 2.308, 3.311, 4.1,
                        4.903, 5.661, 6.556, 7.384, 8.253, 8.997,
                        9.769, 10.6, 11.47, 12.29, 13.01,
                        14, 14.73, 15.44, 16.33, 17.15,
                        18, 18.82, 19.64, 20.41, 21.18,
                        21.97, 22.78, 23.59, 24.43, 25.27,
                        26.77])
    diff1 = np.absolute(result1-actual1)
    assert(all(i <= 0.2 for i in diff1))
    patient2 = PatientInfo(GetData('test_data/test_data18.csv'))
    assert pytest.approx(patient2.num_beats, 5) == 18
    assert pytest.approx(patient2.mean_hr_bpm, 5) == 62
    result2 = patient2.beats
    actual2 = np.array([0, .749, 1.499, 2.249,  2.999, 3.746, 4.499,
                        5.249, 5.994, 6.749, 7.471, 8.224, 8.976, 9.729,
                        10.5, 11.25, 12, 12.69, 13.5])
    diff2 = np.absolute(result2-actual2)
    assert(all(i <= 0.2 for i in diff2))


def test_check_interp():
    intt = PatientInfo(GetData('test_data/test_data30.csv'))
    v = intt.volt
    t = intt.time
    assert(not np.isnan(v).any())
    assert(not np.isnan(t).any())


def test_write_json():
    patient1 = PatientInfo(GetData('test_data/test_data1.csv'))
    name = os.path.basename(patient1.path)
    name = os.path.splitext(name)[0]
    json_name = name + '.json'
    with open(json_name) as json_data:
        d = json.load(json_data)
    assert(d['ECG Duration'] == patient1.duration)
    assert(np.allclose(d['Voltage Extremes'],
                       np.array(patient1.voltage_extremes)))
    assert(np.isclose(d['Number of Beats'], patient1.num_beats))
    assert(np.isclose(d['Mean BPM'], patient1.mean_hr_bpm))
    assert(np.allclose(d['Times of Beats'], patient1.beats))
