import pytest
from ReadECG import GetData
import os
import numpy as np
import logging as lg
import warnings


def test_GetData():
    with pytest.raises(TypeError):
        GetData('test_data/test_data1.json')
    with pytest.raises(OSError):
        GetData('test_data/notreal.csv')

def test_verify_csv():
    with pytest.raises(TypeError):
        GetData('test_data/test_data1.json')
    with pytest.raises(OSError):
        GetData('test_data/notreal.csv')

def test_get_data():
    with pytest.raises(IOError):
        GetData('test_data/empty.csv')
