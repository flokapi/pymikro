from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


from ..hid_device import HidDevice


class Screen:
    font_file_path: str
    hid: HidDevice

    def __init__(self, hid_: HidDevice, font_file_path_: str) -> None:
        self.hid = hid_
        self.font_file_path = font_file_path_

    def _get_bit_img(self, text: str, size: int):
        img = Image.new("1", (128, 32))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font_file_path, size)
        text_sp = text.split("\n") + [""]
        draw.text((0, 0), text_sp[0], 1, font=font)
        draw.text((0, 16), text_sp[1], 1, font=font)
        return img

    def _get_buffer(self, img) -> list[int]:
        buf = [0xFF] * 512
        for i in range(128):
            for line in range(4):
                byte_val = 0x00
                for bit in range(8):
                    byte_val = byte_val << 1
                    pix_val = img.getpixel((i, (8 * line) + (7 - bit)))
                    if pix_val == 0:
                        byte_val += 1
                buf[128 * line + i] = byte_val
        return buf

    def _write_buf(self, buf: list[int]) -> None:
        header_hi = [0xE0, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x02, 0x00]
        header_lo = [0xE0, 0x00, 0x00, 0x02, 0x00, 0x80, 0x00, 0x02, 0x00]
        self.hid.write(header_hi + buf[:256])
        self.hid.write(header_lo + buf[256:])

    def set(self, text: str, size: int = 14):
        img = self._get_bit_img(text, size)
        buf = self._get_buffer(img)
        self._write_buf(buf)
