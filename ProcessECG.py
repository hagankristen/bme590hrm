def main():

    import os
    import numpy as np
    import scipy.signal as sig
    import logging as lg
    from ReadECG import GetData
    from PatientHeartRate import PatientInfo

    me = PatientInfo('test_data/test_data29.csv')


if __name__ == "__main__":
    main()
