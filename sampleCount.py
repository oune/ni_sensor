import nidaqmx
from nidaqmx import constants
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
import time
import numpy as np
from time import ctime, time, localtime, strftime

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:3")

sampleRate = 2500    # Sample Rate in Hz
numberOfSamples = 50

# https://github.com/tenss/Python_DAQmx_examples

task.timing.cfg_samp_clk_timing(
    sampleRate, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS)


def printData(tTask, event_type, num_samples, callback_data):
    datas = task.read(sampleRate)
    now = time()
    now_str = ctime(now)

    # numberOfSamples 가 2500 보다 작을때 사용하는 로직
    if numberOfSamples < 2500:
        new_datas = []
        for dataList in datas:
            distance = int(len(dataList) / numberOfSamples)
            newList = [dataList[i]
                       for i in range(0, len(dataList) - 1, distance)]
            new_datas.append(newList)

        datas = new_datas

    print(now_str, " 센서로 부터 값 획득", len(datas), len(datas[0]))
    return 0


task.register_every_n_samples_acquired_into_buffer_event(
    sampleRate, printData)

task.start()

while True:
    pass

task.stop()
