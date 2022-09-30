import nidaqmx
from time import ctime, time
import numpy as np
import csv
import nidaqmx.system
from nidaqmx.constants import *
import inquirer
import pprint
import json


system = nidaqmx.system.System.local()
devices = system.devices
device_names = [device.name for device in devices]

device_question = [
    inquirer.List('device_name',
                  message="장치를 선택해주세요.",
                  choices=device_names,
                  ),
]

device_name = inquirer.prompt(device_question)['device_name']
device = system.devices[device_name]

channel_choices = [
    {'name': channel.name} for channel in device.ai_physical_chans
]


def validation_function(ans, current):
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason='채널을 한개 이상 선택해 주세요')
    return True


channel_question = [
    inquirer.Checkbox('device_channels',
                      message="채널을 선택해주세요.",
                      choices=channel_choices,
                      validate=validation_function
                      ),
]
channels = [channel['name']
            for channel in inquirer.prompt(channel_question)['device_channels']]

task = nidaqmx.Task()
for channel in channels:
    task.ai_channels.add_ai_voltage_chan(channel)

task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                samps_per_chan=51200)

path_question = [
    inquirer.Path('path', message='저장할 파일명을 입력해주세요.',
                  exists=False, path_type=inquirer.Path.FILE),
]

filePath = inquirer.prompt(path_question)['path']

writerList = []
fileList = []
for channel in task.channels:
    name = filePath + "_" + channel.name.replace("/", "_") + ".csv"
    print('name = ', name)
    fileList.append(open(name, 'a', newline='\n'))
    writerList.append(csv.writer(fileList[-1]))

while True:
    datas = task.read(number_of_samples_per_channel=-1)
    for idx, data in enumerate(datas):
        for raw in data:
            writerList[idx].writerow([ctime(time()), raw])
