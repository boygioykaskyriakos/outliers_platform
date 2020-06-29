import random as rand
import random
import matplotlib.pyplot as plt
import time


def myHealthcare(n):
    temp = []
    hr = []
    pulse = []
    bloodpr = []
    resrate = []
    oxsat = []
    ph = []
    ts = list(i for i in range(1, n + 1))
    rand.seed(109)
    for i in range(n):
        temp.append(rand.randint(36, 39))
        hr.append(rand.randint(55, 100))
        pulse.append(rand.randint(55, 100))
        bloodpr.append(rand.randint(120, 121))
        resrate.append(rand.randint(11, 17))
        oxsat.append(rand.randint(93, 100))
        ph.append((rand.randint(71, 76) / 10))
    a = list(zip(ts, temp, hr, pulse, bloodpr, resrate, oxsat, ph))
    return a


def abnormalSignAnalytics(n, s):
    sampled = random.sample(myHealthcare(n), k=s)
    abnormal_pulse = []
    abnormal_bloodpr = []
    for record in sampled:
        if record[3] not in range(60, 100):
            abnormal_pulse.append([record[0], record[3]])
        if record[4] != 120:
            abnormal_bloodpr.append(record[0])
    print(str(len(abnormal_pulse)) + ' abnormal pulse records were counted: ' + str(abnormal_pulse))
    print(str(len(abnormal_bloodpr)) + ' abnormal blood pressure records happened in timestamps: ' + str(
        abnormal_bloodpr))
    return abnormal_pulse, abnormal_bloodpr


def frequencyAnalytics(n, s):
    sampled = random.sample(myHealthcare(n), k=s)
    freq_dict = {}
    frec_list = []
    for record in sampled:
        if record[3] not in freq_dict:
            freq_dict[record[3]] = 1
        else:
            freq_dict[record[3]] += 1
    print('Frequency of pulse rates is: ')
    print(freq_dict)
    #  for key in freq_dict:
    #    freq_list.append([key,freq_dict[key]])
    #  print(freq_list)
    plt.bar(list(freq_dict.keys()), freq_dict.values(), color='b')
    plt.xlabel('Pulse')
    plt.ylabel('Frequency')
    plt.title('Frequency Histogram of Pulse Rates')
    plt.xlim(55, 100)
    plt.ylim(0, max(freq_dict.values()) + 0.5)
    plt.show()
    return freq_dict


def healthAnalyzer(n, x):
    multi_list = []
    freq_hr = {}
    for record in myHealthcare(n):
        if record[3] == x:
            multi_list.append([record])
            if record[2] not in freq_hr:
                freq_hr[record[2]] = 1
            else:
                freq_hr[record[2]] += 1
    plt.bar(list(freq_hr.keys()), freq_hr.values(), color='m')
    plt.xlabel('Heart Rate')
    plt.ylabel('Frequency')
    plt.title('Frequency Histogram of Heart Rate for a given pulse rate value')
    plt.xlim(55, 100)
    plt.ylim(0, max(freq_hr.values()) + 0.5)
    plt.show()
    print('All the records associated with that pulse rate value are:')
    print(str(multi_list))
    return multi_list


def benchmarking(f):
    n = [1000, 2500, 5000, 7500, 10000]
    run_time = []
    for el in n:
        t = time.time()
        f(el)
        dt = time.time() - t
        run_time.append(dt)
    plt.plot(n, run_time, marker='o')
    plt.title('Dependency of Running Time over the Number of Records')
    plt.xlabel('Number of Records')
    plt.ylabel('Time (sec)')
    plt.xlim(0, 11000)
    plt.show()


