import pymikro


def demo_lights(maschine):
    state = {
        "button": {
            "stop": {"val": 1},
        },
        "strip": {
            1: {"val": 3, "color": "blue"},
        },
        "pad": {
            1: {"val": 3, "color": "purple"},
        },
    }
    maschine.lights.set_all(state)

    maschine.lights.set("pad", 6, 3, "orange")
    maschine.lights.set("strip", 5, 3, "green")
    maschine.lights.set("button", "notes", 3)
    maschine.lights.update()


def demo_screen(maschine):
    maschine.screen.set("Hello World!\nIt's working")


def demo_btn_pad(maschine):
    while True:
        cmd = maschine.read_cmd()
        if cmd:
            if cmd["cmd"] == "pad":
                print(
                    "Pad number {} pressed with value: {}".format(
                        cmd["pad_nb"], cmd["pad_val"]
                    )
                )
            if cmd["cmd"] == "btn":
                print("Buttons pressed: {}".format(cmd["btn_pressed"]))


if __name__ == "__main__":
    maschine = pymikro.MaschineMikroMk3()

    demo_lights(maschine)
    demo_screen(maschine)
    demo_btn_pad(maschine)
