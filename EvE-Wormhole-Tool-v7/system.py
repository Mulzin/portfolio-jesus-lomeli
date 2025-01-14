from typing import TYPE_CHECKING,List

if TYPE_CHECKING:
    from signatures import ConnectionHole,ExitHole,ScanSite

class SolarSystem:
    '''
    Contains all the info as well as signatures of a solar system
    Attributes:
        id (int): system unique id
        depth (int): how many jumps from the root is the solar system
        title (str): title or name of the system, composed of the id and depth
        class_level (int): difficulty or threat level ofthe system
        scan_site_counter (int): keep track of the scan sites in the system

        connection_list (List["ConnectionHole"]): connection wormhole signatures
        exit_list (List["ExitHole"]):   exit wormhole signatures
        scan_site_list (List["ScanSite"]):  scan sites signatures
    '''
    def __init__(self,system_id: int,system_depth: int,incoming_wormhole: "ConnectionHole") -> None:
        self.id = system_id
        
        self.depth = system_depth

        self.title = f"{system_depth}-{system_id:03}"    

        self.class_level = 0 

        self.scan_site_counter = 0

        self.connection_list: List["ConnectionHole"] = [incoming_wormhole] 
        self.exit_list: List["ExitHole"] = []
        self.scan_site_list: List["ScanSite"] = []