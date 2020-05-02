import sys
import math
import matplotlib.pyplot as plt


def distribution_moment(p, q):  # Mq
    result = 0
    for pi in p:
        if pi != 0:
            result += pi**q
    return result


def event_cells_probability(table, cell_size, N):
    p = []

    for i in range(len(table))[::cell_size]:
        for j in range(len(table[i]))[::cell_size]:
            local_p = 0
            for di in range(cell_size):
                for dj in range(cell_size):
                    if i + di < len(table) and j + dj < len(table[i]):
                        local_p += table[i + di][j + dj]
            local_p = float(local_p / N)
            p.append(local_p)

    return p


def t(table, q):  # t(q)
    N = 0
    for line in table:
        for j in line:
            N += j
    p1 = event_cells_probability(table, 1, N)
    p2 = event_cells_probability(table, 2, N)
    M1 = distribution_moment(p1, q)
    M2 = distribution_moment(p2, q)
    if M1 == M2 == 0:
        return 0
    x1 = math.log(1/len(table))
    x2 = math.log(2/len(table))
    y1 = math.log(M1)
    y2 = math.log(M2)
    return (y2 - y1) / (x2 - x1)


def singularity_index(table, q):
    N = 0
    for line in table:
        for j in line:
            N += j
    p1 = event_cells_probability(table, 1, N)
    p2 = event_cells_probability(table, 2, N)
    M1 = distribution_moment(p1, q - 1)
    M1q = distribution_moment(p1, q)
    M2 = distribution_moment(p2, q - 1)
    M2q = distribution_moment(p2, q)
    return q * (M2 / M2q - M1 / M1q) * (math.log(2 / len(table)) - math.log(1 / len(table)))


def multifractal_spectrum_function(table, q, alpha):
    return q * alpha + t(table, q)


#file_template = input('Enter file template\n')
file_template = 'central_America_1month'
input_file = open(file_template + '_table.txt', 'r')
height = int(input_file.readline()[:-1:])
width = int(input_file.readline()[:-1:])
eps = float()


if height != width:
    print('Dimensions are not equal\n')
    sys.exit()

draw_table = []
for i in range(height):
    draw_table.append(input_file.readline()[:-1:].split(' '))

for i in range(len(draw_table)):
    for j in range(len(draw_table[i])):
        draw_table[i][j] = int(draw_table[i][j])

q = [i * 0.1 for i in range(-20, 20)]
a = [singularity_index(draw_table, x) for x in q]
f = [multifractal_spectrum_function(draw_table, q[i], a[i]) for i in range(len(a))]

fig, ax = plt.subplots()
ax.set_xlabel('alpha')
ax.set_ylabel('f(alpha)')
plt.plot(a, f)
plt.show()
