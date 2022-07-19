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
channel_name = device.name + "/" + channels
    
task.ai_channels.add_ai_rtd_chan(channel_name, min_val=0.0, max_val=100.0, rtd_type=RTDType.PT_3750, resistance_config=ResistanceConfiguration.THREE_WIRE, current_excit_source=ExcitationSource.INTERNAL, current_excit_val=0.00100)

task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                samps_per_chan=51200)
print('task ready')



for t in device.ao_physical_chans:
    print(t)

filePath = input("저장할 파일명을 입력해주세요 : ")
    
writerList = []
fileList = []
for channel in task.channels:
    name = filePath +"_"+ channel.name.replace("/", "_") + ".csv"
    print('name = ', name)
    fileList.append(open(name, 'a', newline='\n'))
    writerList.append(csv.writer(fileList[-1]))


print('start')
while True:
    datas = task.read(number_of_samples_per_channel=-1)
    for idx, data in enumerate(datas):
        print(len(data))
        for raw in data:
            writerList[idx].writerow([ctime(time()), raw])






