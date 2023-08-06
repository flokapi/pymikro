

import pymikro
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


class AnimatedGraph:
    def __init__(self):
        self.buf = []

        self.initMaschine()
        self.initGraph()

    def initMaschine(self):
        self.maschine = pymikro.MaschineMikroMk3()

    def initGraph(self):
        style.use('fivethirtyeight')

        fig = plt.figure()
        self.ax1 = fig.add_subplot(1,1,1)

        ani = animation.FuncAnimation(fig, self.animate, interval=1)
        plt.show()

    def updateBuf(self):
        count = 0
        while True:
            cmd = self.maschine.readCmd()
            if cmd and cmd['cmd'] == 'pad':
                self.buf.append(cmd['pad_val'])

                if len(self.buf) > 500:
                    self.buf.pop(0)

            count += 1
            if cmd == None or count > 100:
                break

    def animate(self, _):
        self.updateBuf()

        xs = [x for x in range(len(self.buf))]
        ys = self.buf

        self.ax1.clear()
        self.ax1.plot(xs, ys)




if __name__ == '__main__':
    graph = AnimatedGraph()