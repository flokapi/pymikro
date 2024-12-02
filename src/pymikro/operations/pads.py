class Pads:
    pad_order: list[int]

    def __init__(self, pad_order_: list[int]) -> None:
        self.pad_order = pad_order_

    def decode(self, raw_cmd: list[int]) -> dict | None:
        if len(raw_cmd) > 4 and raw_cmd[0] == 2:
            info = {}
            info["cmd"] = "pad"

            info["pad_nb"] = self.pad_order[raw_cmd[1]]
            info["pad_val"] = (raw_cmd[2] & 0x0F) * 256 + raw_cmd[3]

            ctrl = raw_cmd[2] & 0xF0
            info["touched"] = ctrl == 0x40
            info["pressed"] = ctrl == 0x10
            info["released"] = (ctrl == 0x20) or (ctrl == 0x30)

            return info

        return None
