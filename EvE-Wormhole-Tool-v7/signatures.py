from system import SolarSystem
from tkinter import Label,Frame,Button,Entry
from custom_widgets import ToggleButton
from methods import pack_toggle_button
import constants as const

class Signature:
    '''
    Parent class containing table frame
    Attribute:
        frame_visibilility (bool): whether the frame is hiden / visible
    '''
    def __init__(self,
                 frame: Frame #table frame containing the signature
                 ):        
        self.frame_visibilility = False
        self.frame = Frame(frame)
        self.delete_button = Button(self.frame,text="Delete")

class Wormhole():
    '''
    Parent class for both types of wormholes: connection and exit
    Attribute:
        timer_toggles (list[ToggleButton]): timer to estimate life expentancy of wormholes
    '''
    def __init__(self):
        self.timer_toggles = [ToggleButton(i,self.frame) for i in range(const.TIMER_NUM)]

class ConnectionHole(Signature,Wormhole):
    '''
    Wormhole leading to another solar system
    Attributes:
        linked_systems ([system.SolarSystem,system.SolarSystem]): pair of systems connected via this wormhole
        destination_label (tkinter.Label): destination title
        destination_class_label (tkinter.Label): destination class
        jump_button (tkinter.Button): button for jumping between linked systems, method is configured after init
    '''
    def __init__(self,frame: Frame,parent_system: SolarSystem) -> None:
        super().__init__(frame)
        Wormhole.__init__(self)
        self.linked_systems = [parent_system]
        self.destination_label = Label(self.frame)
        self.destination_class_label = Label(self.frame,text=const.DEFAULT_DESTINATION_CLASS_LABEL_TEXT)
        self.jump_button = Button(self.frame,text=const.JUMP_BUTTON_TEXT)

    def pack_widgets(self) -> None:
        '''
        Pack ui elements
        '''
        self.destination_label.pack(side="left")
        self.jump_button.pack(side="left")
        self.destination_class_label.pack(side="left")
        pack_toggle_button(self.timer_toggles)
        self.delete_button.pack(side="left")

class ExitHole(Signature,Wormhole):
    '''
    Wormhole leading to known space
    Attributes:
        sec_level (int): int to classify the known space security level (High 0,Low 1,Null 2)
        destination_entry (tkinter.Entry): entry input for known space system name
        sec_level_toggles (list[ToggleButton]): trio of toggles used to select and assign sec_level
    '''
    def __init__(self,frame: Frame) -> None:
        super().__init__(frame)
        Wormhole.__init__(self)
        self.sec_level = 0
        self.destination_entry = Entry(self.frame)
        self.sec_level_toggles = [ToggleButton(i,self.frame) for i in range(const.SEC_LEVEL_NUM)]
    
    def pack_widgets(self) -> None:
        '''
        Pack ui elements
        '''
        self.destination_entry.pack(side="left")
        pack_toggle_button(self.sec_level_toggles)   
        pack_toggle_button(self.timer_toggles)  
        self.delete_button.pack(side="left")

class ScanSite(Signature):
    '''
    Treasure site within the system
    Attributes:
        loot_type (int): whether this site is "Relic 0" or "Data 1" site
        title_label (tkinter.Label): site title
        loot_type_toggles (list[ToggleButton]): duo of toggle button to assign loot type
    '''
    def __init__(self,site_id: int,frame: Frame) -> None:
        super().__init__(frame)
        self.loot_type = 0
        self.title_label = Label(self.frame,text=f"{site_id:02}")
        self.loot_type_toggles = [ToggleButton(i,self.frame) for i in range(const.LOOT_TYPE_NUM)]
    
    def pack_widgets(self):
        self.title_label.pack(side="left")
        pack_toggle_button(self.loot_type_toggles)
        self.delete_button.pack(side="left")