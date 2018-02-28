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
