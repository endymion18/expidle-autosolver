from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)  # start client
device = client.devices()[0]  # get first connected device

image_path = "images/screen.jpg"


def get_screenshot():
    result = device.screencap()
    with open(image_path, "wb") as fp:
        fp.write(result)


def tap_screen(x: int, y: int):
    device.shell(f"input tap {x} {y}")


def restart_game():
    device.shell(f"input tap {360} {1340}")
