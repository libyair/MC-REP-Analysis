import tkinter as tk 
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox
import os
from os import path
from datetime import datetime
import pandas as pd
import sys

class GetSettings(object):
    def __init__(self, FIXTURE_DIR, db):
        
        self.FIXTURE_DIR = FIXTURE_DIR
        self.db = db
        
        self.window = Tk()
        ttk.Style().theme_use('vista')
        # self.window['bg'] = 'snow'
        self.window.geometry("550x200")
        # rename the title of the window
        self.window.title("Greenennsis - Market analysis software")
        self.window.eval('tk::PlaceWindow . center')


        self.input_file = tk.StringVar()  
        self.output_file = tk.StringVar()
        self.name = tk.StringVar()  

        # draw fields
        tk.Label(self.window, text = "Run settings").grid(row = 0) 

        
        
        #Create Entry with history entries list
        HistoryCombobox.register(self.window)
        list_len = min(len(db),6)

        ## Input path entry list
        tk.Label(self.window, text = "Set input folder path:").grid(row = 1)
        self.entryInput_file = HistoryCombobox(self.window, width="50", textvariable=self.input_file)
        self.entryInput_file.bind("<Return>", self.on_add)
        
        for item in db['input_path'].unique()[0:list_len]:
            self.entryInput_file.add(item)
        self.entryInput_file.grid(row = 1, column = 1)
       
        ## Output path entry list
        tk.Label(self.window, text = "Set output path:").grid(row = 2)
        self.entryOutput_file = HistoryCombobox(self.window, width="50", textvariable=self.output_file)
        self.entryOutput_file.bind("<Return>", self.on_add)
        for item in db['output_path'].unique()[0:list_len]:
            self.entryOutput_file.add(item)
        self.entryOutput_file.grid(row = 2, column = 1)

        ## Name list
        tk.Label(self.window, text = "Set run name:").grid(row = 3)
        self.entryName = tk.Entry(self.window, width="50", textvariable=self.name)
        
        self.entryName = HistoryCombobox(self.window, width="50", textvariable=self.name)
        self.entryName.bind("<Return>", self.on_add)
        for item in db['run_name'].unique()[0:list_len]:
            self.entryName.add(item)       
        self.entryName.grid(row = 3, column = 1)
        
        #add logo 
        self.logo_path = os.path.join(FIXTURE_DIR, 'logo.png')
        self.logo = Image.open(self.logo_path)
        width, height = self.logo.size
        self.logo=self.logo.resize((round(width/6), round(height/6)), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.logo)
        self.label = tk.Label(self.window, image = self.photo)
        self.label.image = self.photo
        self.label.grid(row = 0)

        ### submit botton
        sbmitbtn = Button(self.window, text = "Submit", #activebackground = "green",activeforeground = "black", 
                  command= self.callback)
        sbmitbtn.grid(row = 5, column = 2) 
        
        ## abort run window
        stop = Button(self.window, text="Cancel run", command=self.stop)
        stop.grid(row = 6, column = 2) 
        
        #creat window
        self.window.mainloop()
        

    def callback(self):
        self.input_path = self.entryInput_file.get()
        self.output_path =  self.entryOutput_file.get()
        self.run_name = self.entryName.get()
        pathExist = self.validate_path() 

        if pathExist and len(self.input_path)>0 and len(self.output_path)>0:
            self.update_db()
            self.window.destroy()


    def validate_path(self):
        massageInput = ''
        massageOutput = ''
        if not path.exists(self.input_path):      
           massageInput = "Input path does not exist"
           print("Input path does not exist: ", self.output_path)

        if not path.exists(self.output_path):
            massageOutput = "Output path does not exist"
            print("Output path does not exist: ", self.output_path)

        if len(massageInput)>0 or len(massageOutput)>0:
            root = tk.Tk()
            root.withdraw()
            tk.messagebox.showerror(title="Error message", \
                message=f"{massageInput}\n{massageOutput}")
            return False
        
        return True
        
    
    def on_add(self, ev):
        """Update the history list"""
        item = ev.widget.get()
        ev.widget.delete(0, tk.END)
        ev.widget.add(item)

    def update_db(self):
        """Update db with current settings"""
        time = datetime.now()
        time_str = time.strftime("%d/%m/%Y %H:%M:%S")
        run_dict = {
            'id': [len(self.db)+1] ,
            'run_name': [self.run_name] ,
            'input_path':[self.input_path] ,
            'output_path': [self.output_path] ,
            'excution_time': [time_str]
        }
        run_dict_df = pd.DataFrame(run_dict)
        
        self.db = self.db.append(run_dict_df, ignore_index = True)
        
        self.db.to_csv(f'{self.FIXTURE_DIR}\db.csv', index=False) 

    def stop(self):
        sys.exit("Aborted!")
        """Stop scanning by setting the global flag to False."""


class HistoryCombobox(ttk.Combobox):
    """Remove the dropdown from a combobox and use it for displaying a limited
    set of historical entries for the entry widget.
    <Key-Down> to show the list.
    It is up to the programmer when to add new entries into the history via `add()`"""
    def __init__(self, master, **kwargs):
        """Initialize the custom combobox and intercept the length option."""
        kwargs["style"] = "History.Combobox"
        self.length = 10
        if "length" in kwargs:
            self.length = kwargs["length"]
            del kwargs["length"]
        super(HistoryCombobox, self).__init__(master, **kwargs)

    def add(self, item):
        """Add a new history item to the top of the list"""
        values = list(self.cget("values"))
        values.insert(0, item)
        self.configure(values=values[:self.length])

    @staticmethod
    def register(master):
        """Create a combobox with no button."""
        style = ttk.Style(master)
        style.layout("History.Combobox",
            [('Combobox.border', {'sticky': 'nswe', 'children':
              [('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children':
                [('Combobox.background', {'sticky': 'nswe', 'children':
                  [('Combobox.focus', {'expand': '1', 'sticky': 'nswe', 'children':
                    [('Combobox.textarea', {'sticky': 'nswe'})]})]})]})]})])
        style.configure("History.Combobox", padding=(1, 1, 1, 1))
        style.configure("History.Combobox", arrowsize=30)
        style.configure('History.Combobox.Vertical.TScrollbar', arrowsize=28)
        style.map("History.Combobox", **style.map("TCombobox"))
        
        

