# Using https://github.com/ErwinLutke/UR-Interface Modbus communication code
# UR Register addresses found on https://s3-eu-west-1.amazonaws.com/ur-support-site/16377/ModBus%20server%20data.pdf

from ModbusTCP import ModbusTCP
import time
import math

class UR10_reader:
    def __init__(self, host) -> None:
        self.modbusTCP = ModbusTCP(host, 502)
        pass

    def get_join_angles(self, tries=0):
        """
        Connects with the Modbus server to requests Cartesian data of the TCP
        :return: Readable cartesian data of TCP, vector in mm, axis in radials
        """
        if tries>10:
            print("Modbus Error: Failed")
            return 0, 0, 0, 0, 0, 0

        packet = self.modbusTCP.read_holding_registers(270, quantity=6)

        if packet is None:
            time.sleep(0.01)
            print(f"Modbus Error #{tries}: retrying")
            return self.get_join_angles(tries+1)
        else:
            base = self._format_degrees(packet[9:11])
            shoulder = self._format_degrees(packet[11:13])
            elbow = self._format_degrees(packet[13:15])
            wrist_1 = self._format_degrees(packet[15:17])
            wrist_2 = self._format_degrees(packet[17:19])
            wrist_3 = self._format_degrees(packet[19:21])
            return base, shoulder, elbow, wrist_1, wrist_2, wrist_3

    def get_UR_register_info_block(self, address_start = 270, extra_format = None, tries=0):
        """
        
        """
        if tries>10:
            print("Modbus Error: Failed")
            return 0, 0, 0, 0, 0, 0

        packet = self.modbusTCP.read_holding_registers(address_start, quantity=6)

        if packet is None:
            time.sleep(0.01)
            print(f"Modbus Error #{tries}: retrying")
            return self.get_UR_register_info_block(address_start, extra_format ,tries+1)
        else:
            first = self._format(packet[9:11], extra_format)
            second = self._format(packet[11:13], extra_format)
            third = self._format(packet[13:15], extra_format)
            fourth = self._format(packet[15:17], extra_format)
            fifth = self._format(packet[17:19], extra_format)
            sixth = self._format(packet[19:21], extra_format)
            return first, second, third, fourth, fifth, sixth

    @staticmethod
    def _format_degrees(d):
        """Formats signed integers to unsigned float
        :param d: signed integer to format
        :return: unsigned float
        """
        d = d.hex()
        d_i = int(d, 16)
        d_f = 0

        if d_i < 32768:
            d_f = float(d_i)
        if d_i > 32767:
            d_i = 65535 - d_i
            d_f = float(d_i) * -1
        #return d_f
        return math.degrees( d_f / 1000 )

    @staticmethod
    def _format(d, extra=None):
        """Formats signed integers to unsigned float
        :param d: signed integer to format
        :return: unsigned float
        """
        d = d.hex()
        d_i = int(d, 16)
        d_f = 0

        if d_i < 32768:
            d_f = float(d_i)
        if d_i > 32767:
            d_i = 65535 - d_i
            d_f = float(d_i) * -1
        if extra:
            d_f = extra(d_f)
        return d_f


    #def _degrees(self, d):
    #    """Formats signed integers to unsigned float, and transforms them to a proper angle in degrees
    #    """
    #    return math.degrees(self._format(d) / 1000)

    def get_UR_info(self):
        joint_angle = self.get_UR_register_info_block(270, lambda x : float('%.3f'%(math.degrees(x / 1000))))
        joint_current = self.get_UR_register_info_block(290)
        joint_temp = self.get_UR_register_info_block(300)
        return joint_angle + joint_current + joint_temp