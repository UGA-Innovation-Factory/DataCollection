import time
from Communication.SocketConnection import SocketConnection

class csharpConnect:
    def __init__(self, getterFunction, timeOut : float, socket : int, ip="localhost") -> None:
        #Getter function should give a list of the values to be sent to unity
        self.getter = getterFunction
        self.timeOut = timeOut
        self.socket = socket
        self.ip = ip

    def getValuesFromGetterToString(self) -> str:
        return str(self.getter())[1:-1]

    def run(self):
        while True:
            try:
                csharp_out_socket = SocketConnection(self.ip, self.socket)
                connected = csharp_out_socket.connect()
                if connected:
                    print(f"~ Socket {self.socket} Connected! ~")

                    while True:
                        time.sleep(self.timeOut)
                        results = str(self.getter())[1:-1]
                        #print(results)
                        if connected:
                            message = results.encode('ASCII')
                            connected.send(message)
                        else: 
                            print(f"Socket {self.socket}: Not connected to Unity.")
                            break
                        
            except Exception as e:
                print(f"Socket {self.socket}: Connection Error.")
                print(e)
            time.sleep(1)
