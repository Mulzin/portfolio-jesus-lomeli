from system import SolarSystem
from main_window import MainWindow
from signatures import ConnectionHole,ExitHole,ScanSite
from methods import flip_frame_visibility,flip_all_frames_visibility,update_destination_labels,setup_toggles,delete_signautre
import constants as const

class WomholeMapper:
    '''
    Attributes:
        system_id_counter (int): incremental int to assign ids to new systems
        current_system (system.SolarSystem): current system we are in
        main_window: UI controller
    '''
    def __init__(self) -> None:
        self.system_id_counter = 0

        self.current_system = SolarSystem(
            self.system_id_counter,
            const.STARTING_DEPTH,None
        )
        
        self.main_window = MainWindow()

    def app_start(self) -> None:  
        '''
        The connection_list of the root system is set to empty
        Call the ui init
        '''      
        self.current_system.connection_list = []
        self.main_window.initialize_ui(self.current_system.title,
                                       self.update_system_class,
                                       self.new_signature)
    
    def update_system_class(self,event) -> None:
        '''
        Update the current system class level when the class combobox is selected 
        '''
        combobox_value = self.main_window.class_combobox.get()
        if combobox_value == "Unknown": combobox_value = 0
        self.current_system.class_level = combobox_value

    def new_signature(self) -> None:
        '''
        On click event for the "New sig" button
        Get the type of signature from the combobox then filter the signature type
        Then append the new signature to its corresponding list 
        '''
        new_sig_type = self.main_window.new_signature_combobox.get()

        if new_sig_type == const.NEW_SIG_COMBOBOX_VALUES[0]:
            self.current_system.connection_list.append(self.create_new_wormhole())
        elif new_sig_type == const.NEW_SIG_COMBOBOX_VALUES[1]:
            self.current_system.exit_list.append(self.create_new_exit_wormhole())
        elif new_sig_type == const.NEW_SIG_COMBOBOX_VALUES[2]:
            self.current_system.scan_site_list.append(self.create_new_scan_site())

    def create_new_wormhole(self) -> ConnectionHole:
        '''
        Initialize and return wormhole leading to a new system
        '''
        self.system_id_counter += 1

        new_id = self.system_id_counter         #id and depths for the new system
        new_depth = self.current_system.depth+1

        new_wormhole = ConnectionHole(                  #new wormhole
            self.main_window.wormhole_table.table_frame,
            self.current_system
        )
        new_system = SolarSystem(       #new solar system
            new_id,
            new_depth,
            new_wormhole
        )
        new_wormhole.linked_systems.append(new_system)                                          #append the new system to the list of pair of linked system
        new_wormhole.jump_button.configure(command=lambda: self.jump_wormhole(new_wormhole))    #update method for "Jump" button in new wormhole
        
        setup_toggles(new_wormhole.timer_toggles)   #init toggle buttons

        new_wormhole.delete_button.configure(       #update method for "Delete" button in new wormhole
            command=lambda: delete_signautre(
                self.current_system.connection_list,
                new_wormhole
            )
        )

        new_wormhole.destination_label.configure(text=new_system.title)         #update label
        new_wormhole.pack_widgets()                                             #add widgets to ui
        new_wormhole.frame_visibilility = flip_frame_visibility(new_wormhole)   #flip the new wormhole frame to visible

        return new_wormhole
    
    def create_new_exit_wormhole(self) -> ExitHole:
        '''
        Initialize and return new wormhole leading to known space
        '''
        new_exit = ExitHole(self.main_window.exit_table.table_frame)    #new exit wormhole
        
        setup_toggles(new_exit.sec_level_toggles)   #init toggle buttons
        setup_toggles(new_exit.timer_toggles)

        new_exit.delete_button.configure(           #update method for "Delete" button in new wormhole  
            command=lambda: delete_signautre(
                self.current_system.exit_list,
                new_exit
            )
        )

        new_exit.destination_entry.insert(0,const.DEFAULT_EXIT_DESTINATION_TEXT)    #init default text for entry
        new_exit.pack_widgets()                                                     #add widgets to ui
        new_exit.frame_visibilility = flip_frame_visibility(new_exit)               #flip the new wormhole frame to visible

        return new_exit
    
    def create_new_scan_site(self) -> ScanSite:
        '''
        Initialize and return new scan site
        '''
        new_scan_site = ScanSite(                           #new scan site
            self.current_system.scan_site_counter,
            self.main_window.scan_site_table.table_frame)
        
        self.current_system.scan_site_counter += 1          #update current system counter

        setup_toggles(new_scan_site.loot_type_toggles)      #init toggle buttons

        new_scan_site.delete_button.configure(              #update method for "Delete" button in new scan site
            command=lambda: delete_signautre(
                self.current_system.scan_site_list,
                new_scan_site
            )
        )

        new_scan_site.pack_widgets()                                            #add widgets to ui
        new_scan_site.frame_visibilility = flip_frame_visibility(new_scan_site) #flip the new wormhole frame to visible

        return new_scan_site
    
    def jump_wormhole(self,wormhole: ConnectionHole) -> None:
        '''
        
        '''
        flip_all_frames_visibility(self.current_system) #hide all frames from current system

        '''
        Wormhole:
            linked_system = [system_1,system_2]
        Evaluate which of the systems we are currently at 
        '''
        if self.current_system == wormhole.linked_systems[0]:  #if current system == system[0]

            update_destination_labels(              #update the wormhole ui elements to represent the new desitation
                wormhole.destination_label,
                wormhole.destination_class_label,
                wormhole.linked_systems[0]
            )
            self.current_system = wormhole.linked_systems[1]    #change the current system to the one we are not in
        else:                                   
            update_destination_labels(                  #same as the previous if but inverted
                wormhole.destination_label,          
                wormhole.destination_class_label,
                wormhole.linked_systems[1]
            )
            self.current_system = wormhole.linked_systems[0]

        self.main_window.current_system_label.configure(text=f"Current system: {self.current_system.title}")    #update static ui elements
        self.main_window.class_combobox.current(self.current_system.class_level)

        flip_all_frames_visibility(self.current_system)     #change the new solar system frimes to visible

main_app = WomholeMapper()
main_app.app_start()