class Buttons:
    button_order: list[str]
    last_encoder_pos: int | None

    def __init__(self, button_order_: list[str]) -> None:
        self.button_order = button_order_
        self.last_encoder_pos = None

    def _get_pressed_btns(self, raw_cmd: list[int]) -> dict:
        btn_bytes = bytes(raw_cmd[1:6])
        btn_val = int.from_bytes(btn_bytes, byteorder="little")

        btns = []
        for btn_index in range(len(self.button_order)):
            if (btn_val % 2) == 1:
                btns.append(self.button_order[btn_index])
            btn_val = btn_val >> 1

        return {"btn_pressed": btns}

    def _get_encoder_info(self, raw_cmd: list[int]) -> dict:
        info = {}

        encoder_pos = raw_cmd[7]
        encoder_move = 0
        if self.last_encoder_pos is not None:
            diff = encoder_pos - self.last_encoder_pos
            if abs(diff - 16) < abs(diff):
                encoder_move = diff - 16
            elif abs(diff + 16) < abs(diff):
                encoder_move = diff + 16
            else:
                encoder_move = diff
        self.last_encoder_pos = encoder_pos

        info["encoder_pos"] = encoder_pos
        info["encoder_move"] = encoder_move
        info["encoder_touched"] = raw_cmd[6] == 1

        return info

    def _get_strip_value(self, raw_cmd: list[int]) -> dict:
        info = {}

        info["strip_pos_1"] = raw_cmd[10]
        info["strip_pos_2"] = raw_cmd[12]
        # info['strip_time'] = rawCmd[9]*256 + rawCmd[8]

        return info

    def decode(self, raw_cmd: list[int]) -> dict | None:
        if len(raw_cmd) > 10 and raw_cmd[0] == 1:
            ret = {"cmd": "btn"}

            ret.update(self._get_pressed_btns(raw_cmd))
            ret.update(self._get_encoder_info(raw_cmd))
            ret.update(self._get_strip_value(raw_cmd))

            return ret

        return None
