def main(csv_file):

    try:
        import os
        import numpy as np
        import scipy.signal as sig
        import logging as lg
        from ReadECG import GetData
        from PatientHeartRate import PatientInfo
    except ImportError as e:
        print('ImportError: %s module not found.' % e.name)
        print('Activate virtual environment.')

    print('Beginning ECG Processing...')
    inter = GetData(csv_file)
    final = PatientInfo(inter)
    print('Finished ECG Processing.')
    name = os.path.basename(csv_file)
    name = os.path.splitext(name)[0]
    json_name = name + '.json'
    print('Results seen in %s file' % json_name)


if __name__ == "__main__":
    main()
