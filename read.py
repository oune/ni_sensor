import nidaqmx
import nidaqmx.system
from nidaqmx.constants import *
import time
from time import ctime
import asyncio

system = nidaqmx.system.System.local()
devices = system.devices


for idx, device in enumerate(devices):
    print(idx, ']', device.name)

name = input("input device name ex) cDAQMOD1/ai0 : ")

print("device type")
print("[1] vib")
print("[2] temp")
type = input("select device type ex) 1 : ")

task = nidaqmx.Task()

if (type == '1'):
    task.ai_channels.add_ai_voltage_chan(name)
    task.timing.cfg_samp_clk_timing(rate=51200,
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                    samps_per_chan=102400)

elif (type == '2'):
    task.ai_channels.add_ai_rtd_chan(name, min_val=0.0, max_val=100.0, rtd_type=RTDType.PT_3750,
                                     resistance_config=ResistanceConfiguration.THREE_WIRE, current_excit_source=ExcitationSource.INTERNAL, current_excit_val=0.00100)
    task.timing.cfg_samp_clk_timing(rate=51200,
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                    samps_per_chan=51200)

else:
    print("wrong input plese try again")


async def read():
    start = time.time()
    data = task.read(number_of_samples_per_channel=51200)
    end = time.time()

    print("=============================================")
    print("data length : ", len(data))
    print("start time", ctime(start))
    print("end time", ctime(end))
    print("running time (second) :", end - start)


async def run():
    for i in range(0, 5):
        await read()

if __name__ == '__main__':
    asyncio.run(run())
