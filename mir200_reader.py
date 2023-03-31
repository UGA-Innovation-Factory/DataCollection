import json
import requests
import time
from csharpConnect import csharpConnect
from HiveMQConnect import HiveClient

ip = "172.22.114.160"
host = "http://" + ip + "/api/v2.0.0"
head = {}
head['accept'] = 'application/json'
head['Authorization'] = 'Basic dWdhaWYtYWRtaW46NzE0YTBiZmJkZjBlMDllMzliZjVkMGFhNGMxNGJjYzY1OTBhMmY4YzJkYWZhOWI5ZGIwZDczNGIwMzljMDUyNg=='
head['Accept-Language'] = 'en_US'

#get_status = requests.get(host, 'status')
#get_status = requests.get(host + '/status', headers= head).json()["position"]
#print(get_status)

def getMirPositions() -> tuple:
    get_status_positions = requests.get(host + '/status', headers= head).json()["position"]
    positions_tuple = tuple(get_status_positions.values())
    #print(positions_tuple)
    return positions_tuple

def getMirData() -> tuple:
    get_status = requests.get(host + '/status', headers= head).json()
    get_status_positions = get_status["position"]
    get_status_velocity = get_status['velocity']
    #print(get_status_velocity)
    data_tuple = (cutFloat(get_status_positions['x']), cutFloat(get_status_positions['y']), cutFloat(get_status_positions['orientation']))
    data_tuple += (cutFloat(get_status['battery_percentage']),)
    data_tuple += (cutFloat(get_status_velocity['linear']), cutFloat(get_status_velocity['angular'])) + (get_status['state_text'],)
    #print(data_tuple)
    return data_tuple

def fakeDataGen():
    while True:
        with open("MirOutput.txt", "r") as file:
            while True:
                text = file.readline()
                if not text:
                    break
                yield " " + text

#iterator = fakeDataGen()
#def getFakeMirData():
#    return next(iterator)

def cutFloat(f):
    return float('%.3f'%f)

# Used to record movement
def writeToFile(fileLines : "list[str]"):
    print("Saving to file")
    with open("MirOutput.txt", "x") as file:
        file.writelines(fileLines)

if __name__ == '__main__':
    getter = getMirData
    #getter = getFakeMirData
    time_out = 0.1

    #mir200socket = csharpConnect(getter, time_out, 12200)
    #mir200socket.run()

    #file_lines = [] # Used to record movement

    hqt_client = HiveClient()
    hqt_client.connect_and_loop_start()
    try:
        while True:
            time.sleep(time_out)
            message = str(getter())[1:-1]
            print(message)
            #file_lines.append(message + "\n") # Used to record movement
            hqt_client.publish("DT/MIR200", message)
    except KeyboardInterrupt:
        hqt_client.loop_stop_and_disconnect()
        #writeToFile(file_lines) # Used to record movement

