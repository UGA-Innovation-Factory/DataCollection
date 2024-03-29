import time, sys, json, os
from HiveMQConnect import HiveClient

from rtde.UR10RTDE import UR10RTDE
#rtde from: https://github.com/UniversalRobots/RTDE_Python_Client_Library


if __name__ == '__main__':
    dirpath = os.path.dirname(os.path.realpath(__file__))
    while True:
        try:
            print("Starting up...")

            UR10_ip = "172.22.114.160"
            frecuency = 50
            config_file = os.path.join(dirpath, "rtde/record_configuration.xml")
            ur10_connection = UR10RTDE(host=UR10_ip, frequency=frecuency, config_file=config_file)
            ur10_connection.connect()

            time_out = 1/frecuency

            hqt_client = HiveClient()
            hqt_client.connect_and_loop_start()

            print("Running...")
            try:
                while True:
                    time.sleep(time_out)
                    message = json.dumps(ur10_connection.read_dict())
                    #print(message)
                    hqt_client.publish("DT/UR10", message)
            except KeyboardInterrupt:
                print("Stopping...")
                hqt_client.loop_stop_and_disconnect()
                ur10_connection.disconnect()
                sys.exit()
        
        except Exception as e:
            print(e)
            print("Trying again in 3 seconds...")
            time.sleep(3)
        
    



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

