import tkinter as tk
import constants as const

class ConnectionTable:
    '''
    Ui table for connection wormholes
    Attributes:
        table_frame (tkinter.Frame): main frame for the table
        titles_frame (tkinter.Frame): row containing the table titles
        title_widgets (tkinter.Label): titles for the columns in the table, kept in a list for iteration
    '''
    def __init__(self,root: tk.Tk) -> None:
        self.table_frame = tk.Frame(root)
        
        self.titles_frame = tk.Frame(self.table_frame)

        self.title_widgets = {
            "destination_label":tk.Label(self.titles_frame,text=const.DESTINATION_LABEL_TEXT),
            "class_label":tk.Label(self.titles_frame,text=const.CLASS_LABEL_TEXT),
            "short_timer_label":tk.Label(self.titles_frame,text=const.SHORT_TIMER_LABEL_TEXT),
            "mid_timer_label":tk.Label(self.titles_frame,text=const.MID_TIMER_LABEL_TEXT),
            "long_timer_label":tk.Label(self.titles_frame,text=const.LONG_TIMER_LABEL_TEXT)}

class ExitTable:
    '''
    Ui table for exit wormholes
    Attributes:
        table_frame (tkinter.Frame): main frame for the table
        titles_frame (tkinter.Frame): row containing the table titles
        title_widgets (tkinter.Label): titles for the columns in the table, kept in a list for iteration
    '''
    def __init__(self,root: tk.Tk) -> None:
        self.table_frame = tk.Frame(root)

        self.titles_frame = tk.Frame(self.table_frame)

        self.title_widgets = {
            "destination_label":tk.Label(self.titles_frame,text=const.DESTINATION_LABEL_TEXT),
            "null_sec_label":tk.Label(self.titles_frame,text=const.NULL_SEC_LABEL_TEXT),
            "low_sec_label":tk.Label(self.titles_frame,text=const.LOW_SEC_LABEL_TEXT),
            "high_sec_label":tk.Label(self.titles_frame,text=const.HIGH_SEC_LABEL_TEXT),            
            "short_timer_label":tk.Label(self.titles_frame,text=const.SHORT_TIMER_LABEL_TEXT),
            "mid_timer_label":tk.Label(self.titles_frame,text=const.MID_TIMER_LABEL_TEXT),
            "long_timer_label":tk.Label(self.titles_frame,text=const.LONG_TIMER_LABEL_TEXT)}
        
class ScanSiteTable:
    '''
    Ui table for scan sites
    Attributes:
        table_frame (tkinter.Frame): main frame for the table
        titles_frame (tkinter.Frame): row containing the table titles
        title_widgets (tkinter.Label): titles for the columns in the table, kept in a list for iteration
    '''
    def __init__(self,root: tk.Tk) -> None:
        self.table_frame = tk.Frame(root)

        self.titles_frame = tk.Frame(self.table_frame)

        self.title_widgets = {
            "site_title_label":tk.Label(self.titles_frame,text=const.SCAN_SITE_LABEL_TEXT),
            "data_label":tk.Label(self.titles_frame,text=const.DATA_LABEL_TEXT),
            "relic_label":tk.Label(self.titles_frame,text=const.RELIC_LABEL_TEXT)}        