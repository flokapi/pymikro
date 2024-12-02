from hid import Device


class HidDevice:
    vid: int
    pid: int
    hid: Device

    def __init__(self, vid_: str, pid_: str) -> None:
        self.vid = int(vid_, 16)
        self.pid = int(pid_, 16)
        self.hid = Device(self.vid, self.pid)

    def show_info(self) -> None:
        print(f"Device manufacturer: {self.hid.manufacturer}")
        print(f"Product: {self.hid.product}")
        print(f"Serial Number: {self.hid.serial}")
        print(f"VID: {self.vid}")
        print(f"PID: {self.pid}")

    def read(self) -> list[int]:
        bufSize = 1000
        timeout = 10
        b = self.hid.read(bufSize, timeout)
        return list(b)

    def write(self, data):
        self.hid.write(bytes(data))
