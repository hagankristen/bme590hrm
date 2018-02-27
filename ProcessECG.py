def main():
    try:
        import numpy as np
        import os
        from ReadECG import GetData
        from HeartRate import PatientInfo
        import logging as lg
        import scipy

    except ImportError as e:
        print('ImportError: %s module not found.' % e.name)
        lg.debug(' | ABORTED: ImportError: %s' % e.name)

    cwd = os.getcwd()
    csv_path = os.path.join(cwd, 'test_data/test_data9.csv')

    try:
        patient = GetData(csv_path)
        print('Success: ECG Data extracted from csv.')
    except TypeError:
        print('Input file not csv format or does not exist.')
    except ImportError:
        print('Import Error: module not found.')
    except IOError:
        print('Empty input file.')

    flag = CheckData(patient)
    if flag:
        patient = InterpolateData(patient)

    try:
        patient_heart_info = PatientInfo(patient)
        print(patient_heart_info.calc_num_beats())
        print(patient_heart_info.calc_bpm())
        print(len(patient_heart_info.calc_beat_times()))

    except:
        print('not done')


def CheckData(patient):
    import numpy as np
    flag = 0
    flag = np.isnan(patient.data).any()
    if flag:
        print('Imported data requires interpolation.')
    else:
        print('Imported data does not require interpolation.')
    return flag


if __name__ == "__main__":
    main()
