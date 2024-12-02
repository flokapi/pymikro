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
        settings_file_path = self._get_path(SETTINGS_FILE_NAME)
        font_file_path = self._get_path(FONT_FILE_NAME)

        self._load_settings(settings_file_path)

        vid, pid = self.settings["vid"], self.settings["pid"]
        self.hid = HidDevice(vid, pid)

        self.buttons = Buttons(self.settings["button"]["order"])
        self.pads = Pads(self.settings["pad"]["order"])
        self.lights = Lights(self.settings, self.hid)
        self.screen = Screen(self.hid, font_file_path)

    def _get_path(self, file_name_) -> str:
        return os.path.join(os.path.dirname(__file__), file_name_)

    def _load_settings(self, file_path_: str) -> None:
        with open(file_path_) as f:
            self.settings = json.load(f)

    def read_cmd(self) -> dict | None:
        rawCmd = self.hid.read()
        decodeFuncs = [self.buttons.decode, self.pads.decode]
        for dec in decodeFuncs:
            cmd = dec(rawCmd)
            if cmd is not None:
                return cmd

        return None
