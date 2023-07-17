

import pymikro
import time



def demoPadsBtns(maschine):
	maschine.setLight('button', 'stop', 3)
	maschine.updLights()

	while True:
		r = maschine.readCmd()
		if r:
			#print(r)
			if r['cmd'] =='pad':
				val = r['pad_val']
				nb = r['pad_nb']

				if r['pressed']:
					maschine.setLight('pad', nb , 2,'violet')
					maschine.updLights()

				if r['released']:
					maschine.setLight('pad', nb , 1,'green')
					maschine.updLights()

				print('X'*int(val/10))

			if r['cmd'] == 'btn':
				if 'stop' in r['btn_pressed']:
					maschine.setLights({})
					maschine.updLights()



if __name__ == '__main__':
	maschine = pymikro.MaschineMikroMk3()

	demoPadsBtns(maschine)

