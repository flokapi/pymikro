from ..hid_device import HidDevice


class Lights:
    settings: dict
    hid: HidDevice
    lights_state: dict

    def __init__(self, settings_: dict, hid_: HidDevice) -> None:
        self.settings = settings_
        self.hid = hid_
        self.lights_state = {}

    def set_all(self, state: dict) -> None:
        self.lights_state = state

    def get_all(self) -> dict:
        return self.lights_state

    def set(
        self, elemType: str, elemRef: str, val: int = 4, color: str | None = None
    ) -> None:
        if elemType not in self.lights_state.keys():
            self.lights_state[elemType] = {}

        self.lights_state[elemType][elemRef] = {"val": val, "color": color}

    def _get_elem_nb(self, elemType: str, elemRef: str) -> int | None:
        if elemType in ["pad", "button"]:
            if elemRef == "enter":
                return None
            return self.settings[elemType]["order"].index(elemRef)
        return int(elemRef)

    def _get_color_byte(self, elemType: str, elem: dict) -> int:
        byte = 0x00
        if elemType in ["pad", "strip"]:
            colorNb = self.settings["color"].index(elem["color"])
            if elem["val"] != 0:
                byte = 0x04 * colorNb + elem["val"]
        if elemType == "button":
            byte = self.settings["button"]["brightness"][elem["val"]]
        return byte

    def _set_color(self, buf: list[int], elemType: str, offset: int) -> None:
        if elemType not in self.lights_state.keys():
            return

        for elemRef in self.lights_state[elemType].keys():
            elem = self.lights_state[elemType][elemRef]

            elemNb = self._get_elem_nb(elemType, elemRef)
            if elemNb is not None:
                byte = self._get_color_byte(elemType, elem)
                buf[offset + elemNb] = byte

    def update(self) -> None:
        buf = [0x80] + [0x00] * 90

        self._set_color(buf, "button", 1)
        self._set_color(buf, "pad", 40)
        self._set_color(buf, "strip", 56)

        self.hid.write(buf)
