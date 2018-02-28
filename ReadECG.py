import logging as lg


class GetData:
    def __init__(self, csv_file):
        self.path = None
        self.time = None
        self.volts = None
        self.verify_csv(csv_file)
        self.get_data()

        lg.basicConfig(filename='GetData.log',
                       level=lg.DEBUG,
                       format='%(asctime)s %(message)s',
                       datefmt='%m/%d/%Y %I:%M:%S %p')

    def verify_csv(self, csv_file):
        try:
            import os
        except ImportError as e:
            print('ImportError: %s module not found.' % e.name)
            lg.debug(' | ABORTED: ImportError: %s' % e.name)

        cwd = os.getcwd()
        csv_path = os.path.join(cwd, csv_file)
        extension = os.path.splitext(csv_file)[1]
        print(flag)
        if extension != '.csv':
            print('TypeError: File not .csv format.')
            lg.debug(' | ABORTED: TypeError: Input file not .csv format.')
            raise TypeError
        elif flag is False:
            print('ImportError: File does not exist.')
            lg.debug(' | ABORTED: OSError: File does not exist.')
            raise OSError
        else:
            self.path = csv_path

    def get_data(self):
        try:
            import warnings
            import numpy as np
        except ImportError as e:
            print('ImportError: %s module not found.' % e.name)
            lg.debug(' | ABORTED: ImportError: %s' % e.name)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data = np.genfromtxt(
                self.path, delimiter=",", dtype=(float, float),
                names=['time', 'voltage'])
        if len(data) == 0:
            raise IOError
            lg.debug(' | ABORTED: IOError: Empty input file.')
        else:
            self.time = data['time']
            self.volt = data['voltage']
            print('Success: ECG Data extracted from csv.')
            lg.info(' | SUCCESS: ECG Data extracted from input csv file.')
