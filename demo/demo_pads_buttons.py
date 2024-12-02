import pymikro


def demo_pads_btns(maschine):
    maschine.lights.set_all({})
    maschine.lights.update()

    # maschine.lights.set_light("button", "stop", 3)
    maschine.lights.update()

    while True:
        r = maschine.read_cmd()
        if r:
            # print(r)
            if r["cmd"] == "pad":
                val = r["pad_val"]
                nb = r["pad_nb"]

                if r["pressed"]:
                    maschine.lights.set("pad", nb, 2, "violet")
                    maschine.lights.update()

                if r["released"]:
                    maschine.lights.set("pad", nb, 1, "green")
                    maschine.lights.update()

                print("X" * int(val / 10))

            if r["cmd"] == "btn":
                if "stop" in r["btn_pressed"]:
                    maschine.lights.set_all({})
                    maschine.lights.update()


if __name__ == "__main__":
    maschine = pymikro.MaschineMikroMk3()

    demo_pads_btns(maschine)
