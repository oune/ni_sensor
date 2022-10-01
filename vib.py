from random import choices
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

device_name = inquirer.list_input(
    "장치를 선택해주세요.", choices=device_names)
device = system.devices[device_name]

channel_choices = [
    {'name': channel.name} for channel in device.ai_physical_chans
]


def validation_function(_, current):
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason='채널을 한개 이상 선택해 주세요')
    return True


channels = [channel['name']
            for channel in inquirer.checkbox("채널을 선택해주세요.",
                                             choices=channel_choices,
                                             validate=validation_function
                                             )]

sensor_type = inquirer.list_input('측정 타입을 선택해 주세요', choices=[
                                  'temperature', 'vibration'])

task = nidaqmx.Task()


# 채널 등록시 예외 처리 필요
try:
    if sensor_type == 'temperature':
        for channel in channels:
            task.ai_channels.add_ai_rtd_chan(channel, min_val=0.0, max_val=100.0, rtd_type=RTDType.PT_3750,
                                             resistance_config=ResistanceConfiguration.THREE_WIRE, current_excit_source=ExcitationSource.INTERNAL, current_excit_val=0.00100)

    if sensor_type == 'vibration':
        for channel in channels:
            task.ai_channels.add_ai_voltage_chan(channel)
except nidaqmx.errors.DaqError:
    print('잘못된 측정 타입이 선택 되었습니다. 다른 타입으로 선택해 주세요.')
    task.close()
    exit()

task.timing.cfg_samp_clk_timing(rate=51200,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                samps_per_chan=100000)


# 라이브러리 업데이트 이후 사용
# filePath = inquirer.path('저장할 파일명을 입력해주세요.',
#                       exists=False, path_type=inquirer.Path.FILE)

path_question = [
    inquirer.Path('path', message='저장할 파일명을 입력해주세요.',
                  exists=False, path_type=inquirer.Path.FILE),
]
filePath = inquirer.prompt(path_question)['path']

writerList = []
fileList = []
for channel in task.channels:
    name = filePath + "_" + channel.name.replace("/", "_") + ".csv"
    fileList.append(open(name, 'a', newline='\n'))
    writerList.append(csv.writer(fileList[-1]))
    print(name, '파일 생성됨')

while True:
    datas = task.read(number_of_samples_per_channel=51200)

    print(ctime(time()), '센서로 부터 값 획득')

    for idx, data in enumerate(datas):
        for raw in data:
            writerList[idx].writerow([ctime(time()), raw])
