class GetData:
    def __init__(self, csv_file):
        """Returns GetData class that contains path and ECG data
                            from csv file

        :param csv_file: path to input csv file
        :returns self: instance of GetData
        :raises TypeError: if csv file nonexistent or not .csv
        :raises IOError: if input csv is empty
        """
        import os
        import numpy as np
        import warnings

        extension = os.path.splitext(csv_file)[1]
        if extension != '.csv':
            raise TypeError
        flag = os.path.exists(csv_file)
        if flag is False:
            raise TypeError
        self.path_name = csv_file
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.data = np.genfromtxt(
                csv_file, delimiter=",", dtype=(float, float))
        if len(self.data) == 0:
            raise IOError
