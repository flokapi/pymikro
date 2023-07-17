

import pymikro
import time



def demoLights(maschine):
    state = {
        'button': {
            'stop': {'val': 1},
        },
        'strip': {
            1: {'val': 3, 'color': 'blue'},
        },
        'pad': {
            1: {'val': 3, 'color': 'purple'},
        }
    }
    maschine.setLights(state)

    maschine.setLight('pad', 6, 3, 'orange')
    maschine.setLight('strip', 5, 3, 'green')
    maschine.setLight('button', 'notes', 3)
    maschine.updLights()


def demoScreen(maschine):
    maschine.setScreen("Hello World!\nIt's working")


def demoBtnPad(maschine):
    while True:
        cmd = maschine.readCmd()
        if cmd:
            if cmd['cmd'] == 'pad':
                print('Pad number {} pressed with value: {}'.format(cmd['pad_nb'], cmd['pad_val']))
            if cmd['cmd'] == 'btn':
                print('Buttons pressed: {}'.format(cmd['btn_pressed']))


if __name__ == '__main__':
    maschine = pymikro.MaschineMikroMk3()

    demoLights(maschine)
    demoScreen(maschine)
    demoBtnPad(maschine)