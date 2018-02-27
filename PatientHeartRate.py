import os
import numpy as np
import scipy.signal as sig
import logging as lg


class PatientInfo:
    def __init__(self, patient):
        self.name = patient.path_name
        self.ecg = patient.data
        self.voltage_extremes = self.calc_volt_ex()
        self.duration = self.calc_duration()
        self.num_beats = self.calc_num_beats()
        self.mean_hr_bpm = self.calc_bpm()
        self.beat_times = self.calc_beat_times()

    def calc_num_beats(self):
        data = self.ecg
        voltz = data[:, 1]
        time = data[:, 0]
        auto = sig.correlate(voltz, voltz, mode='full', method='auto')
        auto_crop = auto[np.argmax(auto):-1]
        pks = sig.find_peaks_cwt(auto_crop, np.arange(1, 225))
        np.savetxt("pk1.csv", pks, delimiter=",")
        self.num_beats = len(pks)
        return self.num_beats

    def calc_volt_ex(self):
        data = self.ecg
        voltz = data[:, 1]
        self.voltage_extremes = (np.nanmin(voltz), np.nanmax(voltz))
        return self.voltage_extremes

    def calc_duration(self):
        data = self.ecg
        time = data[:, 0]
        self.duration = time[-1] - time[0]
        return self.duration

    def calc_bpm(self):
        period = self.duration
        beats = self.num_beats
        self.mean_hr_bpm = np.rint(beats/period * 60)
        return self.mean_hr_bpm

    def calc_beat_times(self):
        data = self.ecg
        voltz = data[:, 1]
        time = data[:, 0]
        auto = sig.correlate(voltz, voltz, mode='full', method='auto')
        auto_crop = auto[np.argmax(auto):-1]
        pks = sig.find_peaks_cwt(auto_crop, np.arange(1, 225))
        self.beat_times = time[pks]
        return self.beat_times
