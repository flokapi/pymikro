

import pymikro



def demoOutputState(maschine):
	print('Press any button, pad, the encoder, or strip line...')

	while True:
		r = maschine.readCmd()
		if r:
			print(r)


if __name__ == '__main__':
	maschine = pymikro.MaschineMikroMk3()

	demoOutputState(maschine)

