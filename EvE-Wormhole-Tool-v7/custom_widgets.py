from typing import List
from tkinter import Button,Frame

class ToggleButton:
    '''
    Attributes:
        value (int): int assigned to this button
        is_selected (bool): state of the button
        button (tinter.Button): button ui elament
        container_list (List[ToggleButton]): list where this button is contained, variable is assigned after init
    '''
    def __init__(self,value: int,frame: Frame):
        self.value = value
        self.is_selected = False
        self.button = Button(frame,text="X")
        self.container_list: List["ToggleButton"] = []
    
    def select_toggle(self):
        '''
        On click method for the buttons
        Iterate through the container and change the state of the clicked button
        '''
        self.is_selected = True     #update clicked button state

        for toggle in self.container_list:          #iterate container
            if toggle.is_selected:                  #if selected, update color and state
                toggle.button.configure(bg="blue")
                toggle.button.configure(state="disabled")
            else:
                toggle.button.configure(bg="white")     #else if not slected, update color and state
                toggle.button.configure(state="active")

            toggle.is_selected = False  #clicked button is_selected is set no false for when this method is called again 
   