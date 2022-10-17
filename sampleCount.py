import nidaqmx
from nidaqmx import constants
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
import time
import numpy as np
from time import ctime, time, localtime, strftime

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")

sampleRate = 100     # Sample Rate in Hz
secsToAcquire = 10    # Number of seconds over which to acquire data
numberOfSamples = int(secsToAcquire * sampleRate)

# https://github.com/tenss/Python_DAQmx_examples

task.timing.cfg_samp_clk_timing(
    sampleRate, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=numberOfSamples)

while(True):
    datas = task.read(
        number_of_samples_per_channel=constants.READ_ALL_AVAILABLE)
    now = time()
    now_str = ctime(now)
    print(now_str, " 센서로 부터 값 획득", len(datas))
