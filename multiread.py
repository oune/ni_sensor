import nidaqmx
import time
from time import ctime
import numpy as np
import csv

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:3")
task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                samps_per_chan=51200)


data = task.read(number_of_samples_per_channel=-1)
print("chanells : ", len(data))

for i in range(len(data)):
    print(i, ": ", len(data[i]))
