import time, sys, json
from HiveMQConnect import HiveClient

from rtde.rtde_ur10_connection import UR10Listener
#rtde from: https://github.com/UniversalRobots/RTDE_Python_Client_Library

# def fakeDataGen():
#     while True:
#         with open("UR10Output.txt", "r") as file:
#             while True:
#                 text = file.readline()
#                 if not text:
#                    break
#                yield " " + text


if __name__ == '__main__':
    print("Starting up...")

    UR10_ip = "172.22.114.160"
    frecuency = 10
    config_file = "rtde/record_configuration.xml"
    ur10_connection = UR10Listener(host=UR10_ip, frequency=frecuency, config_file=config_file)
    ur10_connection.connect()

    time_out = 1/frecuency

    hqt_client = HiveClient()
    hqt_client.connect_and_loop_start()

    print("Running...")
    try:
        while True:
            time.sleep(time_out)
            message_dict = ur10_connection.read_dict()
            #print(message_dict)
            hqt_client.publish("DT/UR10", json.dumps(message_dict))
    except KeyboardInterrupt:
        print("Stopping...")
        hqt_client.loop_stop_and_disconnect()
        ur10_connection.disconnect()
        sys.exit(0)
    
    



    # Old code - ignore
    # while True:
    #     try:
    #         print("\nTrying to connect to Unity.")
    #         csharp_out_socket = SocketConnection("localhost", 12345)
    #         connected = csharp_out_socket.connect()
    #         if connected:
    #             print("~ Connected! ~")

    #             while True:
    #                 time.sleep(time_out)
    #                 results = str(getter())[1:-1]
    #                 #print(results)
    #                 if connected:
    #                     message = results.encode('ASCII')
    #                     connected.send(message)
    #                 else: 
    #                     print("Not connected to Unity.")
    #                     break
                    
    #     except Exception as e:
    #         print("Connection Error.")
    #     time.sleep(1)

