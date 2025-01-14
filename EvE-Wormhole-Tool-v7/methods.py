from typing import TYPE_CHECKING,List
import constants as const

if TYPE_CHECKING:
    from signatures import ConnectionHole,ExitHole,ScanSite
    from tables import ConnectionTable,ExitTable,ScanSiteTable
    from custom_widgets import ToggleButton
    from system import SolarSystem
    from tkinter import Label

def pack_table(table: "ConnectionTable|ExitTable|ScanSiteTable") -> None:
    '''
    Pack table static ui elements
    '''
    table.table_frame.pack(side="top")
    table.titles_frame.pack(side="top")
    for label in table.title_widgets:
        table.title_widgets[label].pack(side="left")

def pack_toggle_button(toggle_list: List["ToggleButton"])  -> None:
    '''
    Pack list of toggle buttons
    '''
    for toggle in toggle_list:
        toggle.button.pack(side="left")

def setup_toggles(toggle_list: List["ToggleButton"]):
    '''
    Initialize toggle buttons
    '''
    for toggle in toggle_list:      #iterate toggles
        toggle.container_list = toggle_list #assign container
        toggle.button.configure(command=toggle.select_toggle)   #configure button onclik method

    toggle_list[0].is_selected = True   #first toggle is selected by default
    toggle_list[0].select_toggle()

def flip_all_frames_visibility(solar_system: "SolarSystem") -> None:  
    '''
    Flip system sigantures frames between visible / invisible
    '''
    for wormhole in solar_system.connection_list:
        wormhole.frame_visibilility = flip_frame_visibility(wormhole)
    for exit in solar_system.exit_list:
        exit.frame_visibilility = flip_frame_visibility(exit)
    for site in solar_system.scan_site_list:
        site.frame_visibilility = flip_frame_visibility(site)

def flip_frame_visibility(signature: "ConnectionHole|ExitHole|ScanSite") -> bool:
    '''
    Swap frame visibility
    '''
    if signature.frame_visibilility:
        signature.frame.pack_forget()
        return False        
    else:
        signature.frame.pack(side="top")
        return True

def update_destination_labels(title_label: "Label",
                              class_label: "Label",
                              system: "SolarSystem"
    ) -> None:
    '''
    When jumping to a system update the jump wormhole to represent new destination
    '''
    title_label.configure(text=system.title)        #destination title
    if system.class_level == const.UNKNOWN_CLASS_INT:       #destination class level
        class_label.configure(text=const.CLASS_ZERO_TEXT)   #if class == 0 use const string
    else:
        class_label.configure(text=str(system.class_level)) #else use class_level int

def delete_signautre(container_list: List["ConnectionHole|ExitHole|ScanSite"],
                     signature: "ConnectionHole|ExitHole|ScanSite"
    ):
    '''
    Delete signature from current system
    '''
    flip_frame_visibility(signature)    #hide siganuter frame
    container_list.pop(container_list.index(signature)) #pop from list