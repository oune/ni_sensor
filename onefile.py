import nidaqmx
import time
import numpy as np
import csv
from time import ctime, time, localtime, strftime

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:2")
task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                samps_per_chan=51200)

filePath = input("저장할 파일명을 입력해주세요")

with open(filePath, 'a', newline='\n') as f:
    write = csv.writer(f)
    datas = task.read(number_of_samples_per_channel=-1)

    now = time()
    now_str = ctime(now)

    for i in range(len(datas[0])):
        li = [now_str]
        li.extend([datas[j][i] for j in range(len(task.channels))])
        write.writerow(li)
