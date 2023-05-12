from HiveMQConnect import HiveClient
import time


def fakeDataGen():
    while True:
        with open("UR10Output.txt", "r") as file:
            while True:
                text = file.readline()
                if not text:
                    break
                yield text


if __name__ == '__main__':
    print("Starting up...")

    iterator = fakeDataGen()
    getter = (lambda : next(iterator))

    time_out = 0.02

    hqt_client = HiveClient()
    hqt_client.connect_and_loop_start()

    print("Running...")
    try:
        while True:
            time.sleep(time_out)
            message = getter()
            print(message)
            hqt_client.publish("fake/UR10", message)
    except KeyboardInterrupt:
        print("Stopping...")
        hqt_client.loop_stop_and_disconnect()