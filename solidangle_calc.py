
import matplotlib.pyplot as plt
import numpy as np
from numpy import radians, cos, pi

data_20 = np.array([[20, 0, 1.5579454625034739],
                    [20, 10, 1.6456083018539565],
                    [20, 20, 1.7021373852319308],
                    [20, 30, 1.4371430386539854],
                    [20, 40, 1.1905999020961957],
                    [20, 50, 1.1754393181105072],
                    [20, 60, 0.9676624060389081]])

data_30 = np.array([[30, 0, 2.1885888100553696],
                    [30, 10, 2.128793769341387],
                    [30, 20, 2.0557360925714536],
                    [30, 30, 1.8482868102385914],
                    [30, 40, 1.6295606034673293],
                    [30, 50, 1.4540197852599812],
                    [30, 60, 1.1895541212326641]])

data_50 = np.array([[50, 0, 1.7425996044451257],
                    [50, 10, 1.7069204792651576],
                    [50, 20, 1.4342129635634693],
                    [50, 30, 1.4566655937985602],
                    [50, 40, 1.2374842137194564],
                    [50, 50, 1.1809896108244204],
                    [50, 60, 0.9280275762381395]])


data_100 = np.array([[100, 0, 0.8944547337928115],
                    [100, 10, 0.8580104190237179],
                    [100, 20, 0.8082458216056045],
                    [100, 30, 0.7373796788813632],
                    [100, 40, 0.5896596409716086],
                    [100, 50, 0.5967613247594137],
                    [100, 60, 0.5232359986392423]])

solid_angles = [cos(radians(0))-cos(radians(5)),
                cos(radians(5))-cos(radians(15)),
                cos(radians(15))-cos(radians(25)),
                cos(radians(25))-cos(radians(35)),
                cos(radians(35))-cos(radians(45)),
                cos(radians(45))-cos(radians(55)),
                cos(radians(55))-cos(radians(65))]

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
plots = [ax1, ax2, ax3, ax4]
i = 0

with open('solidangle_data.txt', 'w') as f:
    f.write('energy, angle, weighted effective area\n')
    for data in [data_20, data_30, data_50, data_100]:

        angles = data[:, 1]
        energy = data[0, 0]
        effective_area = data[:, 2]

        temp = 2 * pi * (solid_angles * effective_area)

        for row in range(7):
            f.write('{}, {}, {}\n'.format(energy, data[row, 1], temp[row]))
        f.write('\n')

        plots[i].plot(angles, effective_area, 'o', angles, temp, 's')
        plots[i].set_title(r'COMPTEL Effective Area {} MeV'.format(energy), size=12)
        plots[i].grid(True)
        plots[i].legend([r'unweighted', r'weighted by $\displaystyle\Omega$'],
                        fontsize=8, numpoints=1, markerscale=.8)

        i += 1

plt.savefig('solidangle_effarea')
