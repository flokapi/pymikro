import pymikro


def demo_output_state(maschine):
    print("Press any button, pad, the encoder, or strip line...")

    while True:
        r = maschine.read_cmd()
        if r:
            print(r)


if __name__ == "__main__":
    maschine = pymikro.MaschineMikroMk3()

    demo_output_state(maschine)
