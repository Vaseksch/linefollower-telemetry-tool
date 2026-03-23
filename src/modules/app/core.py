import customtkinter as ctk
from ..loader.core import FileHandler
from modules.serial.core import read_serial_data
from modules.analysis.core import Analyzer
from pandas import DataFrame
from .const import APP_SIZE_RATIO
from loguru import logger
import ctypes
from matplotlib import pyplot as plt
from serial import PortNotOpenError

class mainApp(ctk.CTk):
    def __init__(self, file_handler: FileHandler, analyzer: Analyzer):
        super().__init__()
        self.geometry(self.get_screen_size())
        self.title("LapLog")
        
        self.file_handler = file_handler
        self.dataframe: DataFrame
        self.analyzer = analyzer
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid
        
        self.robot_connect_button = ctk.CTkButton(self, text="Load robot data", command=self.load_robot_data)
        self.robot_connect_button.grid(row=0, column=0, padx=40, pady=20, sticky="ew", columnspan=4)
        
        self.load_button = ctk.CTkButton(self, text="Load file", command=self.load_file)
        self.load_button.grid(row=1, column=1, padx=(10, 10), sticky="ew")
        
        self.save_button = ctk.CTkButton(self, text="Save file", command=self.save_file)
        self.save_button.grid(row=1, column=2, padx=(10, 10), sticky="ew")
        
        self.excel_button = ctk.CTkButton(self, text="Open with Excel", command=self.open_with_excel)
        self.excel_button.grid(row=1, column=3, padx=(10, 40), sticky="ew")
        
        self.file_name_entry = ctk.CTkEntry(self, placeholder_text="enter valid file name")
        self.file_name_entry.grid(row=1, column=0, padx=(40, 10), sticky="ew")
        
        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.grid(row=2, column=0, padx=40, pady=20, sticky="nsew", columnspan=4)
        
        self.ku_entry = ctk.CTkEntry(self, placeholder_text="enter Ku")
        self.ku_entry.grid(row=3, column=0, padx=(40, 10), pady=20, sticky="e")
        
        self.label = ctk.CTkLabel(self, text="KP: Null, KD: Null", fg_color="transparent")
        self.label.grid(row=3, column=1, padx=10, pady=20, sticky="e")
        
        self.analysis_button = ctk.CTkButton(self, text="Calculate KD, KU", command=self.run_analysis)
        self.analysis_button.grid(row=3, column=2, padx=(10, 40), pady=20, sticky="ew")
        
        self.x_axis_entry = ctk.CTkEntry(self, placeholder_text="enter X axis")
        self.x_axis_entry.grid(row=4, column=0, padx=(40, 10), pady=20, sticky="e")
        
        self.y_axis_entry = ctk.CTkEntry(self, placeholder_text="enter Y axis")
        self.y_axis_entry.grid(row=4, column=1, padx=10, pady=20, sticky="e")
        
        self.plot_button = ctk.CTkButton(self, text="Show plot", command=self.plot_dataset)
        self.plot_button.grid(row=4, column=2, padx=(10, 40), pady=20, sticky="ew")
        
    def get_screen_size(self):
        screen_size_x = int(self.winfo_screenwidth() * APP_SIZE_RATIO)
        screen_size_y = int(self.winfo_screenheight() * APP_SIZE_RATIO)
        
        
        screen_dimensions = f"{screen_size_x}x{screen_size_y}"
        logger.debug(screen_dimensions)
        
        return screen_dimensions
    
    def load_file(self):
        file_name = self.file_name_entry.get()
        if len(file_name) > 0:
            if self.Mbox("Load new file?", "Are you sure you want to load new file, unsaved data will be lost", 1) == 1:
                try:
                    self.dataframe = self.file_handler.load_file(file_name=file_name)
                except ValueError:
                    logger.error("Invalid file format")
                    self.Mbox("ERROR", "Enter valid file name. File name must end with .csv", 0x0 | 0x10)
                self.textbox.delete("0.0")
                self.textbox.insert("0.0", self.dataframe.to_string())
        else:
            self.Mbox("Warning", "Invalid file name", 0x0 | 0x10)
    
    def load_robot_data(self):
        if self.Mbox("Load new file?", "Are you sure you want to load new data, unsaved data will be lost", 1) == 1:
            try:
                self.dataframe = read_serial_data()
                self.textbox.delete("0.0")
                self.textbox.insert("0.0", self.dataframe.to_string())
            except PortNotOpenError:
                self.Mbox("ERROR", "No device found.", 0x0 | 0x10)
    
    def save_file(self):
        file_name = self.file_name_entry.get()
        if len(file_name) > 0:
            if not self.file_handler.check_if_file_exists(file_name=file_name):
                try:
                    self.file_handler.save_file(dataframe=self.dataframe, file_name=file_name)
                except ValueError:
                    logger.error("Invalid file format")
                    self.Mbox("ERROR", "Enter valid file name. File name must end with .csv or .xlsx", 0x0 | 0x10)
                    
            elif self.Mbox("Owerwrite file?", "File with this name already exists are you sure you want to over write it?", 1) == 1:
                try:
                    self.file_handler.save_file(dataframe=self.dataframe, file_name=file_name)
                except ValueError:
                    logger.error("Invalid file format")
                    self.Mbox("ERROR", "Enter valid file name. File name must end with .csv or .xlsx", 0x0 | 0x10)
            else:
                logger.error("An ERROR occured while saving the file")
        
    def Mbox(self, title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
    def plot_dataset(self):
        x_param = self.x_axis_entry.get()
        y_param = self.y_axis_entry.get()
        
        x_data = self.dataframe[x_param]
        y_data = self.dataframe[y_param]
        
        plt.plot(x_data, y_data)
        plt.grid(which='minor', linewidth=0.3)
        plt.minorticks_on()
        plt.show()
        
    def open_with_excel(self):
        file_name = self.file_name_entry.get()
        if len(file_name) > 0:
            if self.file_handler.check_if_file_exists(file_name=file_name):
                self.file_handler.launch_excel(file_name=file_name)
        else:
            logger.error("Invalid file format")
            
    def run_analysis(self):
        ku = float(self.ku_entry.get())
        kp, kd = self.analyzer.calculate_ziegler_nichols(self.dataframe, ku)
        
        self.label.configure(text=f"KP: {kp:.3f}, KD: {kd:.3f}")
