import nidaqmx
import time
from time import ctime

task = nidaqmx.Task()
name = input("input device name ex) cDAQMOD1/ai0 : ")
task.ai_channels.add_ai_voltage_chan(name)
task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                samps_per_chan=51200)

for i in range(0, 5):
    start = time.time()
    data = task.read(number_of_samples_per_channel=51200)
    end = time.time()

    print("=============================================")
    print("data length : ", len(data))
    print("start time", ctime(start))
    print("end time", ctime(end))
    print("running time (second) :", end - start)
    print("=============================================")
