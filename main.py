# -*-coding:utf-8-*-
import psutil
import GPUtil
import matplotlib.pyplot as plt
import numpy as np

FILTER_FLAG = True
FIFO_MODE = True
FIFO_LENGTH = 500


def detect():
    # get
    gpus = GPUtil.getGPUs()
    gpu_load = gpus[0].load
    gpu_mem_total = gpus[0].memoryTotal
    gpu_mem_used = gpus[0].memoryUsed
    cpu_load = psutil.cpu_percent() / 100
    ram_load = psutil.virtual_memory().percent / 100
    return cpu_load, gpu_load, ram_load, gpu_mem_total, gpu_mem_used


def render(cpu_load, cpu_load_list, gpu_load, gpu_load_list, ram_load_list, gpu_mem_load_list, ram_load,
           send_cycle_list):
    # plt
    plt.cla()
    plt.plot(cpu_load_list, label="CPU", color="red", alpha=0.7, linewidth=3)
    plt.plot(gpu_load_list, label="GPU", color="green", alpha=0.7, linewidth=3)
    plt.plot(ram_load_list, label="RAM", color="orange", alpha=0.7, linewidth=3)
    if gpu_mem_load_list is not None:
        plt.plot(gpu_mem_load_list, label="GPU MEM", color="c", alpha=0.7, linewidth=3)
    if send_cycle_list is not None:
        send_cycle_list = [i/100 for i in send_cycle_list]
        plt.plot(send_cycle_list, label="SendCycle/100")
    plt.legend()
    if gpu_mem_load_list is not None:
        plt.title("CPU: %d%%   GPU: %d%%   RAM: %d%%   GPU MEM: %d%%" %
                  (cpu_load * 100, gpu_load * 100, ram_load * 100, gpu_mem_load_list[-1]*100))
    else:
        plt.title("CPU: %d%%   GPU: %d%%   RAM: %d%%" %
                  (cpu_load * 100, gpu_load * 100, ram_load * 100))
    plt.ylim([0, 1])
    plt.xlim([0, FIFO_LENGTH])
    plt.pause(0.0000000000001)


def main():
    filtered_gpu_load = 0.1
    filtered_cpu_load = 0.1
    filtered_ram_load = 0.1

    if FIFO_MODE:
        filtered_gpu_load_list = [0] * FIFO_LENGTH
        filtered_cpu_load_list = [0] * FIFO_LENGTH
        filtered_ram_load_list = [0] * FIFO_LENGTH
        gpu_mem_load_list = [0] * FIFO_LENGTH
    else:
        filtered_gpu_load_list = []
        filtered_cpu_load_list = []
        filtered_ram_load_list = []
    while True:
        cpu_load, gpu_load, ram_load, gpu_mem_total, gpu_mem_used = detect()
        gpu_mem_load = gpu_mem_used / gpu_mem_total

        # filter
        if FILTER_FLAG:
            filtered_gpu_load = filtered_gpu_load * 0.9 + gpu_load * 0.1
            filtered_cpu_load = filtered_cpu_load * 0.9 + cpu_load * 0.1
            filtered_ram_load = filtered_ram_load * 0.5 + ram_load * 0.5
        else:
            filtered_gpu_load = gpu_load
            filtered_cpu_load = cpu_load
            filtered_ram_load = ram_load

        # list
        filtered_gpu_load_list.append(filtered_gpu_load)
        filtered_cpu_load_list.append(filtered_cpu_load)
        filtered_ram_load_list.append(filtered_ram_load)
        gpu_mem_load_list.append(gpu_mem_load)
        if FIFO_MODE:
            del filtered_gpu_load_list[0]
            del filtered_cpu_load_list[0]
            del filtered_ram_load_list[0]
            del gpu_mem_load_list[0]

        render(filtered_cpu_load, filtered_cpu_load_list, filtered_gpu_load, filtered_gpu_load_list,
               filtered_ram_load_list, gpu_mem_load_list=gpu_mem_load_list, ram_load=ram_load, send_cycle_list=None)


if __name__ == '__main__':
    main()
