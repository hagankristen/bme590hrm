class GetCsvData:
    def __init__(self, csv_file):
        import os
        import numpy as np
        extension = os.path.splitext(csv_file)[1]
        if extension != '.csv':
            raise TypeError
        flag = os.path.exists(csv_file)
        if flag is False:
            raise TypeError
        self.path_name = csv_file
        try:
            self.data = np.loadtxt(csv_file, delimiter=',', dtype='float', encoding = 'utf-8-sig')
        except:
            raise ValueError
