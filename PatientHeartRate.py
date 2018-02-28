import os
import numpy as np
import scipy.signal as sig
import logging as lg


class PatientInfo:
    def __init__(self, patient):
        self.path = patient.path
        self.volt = patient.volts
        self.time = patient.time
        self.voltage_extremes = None
        self.duration = None
        self.num_beats = None
        self.mean_hr_bpm = None
        self.beat_times = None
        self.check_volt_range()
        self.check_interp()
        self.calc_volt_ex()
        self.calc_duration()
        self.calc_num_beats()
        self.calc_bpm()
        self.calc_beat_times()
        self.write_json()

        lg.basicConfig(filename='PatientHeartRate.log',
                       level=lg.DEBUG,
                       format='%(asctime)s %(message)s',
                       datefmt='%m/%d/%Y %I:%M:%S %p')

    def calc_num_beats(self):
        try:
            auto = sig.correlate(self.volt, self.volt,
                                 mode='full', method='auto')
            auto_crop = auto[np.argmax(auto):-1]
            pks = sig.find_peaks_cwt(auto_crop, np.arange(1, 225))
            self.num_beats = len(pks)
            if len(pks) == 0:
                print('No peaks in ECG detected')
                raise ValueError
        except ValueError:
            lg.debug(' | ABORTED: ValueError: No peaks detected.')
        except:
            lg.debug(' | ABORTED: Unknown error during autocorrelation.')

        return self.num_beats

    def calc_volt_ex(self):
        self.voltage_extremes = (np.nanmin(self.volt), np.nanmax(self.volt))
        lg.info(' | SUCCESS: Voltage extremes calculated.')
        return self.voltage_extremes

    def calc_duration(self):
        self.duration = self.time[-1] - self.time[0]
        lg.info(' | SUCCESS: ECG strip duration calculated.')
        return self.duration

    def calc_bpm(self):
        """Calculates mean beats per min (heart rate) using
                initialized duration and num_beats attributes

        :param self: instance of PatientInfo
        :returns mean_hr_bpm: mean beats per min heart rate as
                                as PatientInfo attribute
        """
        self.mean_hr_bpm = np.rint(self.num_beats/self.duration * 60)
        lg.info(' | SUCCESS: Mean bpm calculated.')
        return self.mean_hr_bpm

    def calc_beat_times(self):
        """Calculates times at which a beat occurs using autocorrelation

        :param self: instance of PatientInfo
        :returns None: no return value
        :raises UnknownError: if autocorrelation fails
        """
        try:
            auto = sig.correlate(self.volt, self.volt,
                                 mode='full', method='auto')
            auto_crop = auto[np.argmax(auto):-1]
            pks = sig.find_peaks_cwt(auto_crop, np.arange(1, 225))
            self.beat_times = self.time[pks]
            lg.info(' | SUCCESS: Times of beats calculated.')
        except:
            lg.debug(' | ABORTED: Unknown error during autocorrelation')
        return self.beat_times

    def check_volt_range(self):
        """Checks voltage data to ensure values do not exceed 300 mV

        :param self: instance of PatientInfo
        :returns None: no return value
        :raises ValueError: if any ECG voltage in data is greater or
                            equal to 300 mV
        """
        if any(i >= 300 for i in self.volt):
            lg.debug(' | ABORTED: ValueError: ECG voltage exceeds 300 mV')
            raise ValueError
        else:
            lg.info(' | SUCCESS: ECG Data within accepted voltage range.')
        return

    def check_interp(self):
        """Checks ECG data for missing values and interpolates

        :param patient: instance of PatientInfo
        :returns patient: self with interpolated data values
        """
        if np.isnan(self.time).any():
            nans, x = np.isnan(self.time), lambda z: z.nonzero()[0]
            self.time[nans] = np.interp(x(nans), x(~nans), self.time[~nans])
            print('Imported time data requires interpolation.')
            lg.info(' | SUCCESS: ECG time data interpolated.')
        if np.isnan(self.volt).any():
            nans, x = np.isnan(self.volt), lambda z: z.nonzero()[0]
            self.volt[nans] = np.interp(x(nans), x(~nans), self.volt[~nans])
            print('Imported voltage data requires interpolation.')
            lg.info(' | SUCCESS: ECG voltage data interpolated.')
        return

    def write_json(self):
        """Write .json file containing attributes of ecg data

        :param patient: instance of PatientInfo
        :returns None: no return value
        """
        import json
        import os
        name = os.path.basename(self.path)
        name = os.path.splitext(name)[0]
        json_name = name + '.json'
        write_data = {
            'Mean BPM': self.mean_hr_bpm,
            'Voltage Extremes': self.voltage_extremes,
            'ECG Duration': self.duration,
            'Number of Beats': self.num_beats,
            'Times of Beats': self.beat_times.tolist(),
        }
        with open(json_name, 'w') as f:
            save = json.dump(write_data, f, sort_keys=True)
        lg.info(' | SUCCESS: ECG data written to json file.')
        print('Success: ECG data written to .json file.')

        return
