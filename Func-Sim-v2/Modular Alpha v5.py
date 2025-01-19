import tkinter as tk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error

def create_connection(db_file):    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def Add_Variable():
    #Clear_Result_Label()     
    table_row = 1   
    variable_entry.append([tk.Entry(root),tk.Entry(root),tk.Entry(root)])
    variable_data.append(["","",0])    
    for entry in variable_entry[-1]:
        entry.grid(row=table_row,column=add_table_column[0])
        table_row+=1
    variable_entry[-1][2].insert(0,0)
    add_table_column[0] += 1       

def Remove_Variable():
    #Clear_Result_Label()
    if len(variable_entry) != 0:
        for entry in variable_entry[-1]:
            entry.grid_forget()
        variable_entry.pop(-1)
        variable_data.pop(-1)        
        add_table_column[0] -= 1    

def Run():
    if Entry_Validation():
        return
    Clear_Result_Label()
    Read_Variable_Entry()
    Calculate_Result()             

def Entry_Validation():
    if bool(variable_entry):
        if iterations_entry.get().isnumeric():            
            if all(all(bool(entry.get()) for entry in column) for column in variable_entry):
                if all(entry[0].get().isalpha() for entry in variable_entry):                    
                    return False
                else:
                    messagebox.showerror("Error","Name must only contain letters")
                    return True
            else:
                messagebox.showerror("Error","Fill all the inputs")
                return True  
        else:
            messagebox.showerror("Error","Iterations must be a number")
            return True 
    else:
        messagebox.showerror("Error","Add at least one variable")
        return True

def Clear_Result_Label():
    if bool(variable_results):
        for result in range(len(variable_results)):
            variable_results[-1].grid_forget()
            variable_results.pop(-1)

def Read_Variable_Entry():
    for variable in range(len(variable_entry)):
        variable_data[variable][0] = variable_entry[variable][0].get()
        variable_data[variable][1] = variable_entry[variable][1].get()
        variable_data[variable][2] = int(variable_entry[variable][2].get())    
    for variable in variable_data:        
        variable[1] += " "
        formula_final = ""
        chunk = ""
        for char in variable[1]:
            if char.isalpha() == False:
                if bool(chunk) == True:
                    for column_search in variable_data:
                        if chunk == column_search[0]:
                            formula_final += "variable_data["+str(variable_data.index(column_search))+"][2]"
                formula_final += char
                chunk = ""
            else:
                chunk += char
        variable[1] = formula_final

def Calculate_Result():
    iterations = int(iterations_entry.get()) 
    table_row = 4   
    for iteration in range(iterations):
        table_column = 1
        for variable in range(len(variable_data)):            
            variable_data[variable][2] = eval(variable_data[variable][1])
            variable_results.append(tk.Label(root,text=variable_data[variable][2]))
            variable_results[-1].grid(row=table_row,column=table_column)
            table_column += 1
        table_row += 1  

def DB_Save_Result():
    DB_Create_Result_Table(result_save_entry)
    sql = """INSERT INTO """+str(result_save_entry.get())+"""(name,function,init)
             VALUES(?,?,?)"""    
    cur = conn.cursor()
    for variable in variable_data:        
        cur.execute(sql,variable)
    conn.commit()
    return cur.lastrowid

def DB_Create_Result_Table(tabla_name):
    sql_create_result_table = """CREATE TABLE IF NOT EXISTS """+str(tabla_name.get())+""" (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    function text NOT NULL,
                                    init integer NOT NULL
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_result_table)
    except Error as e:
        print(e)

def DB_Result_Load():
    return

root = tk.Tk()
root.geometry("800x200+500+250")

database = r"db_result.db"
conn = create_connection(database)

add_table_column = [1]

variable_entry = [] 
variable_data = []  
variable_results = [] 

add_variable_button = tk.Button(root,text="Add",command=Add_Variable)
add_variable_button.grid(row=0,column=0)

remove_variable_button = tk.Button(root,text="Remove",command=Remove_Variable)
remove_variable_button.grid(row=0,column=1)

iterations_label = tk.Label(root,text="Iterations")
iterations_label.grid(row=0,column=2)

iterations_entry = tk.Entry(root)
iterations_entry.grid(row=0,column=3)
iterations_entry.insert(0,1)

run_button = tk.Button(root,text="Run",command=Run)
run_button.grid(row=0,column=4)

result_save_entry = tk.Entry(root)
result_save_entry.grid(row=0,column=5)

result_save_button = tk.Button(root,text="Save",command=DB_Save_Result)
result_save_button.grid(row=0,column=6)

result_load_entry = tk.Entry(root)
result_load_entry.grid(row=0,column=7)

result_load_button = tk.Button(root,text="Load",command=DB_Result_Load)
result_load_button.grid(row=0,column=8)

variable_name_label = tk.Label(root,text="Name")
variable_name_label.grid(row=1,column=0)

variable_formula_label = tk.Label(root,text="Formula")
variable_formula_label.grid(row=2,column=0)

variable_init_label = tk.Label(root,text="Init")
variable_init_label.grid(row=3,column=0)

root.mainloop()