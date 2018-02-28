import logging as lg


class GetData:
    def __init__(self, csv_file):
        self.path = None
        self.time = None
        self.volts = None
        self.verify_csv(csv_file)
        self.get_data(csv_file)

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

        extension = os.path.splitext(csv_file)[1]
        if extension != '.csv':
            raise TypeError
            print('TypeError: File not .csv format.')
            lg.debug(' | ABORTED: TypeError: Input file not .csv format.')
        

    def get_data(self, csv_path):
        try:
            import warnings
            import numpy as np
        except ImportError as e:
            print('ImportError: %s module not found.' % e.name)
            lg.debug(' | ABORTED: ImportError: %s' % e.name)
        try:
            data = np.genfromtxt(
                csv_path, delimiter=",", dtype=(float, float),
                names=['time', 'voltage'])
            if len(data) == 0:
                raise IOError
            else:
                self.path = csv_path
                self.time = data['time']
                self.volt = data['voltage']
                print('Success: ECG Data extracted from csv.')
                lg.info(' | SUCCESS: ECG Data extracted from input csv file.')
        except OSError:
            print('OSError: File does not exist.')
            lg.debug(' | ABORTED: OSError: File does not exist.')
        except IOError:
            print('IOError: File empty.')
            lg.debug(' | ABORTED: IOError: Input file empty.')
        except:
            print('Unknown Error: check input file.')
            lg.debug(' | ABORTED: Unknown error ocurred.')
