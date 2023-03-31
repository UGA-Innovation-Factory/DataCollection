from HiveMQConnect import HiveClient
import time


def fakeDataGen():
    while True:
        with open("MirOutput.txt", "r") as file:
            while True:
                text = file.readline()
                if not text:
                    break
                yield text


if __name__ == '__main__':

    iterator = fakeDataGen()
    getter = (lambda : next(iterator))
    time_out = 0.1

    hqt_client = HiveClient()
    hqt_client.connect_and_loop_start()
    try:
        while True:
            time.sleep(time_out)
            message = str(getter())[:-1]
            print(message)
            hqt_client.publish("DT/MIR200", message)
    except KeyboardInterrupt:
        print("Stopping...")
        hqt_client.loop_stop_and_disconnect()