import pymikro
import time
import datetime


def demo_screen(maschine):
    for i in range(11):
        maschine.screen.set(" " * 6 + f"{10-i}", size=28)
        time.sleep(0.1)

    while True:
        timeStr = datetime.datetime.now().strftime("%H:%M:%S")
        maschine.screen.set(f"Hello World!\n{timeStr}")

        time.sleep(1)


if __name__ == "__main__":
    maschine = pymikro.MaschineMikroMk3()
    demo_screen(maschine)
