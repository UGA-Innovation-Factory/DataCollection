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

    iterator = fakeDataGen()
    getter = (lambda : next(iterator))
    time_out = 0.05

    hqt_client = HiveClient()
    hqt_client.connect_and_loop_start()
    try:
        while True:
            time.sleep(time_out)
            message = str(getter())[:-1]
            print(message)
            hqt_client.publish("DT/UR10", message)
    except KeyboardInterrupt:
        print("Stopping...")
        hqt_client.loop_stop_and_disconnect()