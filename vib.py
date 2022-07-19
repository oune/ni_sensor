import nidaqmx
from time import ctime, time
import numpy as np
import csv
import nidaqmx.system
from nidaqmx.constants import *

system = nidaqmx.system.System.local()
devices = system.devices

print("장치를 선택해주세요")
for idx, device in enumerate(devices):
    print(idx, ']', device.name)

selected = int(input())
device = devices[selected]

task = nidaqmx.Task()
print('add input channels')

channels = device.ai_physical_chans
for channel in channels:
    print("channel : ", channel.name)

channels = input("채널 이름을 입력해 주세요 ex) ai0:3 : ")
task.ai_channels.add_ai_voltage_chan(device.name + "/" + channels)

task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                samps_per_chan=51200)
print('task ready')

filePath = input("저장할 파일명을 입력해주세요")
    
writerList = []
fileList = []
for channel in task.channels:
    name = filePath +"_"+ channel.name.replace("/", "_") + ".csv"
    print('name = ', name)
    fileList.append(open(name, 'a', newline='\n'))
    writerList.append(csv.writer(fileList[-1]))
    
while True:
    datas = task.read(number_of_samples_per_channel=-1)
    for idx, data in enumerate(datas):
        print(len(data))
        for raw in data:
            writerList[idx].writerow([ctime(time()), raw])