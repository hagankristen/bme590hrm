def main():
    try:
        import numpy as np
        import os
        from ReadCsvECG import GetCsvData
        from PatientHeartRate import PatientHeartInfo
        import logging as lg
        import scipy

    except ImportError as e:
        print('ImportError: %s module not found.' % e.name)
        lg.debug(' | ABORTED: ImportError: %s' % e.name)

    cwd = os.getcwd()
    csv_path = os.path.join(cwd, 'test_data/test_data1.csv')

    try:
        patient = GetCsvData(csv_path)
        print('Success: ECG Data extracted from csv.')
    except TypeError:
        print('Input file not csv format or does not exist.')
    except ImportError:
        print('Import Error: module not found.')
    except IOError:
        print('Empty input file.')

    try:
        patient_heart_info = PatientHeartInfo(patient)
        print(patient_heart_info.calc_num_beats())
        print(patient_heart_info.calc_bpm())
    except:
        print('not done')
    #import function files

    #try
    #define class of patientheartrateinfo that has attribues given

    #create data classes inside the patientheartinfo class
    #except print out reason for error (dont raise again)
    #

if __name__ == "__main__":
    main()
