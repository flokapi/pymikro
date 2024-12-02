import os
import json

from .hid_device import HidDevice

from .operations import Buttons, Pads, Lights, Screen


SETTINGS_FILE_NAME = "maschine_mikro_mk3.json"
FONT_FILE_NAME = "DejaVuSans.ttf"


class MaschineMikroMk3:
    settings: dict
    hid: HidDevice
    buttons: Buttons
    pads: Pads
    lights: Lights
    screen: Screen

    def __init__(self) -> None:
        self.lights_state = {}
        self._load_settings(SETTINGS_FILE_NAME)

        vid, pid = self.settings["vid"], self.settings["pid"]
        self.hid = HidDevice(vid, pid)

        self.buttons = Buttons(self.settings["button"]["order"])
        self.pads = Pads(self.settings["pad"]["order"])
        self.lights = Lights(self.settings, self.hid)
        self.screen = Screen(self.hid, self._get_path(FONT_FILE_NAME))

    def _load_settings(self, fileName: str) -> None:
        filePath = self._get_path(fileName)
        with open(filePath) as f:
            self.settings = json.load(f)

    def _get_path(self, fileName) -> str:
        return os.path.join(os.path.dirname(__file__), fileName)

    def read_cmd(self) -> dict | None:
        rawCmd = self.hid.read()
        decodeFuncs = [self.buttons.decode, self.pads.decode]
        for dec in decodeFuncs:
            cmd = dec(rawCmd)
            if cmd is not None:
                return cmd

        return None
