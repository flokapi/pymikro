import pymikro
import time
import datetime



def demoScreen(maschine):
	for i in range(11):
		maschine.setScreen(' '*6+f'{10-i}', size=28)
		time.sleep(0.1)

	while True:
		timeStr = datetime.datetime.now().strftime('%H:%M:%S')
		maschine.setScreen(f"Hello World!\n{timeStr}")

		time.sleep(1)
		
		
if __name__ == '__main__':
	maschine = pymikro.MaschineMikroMk3()
	demoScreen(maschine)
