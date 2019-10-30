import math
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


print('Exercise 1')


################################################################################
#                                Exercise 1) a)                                #
################################################################################


print('a) Run Kolmogorov-Smirnov test to determine distribution of time between client arrivals')


with open('../data/datosTP2EJ1.txt') as my_file:
    time_between_arrivals = sorted([float(line) for line in my_file.readlines()])


def exponential_cdf(x, scale):
    return 1 - math.e ** (- x / scale)


def kolmogorov_smirnov_test(scale):
    significance_level = 0.01
    max_distance = math.sqrt(
        (-1 / (2 * len(time_between_arrivals))) *
        math.log(significance_level / 2)
    )
    rejected = False
    for index, time in enumerate(time_between_arrivals):
        actual_value = exponential_cdf(time, scale=scale)
        lower_value = index / len(time_between_arrivals)
        upper_value = (index + 1) / len(time_between_arrivals)
        distance = max(
            abs(upper_value - actual_value),
            abs(lower_value - actual_value)
        )
        if distance > max_distance:
            rejected = True
            break
    if rejected:
        print(f'    Exponential distribution with scale of {scale} seconds discarded')
    else:
        print(f'    Exponential distribution with scale of {scale} seconds accepted')


kolmogorov_smirnov_test(scale=180)
kolmogorov_smirnov_test(scale=240)

################################################################################
#                                Exercise 1) b)                                #
################################################################################


print('b) Simulate 1000 days of new ATM')


seconds_in_hour = 3600
day_in_seconds = 24 * seconds_in_hour
thousand_days_in_seconds = 1000 * day_in_seconds
arrival_timestamps = [np.random.exponential(scale=180)]
while arrival_timestamps[-1] < thousand_days_in_seconds:
    arrival_timestamps.append(arrival_timestamps[-1] + np.random.exponential(scale=180))

max_banknote_count = 2000
balance = 0
next_available_timestamp = 0

successful_operations = []
unsuccessful_operations = []
log_operations = True
next_day = 0

total_client_time = 0
client_count = 0
success_count = 0

for arrival in arrival_timestamps:
    if next_available_timestamp > day_in_seconds:
        log_operations = False
    if next_available_timestamp > thousand_days_in_seconds:
        break
    if arrival > next_day:
        balance = max_banknote_count
        next_day += day_in_seconds

    if random.random() < 0.25:
        duration = np.random.exponential(scale=300)
        amount = 10 + random.random() * 100
    else:
        duration = np.random.exponential(scale=90)
        amount = -(3 + random.random() * 47)
    wait_time = -max(0, next_available_timestamp - arrival)
    new_balance = balance + amount
    next_available_timestamp = arrival + wait_time + duration
    total_client_time += wait_time + duration
    client_count += 1
    if 0 <= new_balance <= max_banknote_count:
        balance = new_balance
        success_count += 1
        if log_operations:
            successful_operations.append((next_available_timestamp, balance))
    else:
        if log_operations:
            unsuccessful_operations.append((next_available_timestamp, balance))

################################################################################
#                                Exercise 1) c)                                #
################################################################################


print('c) Graph banknotes in ATM in the first day')


marker_size = 1.1
plt.scatter([x[0] / seconds_in_hour for x in successful_operations],
            [y[1] for y in successful_operations], c='blue', s=marker_size)
plt.scatter([x[0] / seconds_in_hour for x in unsuccessful_operations],
            [y[1] for y in unsuccessful_operations], c='red', s=marker_size)
plt.title('Banknotes in ATM in the first day')
plt.xlabel('Time (hours)')
plt.xlim(0, 24)
plt.ylabel('Banknotes in ATM')
plt.ylim(0, max_banknote_count)
blue_patch = mpatches.Patch(color='blue', label='Successful operation')
red_patch = mpatches.Patch(color='red', label='Unsuccessful operation')
plt.legend(handles=[blue_patch, red_patch])

################################################################################
#                                Exercise 1) d)                                #
################################################################################


print(f'd) Mean wait + usage time: {total_client_time / client_count:.1f} minutes')


################################################################################
#                                Exercise 1) e)                                #
################################################################################

current_failure_percentage = 20


print(f'e) Compare to current ATM (current failure rate: {current_failure_percentage}%)')


new_failure_percentage = (1 - success_count / client_count) * 100
if new_failure_percentage < current_failure_percentage:
    conclusion = 'ATM should be changed'
else:
    conclusion = 'ATM should not be changed'
print(f'    {conclusion} since new failure rate is {new_failure_percentage:.1f}%')

plt.show()
