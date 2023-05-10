import rtde.rtde as rtde
import rtde.rtde_config as rtde_config


class UR10Listener:
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
            raise Exception("Unable to configure output") #logging.error("Unable to configure output")
        
        # start data synchronization
        if not self.con.send_start():
            raise Exception("Unable to start synchronization") #logging.error("Unable to start synchronization")


    # Disconnect from robot
    def disconnect(self):
        """Disconnect from the UR10 robot"""
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
        except rtde.RTDEException:
            self.con.disconnect()
            raise Exception("Unable to read from robot")
        
    # Read data from robot and parse output to JSON
    def read_dict(self) -> dict:
        """Reads the current state of the UR10 robot and returns it as a dictionary"""
        return vars(self.read())
