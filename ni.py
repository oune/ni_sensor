import csv
import inquirer
import nidaqmx
import nidaqmx.system
from nidaqmx.constants import *
from time import ctime, time, localtime, strftime
from pyfiglet import Figlet
from sys import exit

f = Figlet(font='slant')
print(f.renderText('NI csv writer'))

system = nidaqmx.system.System.local()
devices = system.devices
device_names = [device.name for device in devices]

device_name = inquirer.list_input(
    "장치를 선택해주세요", choices=device_names)
device = system.devices[device_name]


def validation_function(_, current):
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason='채널을 한개 이상 선택해 주세요')
    return True


channel_choices = [
    {'name': channel.name} for channel in device.ai_physical_chans
]

channels = [channel['name']
            for channel in inquirer.checkbox("채널을 선택해주세요",
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

# 라이브러리 업데이트 이후 사용
# filePath = inquirer.path('저장할 파일명을 입력해주세요',
#                       exists=False, path_type=inquirer.Path.FILE)

path_question = [
    inquirer.Path('path', message='저장할 파일명을 입력해주세요',
                  exists=False, path_type=inquirer.Path.FILE),
]
filePath = inquirer.prompt(path_question)['path']


def int_validation(_, current):
    try:
        int(current)
    except:
        raise inquirer.errors.ValidationError('', reason='정수를 입력해 주세요.')

    return True


samplingRate = int(inquirer.text("샘플링 레이트를 입력해 주세요",
                                 validate=int_validation))

task.timing.cfg_samp_clk_timing(rate=samplingRate,
                                active_edge=nidaqmx.constants.Edge.RISING,
                                sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                samps_per_chan=samplingRate * 2)


def getWriterFileList(date):
    writerList = []
    fileList = []
    for channel in task.channels:
        name = filePath + "_" + date + "_" + \
            channel.name.replace("/", "_") + ".csv"
        fileList.append(open(name, 'a', newline='\n'))
        writerList.append(csv.writer(fileList[-1]))
        print(name, '파일 생성됨')

    return writerList, fileList


def writeOne(csvwriter, data: list, time):
    if type(csvwriter) is list:
        csvwriter = csvwriter[0]

    for raw in data:
        csvwriter.writerow([time, raw])


def writeMulti(writerList, datas: list, time):
    for idx, data in enumerate(datas):
        writeOne(writerList[idx], data, time)


try:
    pre_date = localtime(time())
    pre_wday = pre_date.tm_wday
    writerList, fileList = getWriterFileList(strftime('%Y%m%d', pre_date))
    writer = writeMulti if len(channels) != 1 else writeOne

    while True:
        datas = task.read(number_of_samples_per_channel=samplingRate)

        now = time()
        now_date = localtime(now)
        now_wday = now_date.tm_wday
        now_str = ctime(now)

        if (pre_wday != now_wday):
            writerList, fileList = getWriterFileList(
                strftime('%Y%m%d', pre_date))
            pre_wday = now_wday

        print(now_str, " 센서로 부터 값 획득")
        writer(writerList, datas, now_str)

except KeyboardInterrupt:
    for file in fileList:
        file.close()

    task.close()
    print('정상적으로 종료되었습니다.')
    exit()
