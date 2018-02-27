def main():
    try:
        import numpy as np
        import os
        from ReadECG import GetData
        from PatientHeartRate import PatientInfo
        import logging as lg
        import scipy
        import json

    except ImportError as e:
        print('ImportError: %s module not found.' % e.name)
        lg.debug(' | ABORTED: ImportError: %s' % e.name)

    cwd = os.getcwd()
    test_folder = 'test_data/test_data32.csv'
    csv_path = os.path.join(cwd, test_folder)

    try:
        patient = GetData(csv_path)
        print('Success: ECG Data extracted from csv.')
        CheckVoltRange(patient)
        flag = CheckMissingData(patient)
        if flag:
            patient = InterpolateData(patient)

    except ValueError:
        print('ECG data contains values above normal maximum of ~300 mV')
    except TypeError:
        print('Input file not csv format or does not exist.')
    except ImportError:
        print('Import Error: module not found.')
    except IOError:
        print('Empty input file.')

    try:
        patient_heart_info = PatientInfo(patient)
    except:
        print('not done')

    try:
        WriteJson(patient_heart_info, test_folder)
    except:
        print('Json file not written.')


def CheckVoltRange(patient):
    import numpy as np
    ecg = patient.data
    voltz = ecg[:, 1]
    if any(i >= 300 for i in voltz):
        raise ValueError
    return


def CheckMissingData(patient):
    import numpy as np

    flag = 0
    flag = np.isnan(patient.data).any()
    if flag:
        print('Imported data requires interpolation.')
    else:
        print('Imported data does not require interpolation.')
    return flag


def InterpolateData(patient):
    import numpy as np
    ecg = patient.data
    voltz = ecg[:, 1]
    time = ecg[:, 0]
    if np.isnan(time).any():
        nans, x = np.isnan(time), lambda z: z.nonzero()[0]
        time[nans] = np.interp(x(nans), x(~nans), time[~nans])
        ecg[:, 0] = time
    if np.isnan(voltz).any():
        nans, x = np.isnan(voltz), lambda z: z.nonzero()[0]
        voltz[nans] = np.interp(x(nans), x(~nans), voltz[~nans])
        ecg[:, 1] = voltz
    patient.data = ecg
    return patient


def WriteJson(hrm, folder_path):
    import json
    import os
    name = os.path.basename(folder_path)
    name = os.path.splitext(name)[0]
    json_name = name + '.json'
    write_data = {
        'Mean BPM': hrm.mean_hr_bpm,
        'Voltage Extremes': hrm.voltage_extremes,
        'ECG Duration': hrm.duration,
        'Number of Beats': hrm.num_beats,
        'Times of Beats': hrm.beat_times.tolist(),
    }
    with open(json_name, 'w') as f:
        save = json.dump(write_data, f)
    return


if __name__ == "__main__":
    main()
