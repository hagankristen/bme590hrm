def main():
    """Main that runs all functions needed to process ECG data
                        from specified input file

    :raises ImportError: if any modules are not imported
    :raises ValueError: input data outside of expected values
    :raises IOError: if any modules are not imported
    :raises ImportError: if input file is Empty
    :raises TypeError: if input file nonexistent or not csv
    """
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

    lg.basicConfig(filename='PatientHeartRateMonitor.log',
                   level=lg.DEBUG,
                   format='%(asctime)s %(message)s',
                   datefmt='%m/%d/%Y %I:%M:%S %p')

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
        lg.debug(' | ABORTED: ImportError: %s' % e.name)
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
    """Checks voltage data to ensure values do not exceed 300 mV

    :param patient: instance of GetData
    :returns None: no return value
    :raises ValueError: if any ECG voltage in data is greater or
                        equal to 300 mV
    """
    import numpy as np
    ecg = patient.data
    voltz = ecg[:, 1]
    if any(i >= 300 for i in voltz):
        raise ValueError
    return


def CheckMissingData(patient):
    """Checks ECG data for missing values

    :param patient: instance of GetData
    :returns flag: boolean flag to indicate interpolation need
    """

    import numpy as np
    flag = 0
    flag = np.isnan(patient.data).any()
    if flag:
        print('Imported data requires interpolation.')
    else:
        print('Imported data does not require interpolation.')
    return flag


def InterpolateData(patient):
    """Interpolates time and voltage data if missing values exist

    :param patient: instance of GetData
    :returns patient: GetData instance of patient with
                        interpolated ecg values
    """
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
    """Write .json file containing attributes of ecg data

    :param patient: instance of PatientInfo
    :returns None: no return value
    """
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
