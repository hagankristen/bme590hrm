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
        self.check_interp()
        self.check_volt_range()
        self.calc_volt_ex()
        self.calc_duration()
        self.calc_beats()
        self.write_json()

        lg.basicConfig(filename='PatientHeartRate.log',
                       level=lg.DEBUG,
                       format='%(asctime)s %(message)s',
                       datefmt='%m/%d/%Y %I:%M:%S %p')

    def calc_beats(self):
        """Calculates mean beats per min (heart rate),
                num_beats and beat times attributes

        :param self: instance of PatientInfo
        :raises UnknownError: if peak detection fails
        :raises ValueError: if no beats detected
        """
        try:
            auto = sig.correlate(self.volt, self.volt,
                                 mode='full', method='auto')
            auto_crop = auto[np.argmax(auto):-1]
            wid = np.arange(25, 50)
            pks = sig.find_peaks_cwt(np.square(auto_crop), widths=wid)
            if len(pks) == 0:
                print('No peaks in ECG detected')
                raise ValueError
            else:
                self.num_beats = len(pks)
                self.mean_hr_bpm = np.rint(self.num_beats/self.duration * 60)
                self.beat_times = self.time[pks]
                lg.info(' | SUCCESS: Times of beats calculated.')
                lg.info(' | SUCCESS: Mean heart rate calculated.')
                lg.info(' | SUCCESS: Number of beats calculated.')
        except ValueError:
            lg.debug(' | ABORTED: ValueError: No peaks detected.')
        except:
            lg.debug(' | ABORTED: Unknown error during peak detection.')
        return

    def calc_volt_ex(self):
        """Determines maximum and minimum of voltage data (excluding nan)

        :param self: instance of PatientInfo
        :returns voltage_extremes: tuple of min and max voltages
        """
        self.voltage_extremes = (np.nanmin(self.volt), np.nanmax(self.volt))
        lg.info(' | SUCCESS: Voltage extremes calculated.')
        return self.voltage_extremes

    def calc_duration(self):
        """Calculates time of ECG measurement

        :param self: instance of PatientInfo
        :returns duration: duration of strip (s)
        """
        self.duration = self.time[-1] - self.time[0]
        lg.info(' | SUCCESS: ECG strip duration calculated.')
        return self.duration

    def check_volt_range(self):
        """Checks voltage data to ensure values do not exceed 300 mV

        :param self: instance of PatientInfo
        :raises ValueError: if any ECG voltage in data is greater or
                            equal to 300 mV
        """
        if any(i >= 300 for i in self.volt):
            lg.debug(' | ABORTED: ValueError: ECG voltage exceeds 300 mV')
            print('ValueError: ECG voltage exceeds 300 mV')
            raise ValueError
        else:
            lg.info(' | SUCCESS: ECG Data within accepted voltage range.')
        return

    def check_interp(self):
        """Checks ECG data for missing time and voltages values,
            interpolates if needed, saves back to self

        :param patient: instance of PatientInfo
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
        try:
            with open(json_name, 'w') as f:
                save = json.dump(write_data, f, sort_keys=True)
            lg.info(' | SUCCESS: ECG data written to json file.')
            print('Success: ECG data written to .json file.')
        except:
            lg.debug(' | ABORTED: Error writing json file.')
            print('UnknownError during writing of .json file')
            raise
        return
