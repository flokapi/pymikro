import pymikro
import time


def demoLights(maschine):
	state = {
		'button': {
			'stop': {'val': 1},
			'chords': {'val': 3},
			'rec': {'val': 4}
		},
		'strip': {
			1: {'color': 'blue', 'val': 2},
			13: {'color': 'red', 'val': 3}
		},
		'pad': {
			1: {'color': 'red', 'val': 1},
			2: {'color': 'blue', 'val': 2},
			3: {'color': 'green', 'val': 3},
			7: {'color': 'purple', 'val': 2},
			14: {'color': 'violet', 'val': 1}
		}
	}

	maschine.setLights(state)
	maschine.updLights()

	time.sleep(1)

	maschine.setLights({})
	maschine.setLight('pad', 5, 2,'violet')
	maschine.setLight('strip', 20, 3,'violet')
	maschine.setLight('strip', 21, 3,'blue')
	maschine.setLight('strip', 22, 3,'green')
	maschine.updLights()

	time.sleep(1)

	maschine.setLight('pad', 6, 3,'violet')
	maschine.updLights()

	time.sleep(1)

	for i in range(25):
		maschine.setLight('strip', i, 3,'violet')
		maschine.updLights()
		#time.sleep(0.01)

	time.sleep(1)

	for brightness in [4, 3, 2, 1, 0]:
		maschine.setLights({})
		for buttonName in maschine.settings['button']['order']:
			maschine.setLight('button', buttonName, brightness)
		maschine.updLights()
		time.sleep(0.1)

	for color in maschine.settings['color'][1:]:
		for brightness in [3, 2, 1, 0]:
			for padNb in range(16):
				maschine.setLight('pad', padNb+1, brightness, color)
			for stripLedNb in range(25):
				maschine.setLight('strip', stripLedNb, brightness, color)

			maschine.updLights()
			time.sleep(0.05)


if __name__ == '__main__':
	maschine = pymikro.MaschineMikroMk3()

	demoLights(maschine)
