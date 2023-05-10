import time, sys
from HiveMQConnect import HiveClient
from rtde.rtde_ur10_connection import UR10Listener

def fakeDataGen():
    while True:
        with open("UR10Output.txt", "r") as file:
            while True:
                text = file.readline()
                if not text:
                    break
                yield " " + text


#iterator = None
# def begin_connection():
#     socket_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = "172.22.114.160"            # Ip addres of the robot
#     port = 30002                     # Portnr of the robot
#     socket_inst.settimeout(0.1)

#     try:
#         socket_inst.connect((host, port))
#         new_angle_reader = UR10_reader(host)
#     except OSError as error:
#         print("UR10 Connection OS error: {0}".format(error))
#         raise OSError(error)
#         #print("~ Sending fake data")
#         #return (lambda : (271, 249, 257, 305, 90, 0, 1,2,3,4,5,6, 11,12,13,14,15,16)), 0.5
#         #iterator = fakeDataGen()
#         #return (lambda : next(iterator)), 0.07

#     socket_inst.sendall(b"set_digital_out(8, False)"+ b"\n") #self.r_disable_magnet()
#     print("Connected")
#     return new_angle_reader.get_UR_info, 0.01  


if __name__ == '__main__':
    #getter, time_out = begin_connection()

    UR10_ip = "172.22.114.160"
    frecuency = 10
    config_file = "rtde/record_configuration.xml"
    ur10_connection = UR10Listener(host=UR10_ip, frequency=frecuency, config_file=config_file)
    ur10_connection.connect()

    time_out = 1/frecuency

    hqt_client = HiveClient()
    hqt_client.connect_and_loop_start()

    try:
        while True:
            time.sleep(time_out)
            message_dict = ur10_connection.read_dict()
            #print(message)
            hqt_client.publish_dict("DT/UR10", message_dict)
    except KeyboardInterrupt:
        print("Stopping...")
        hqt_client.loop_stop_and_disconnect()
        ur10_connection.disconnect()
        sys.exit(0)
    
    




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

