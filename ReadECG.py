import logging as lg


class GetData:
    def __init__(self, csv_file):
        self.path = csv_file
        self.time = None
        self.volts = None
        self.verify_csv(csv_file)
        self.get_data()

        lg.basicConfig(filename='GetData.log',
                       level=lg.DEBUG,
                       format='%(asctime)s %(message)s',
                       datefmt='%m/%d/%Y %I:%M:%S %p')

    def verify_csv(self, csv_file):
        """Verifies that input csv path is .csv format and
            that it exists

        :param self: instance of GetData
        :raises ImportError: if module missing
        :raises TypeError: if not .csv format
        :raises OSError: if input file does not exist
        """
        try:
            import os
        except ImportError as e:
            print('ImportError: %s module not found.' % e.name)
            lg.debug(' | ABORTED: ImportError: %s' % e.name)

        extension = os.path.splitext(csv_file)[1]
        cwd = os.getcwd()
        flag = os.path.exists(csv_file)
        if extension != '.csv':
            print('TypeError: Input file type is not .csv')
            raise TypeError('TypeError: File not .csv format.')
            lg.debug(' | ABORTED: TypeError: Input file not .csv format.')
        if flag is False:
            print('OSError: Input file does not exist.')
            raise OSError('OSError: File does not exist.')
            lg.debug(' | ABORTED: OSError: File does not exist.')
        if flag is True and extension == '.csv':
            self.path = csv_file
            lg.info(' | SUCCESS: Input csv file OK to process.')
        return

    def get_data(self):
        """ Gets data from the csv file and assigns values
            to GetData instance

        :param self: instance of GetData
        :raises ImportError: if module missing
        :raises UnknownError: if error occurs during data collection
        :raises IOError: if file is empty
        """
        try:
            import warnings
            import numpy as np
        except ImportError as e:
            print('ImportError: %s module not found.' % e.name)
            lg.debug(' | ABORTED: ImportError: %s' % e.name)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                data = np.genfromtxt(
                    self.path, delimiter=",", dtype=(float, float),
                    names=['time', 'voltage'])
            if len(data) == 0:
                raise IOError('IOError: File empty.')
            else:
                self.time = data['time']
                self.volts = data['voltage']
                print('Success: ECG Data extracted from csv.')
                lg.info(' | SUCCESS: ECG Data extracted from input csv file.')
        except IOError:
            lg.debug(' | ABORTED: IOError: Input file empty.')
            print('IOError: Input file empty.')
            raise IOError
        except:
            print('Unknown Error: check data format in input file.')
            lg.debug(' | ABORTED: Unknown error ocurred.')
        return
