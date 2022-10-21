import nidaqmx
from nidaqmx import constants
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
import time
import numpy as np
from time import ctime, time, localtime, strftime
from scipy import signal

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")

sampleRate = 2500    # Sample Rate in Hz
numberOfSamples = 50

# https://github.com/tenss/Python_DAQmx_examples

task.timing.cfg_samp_clk_timing(
    sampleRate, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS)

task.start()

errorList = []

for i in range(1, 100):
    numberOfSamples = i
    datas = task.read(sampleRate)
    newList = resample = signal.resample(datas, numberOfSamples)
    print(i, len(newList))

    if (i == len(newList)):
        errorList.append(i)

print(errorList)
task.stop()
