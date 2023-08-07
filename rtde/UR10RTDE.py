import rtde.rtde as rtde
import rtde.rtde_config as rtde_config


class UR10RTDE:
    """This class is a wrapper for the rtde library to be used with the UR10 robot hand. While the rtde library is capable of both reading the state and sending commands back, this class is only used for reading the state of the robot."""
    def __init__(self, host : str, frequency : int = 125, config_file : str = "record_configuration.xml", buffered : bool = False, binary : bool = False):
        self.host = host
        self.port = 30004
        self.frequency = frequency
        self.config_file = config_file
        self.buffered = buffered
        self.binary = binary

        # Load configuration file
        conf = rtde_config.ConfigFile(self.config_file)
        self.output_names, self.output_types = conf.get_recipe("out")

        # initialize RDTE
        self.con = rtde.RTDE(self.host, self.port)


    # Connect to robot
    def connect(self):
        """Initialize connection to the UR10 robot"""
        self.con.connect()
        # get controller version
        self.con.get_controller_version()

        # setup recipes
        if not self.con.send_output_setup(self.output_names, self.output_types, frequency=self.frequency):
            raise rtde.RTDEException("Unable to configure output") #logging.error("Unable to configure output")
        
        # start data synchronization
        if not self.con.send_start():
            raise rtde.RTDEException("Unable to start synchronization") #logging.error("Unable to start synchronization")


    # Disconnect from robot
    def disconnect(self):
        """Disconnect from the UR10 robot"""
        if self.is_connected():
            self.con.send_pause()
            self.con.disconnect()
        print("UR10 disconnected")


    # Connection status
    def is_connected(self):
        """Returns True if connected to the UR10 robot"""
        return self.con.is_connected()
    

    # Read data from robot
    def read(self):
        """Reads the current state of the UR10 robot and returns a DataObject"""
        try:
            if self.buffered:
                return self.con.receive_buffered(self.binary)
            return self.con.receive(self.binary)
        except rtde.RTDEException as err:
            self.con.disconnect()
            raise err
        
    # Read data from robot and parse output to JSON
    def read_dict(self) -> dict:
        """Reads the current state of the UR10 robot and returns it as a dictionary"""
        r = self.read()
        if r is None:
            return None
        return vars(r)

    # Read data from robot and parse output to a flattened JSON dictionary
    def read_dict_flat(self) -> dict:
        """Reads the current state of the UR10 robot and returns it as a flattened dictionary"""
        y = self.read_dict()
        if y is None:
            return None
        out = {}

        def flatten(x, name=""):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + "_")
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + "_")
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out
