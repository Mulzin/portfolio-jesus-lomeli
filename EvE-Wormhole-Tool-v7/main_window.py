from tkinter.ttk import Combobox
from tables import ConnectionTable,ExitTable,ScanSiteTable
from typing import Callable
from methods import pack_table
from tkinter import Tk,Label,Frame,Button
import constants as const

class MainWindow:
    '''
    Controller for the ui elements
    Attributes:
        root (tkinter.Tk): main windows

        title_frame (tkinter.Frame): frame containing current system info
        current_system_label (tkinter.Label): title of the current system
        class_label (tkinter.Label): combobox title
        class_combobox (tkinter.Combobox): combobox for class level option

        wormhole_table (tables.ConnectionTable): frame containing connection wormholes ui elements

        exit_table (tables.ExitTable): frame containing exit wormholes ui elements

         scan_site_table (tables.ScanSiteTable): frame containing scan site ui elements
    '''
    def __init__(self) -> None:
        self.root = Tk()

        self.title_frame = Frame(self.root)
        self.current_system_label = Label(self.title_frame)
        self.class_label = Label(self.title_frame,text="Class: ")
        self.class_combobox = Combobox(self.title_frame,state="readonly",values=const.CLASS_COMBOBOX_VALUES)

        self.new_signature_frame = Frame(self.root)
        self.new_signature_button = Button(self.new_signature_frame,text=const.NEW_SIGNATURE_BUTTON_TEXT)
        self.new_signature_combobox =  Combobox(self.new_signature_frame,state="readonly",values=const.NEW_SIG_COMBOBOX_VALUES)

        self.wormhole_table = ConnectionTable(self.root)

        self.exit_table = ExitTable(self.root)

        self.scan_site_table = ScanSiteTable(self.root)
    
    def initialize_ui(self,
                      current_system_title: str,    
                      class_combobox_method: Callable[[],None], 
                      new_signature_method: Callable[[],None]
        ) -> None:
        '''
        Update labels and configure button methods
        '''

        self.current_system_label.configure(text=f"Current system: {current_system_title}") #system title

        self.class_combobox.bind("<<ComboboxSelected>>", class_combobox_method)    #methods for onclik button and combobox selection
        self.new_signature_button.configure(command=new_signature_method)

        self.class_combobox.current(0)          #combobox default values
        self.new_signature_combobox.current(0)

        self.pack_static_widgets()  #pack widgets

        self.root.mainloop()        #start tkinter mainloop
    
    def pack_static_widgets(self) -> None:
        '''
        Pack ui elements
        '''
        self.title_frame.pack(side="top")
        self.current_system_label.pack(side="left")
        self.class_label.pack(side="left")
        self.class_combobox.pack(side="left")
        
        self.new_signature_frame.pack(side="top")
        self.new_signature_button.pack(side="left")
        self.new_signature_combobox.pack(side="left")

        pack_table(self.wormhole_table)
        pack_table(self.exit_table)
        pack_table(self.scan_site_table)