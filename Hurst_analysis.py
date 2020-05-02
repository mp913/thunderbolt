# algorithm from ru.wikipedia.ord/wiki/RS-analysis

import math


def get_average(timeline, tetta):
    sum = 0
    for t in range(tetta):
        sum += timeline[t]
    sum /= tetta
    return sum

def accumulated_diviation(timeline, tetta):
    result = 0
    for k in range(tetta):
        result += timeline[k] - get_average(timeline, tetta)
    return result


#file_template = input('Enter file template\n')
file_template = 'tt'

input_file = open(file_template + '_timeline.txt', 'r')
size = int(input_file.readline()[:-1:])
timeline = input_file.readline()[1:-2:].split(',')
for i in range(len(timeline)):
    timeline[i] = int(timeline[i])

maxX = -float('inf')
minX = float('inf')

for tetta in range(len(timeline) + 1):
    local_X = accumulated_diviation(timeline, tetta)
    if local_X < minX:
        minX = local_X
    if local_X > maxX:
        maxX = local_X

R = maxX - minX

standart_deviation = 0
for t in range(len(timeline)):
    standart_deviation += (timeline[t] - get_average(timeline, t + 1)) ** 2
standart_deviation /= len(timeline)
standart_deviation **= 1/2

Hu = math.log(R/standart_deviation, len(timeline))
print(Hu)
