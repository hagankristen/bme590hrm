class PatientHeartInfo:
    def __init__ (self, patient):
        self.name = patient.path_name
        self.ecg = patient.data
#        self.mean_hr_bpm = None
        self.voltage_extremes = None
        self.duration = None
#        self.num_beats = None
#        self.beats = None

        try :
            import os
            import numpy as np
            import scipy
            import logging as lg

        except ImportError as e:
            print('ImportError: %s module not found.' % e.name)
            lg.debug(' | ABORTED: ImportError: %s' % e.name)
            raise ImportError

#    def calc_mean_bpm(self):
#        data = self.ecg
#        voltz = data[:,1]
#        time = data[:,2]
#        return data

    def calc_volt_ex(self):
        data = self.ecg
        voltz = data[:,1]
        self.voltage_extremes = (min(voltz), max(voltz))
        return self.voltage_extremes

    def calc_duration(self):
        data = self.ecg
        time = data[:,0]
        self.duration = time[-1]
        return self.duration
