from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkOptionMenu, CTkEntry, CTkProgressBar
from customtkinter import filedialog
from customtkinter import END
import json
from pathlib import Path
import os
import shutil



class ProjectFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # configure grid system
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # add widgets onto the frame, for example:
        self.label = CTkLabel(self, text='Project', font=CTkFont(weight='bold', size=20))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,10), sticky="nsew")

        # variables for check if the frame is expand
        self.expand = False

        # widgets
        self.widgets = {}

        self.widgets['select_json_button'] = CTkButton(self, text='Select JSON File', command=self.select_json_button_event)
        self.widgets['select_json_entry'] = CTkEntry(self, placeholder_text='Path to JSON file')

        self.widgets['select_original_button'] = CTkButton(self, text='Select Original Folder', command=self.select_original_button_event)
        self.widgets['select_original_entry'] = CTkEntry(self, placeholder_text='Path to Original folder')

        self.widgets['select_destination_button'] = CTkButton(self, text='Select Destination Folder', command=self.select_destination_button_event)
        self.widgets['select_destination_entry'] = CTkEntry(self, placeholder_text='Path to Destination folder')

        self.widgets['create_dataset_folder_button'] = CTkButton(self, text='Create Dataset Folder', command=self.create_dataset_folder_event)
        self.widgets['create_dataset_folder_progressbar'] = CTkProgressBar(self, progress_color='red')
        self.widgets['create_dataset_folder_progressbar'].set(0)

        self.label.bind('<Button-1>', self.grid_widgets)

    def grid_widgets(self, event):
        if not self.expand:
            self.widgets['select_json_button'].grid(row=1, column=0, padx=10, pady=(10,10), sticky="nsew")
            self.widgets['select_json_entry'].grid(row=1, column=1, padx=10, pady=(10,10), sticky="nsew")

            self.widgets['select_original_button'].grid(row=2, column=0, padx=10, pady=(10,10), sticky="nsew")
            self.widgets['select_original_entry'].grid(row=2, column=1, padx=10, pady=(10,10), sticky="nsew")

            self.widgets['select_destination_button'].grid(row=3, column=0, padx=10, pady=(10,10), sticky="nsew")
            self.widgets['select_destination_entry'].grid(row=3, column=1, padx=10, pady=(10,10), sticky="nsew")

            self.widgets['create_dataset_folder_button'].grid(row=4, column=0, columnspan=2, padx=10, pady=(10,10), sticky="nsew")
            self.widgets['create_dataset_folder_progressbar'].grid(row=5, column=0, columnspan=2, padx=10, pady=(10,10), sticky="ew")
        else:
            self.widgets['select_json_button'].grid_forget()
            self.widgets['select_json_entry'].grid_forget()

            self.widgets['select_original_button'].grid_forget()
            self.widgets['select_original_entry'].grid_forget()

            self.widgets['select_destination_button'].grid_forget()
            self.widgets['select_destination_entry'].grid_forget()

            self.widgets['create_dataset_folder_button'].grid_forget()
            self.widgets['create_dataset_folder_progressbar'].grid_forget()
        self.expand = not self.expand

    def select_json_button_event(self):
        self.json_name = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if self.json_name != '':
            self.widgets['select_json_entry'].delete(0, END)
            self.widgets['select_json_entry'].insert(0, self.json_name)

    def select_original_button_event(self):
        self.original_path = filedialog.askdirectory()
        if self.original_path != '':
            self.widgets['select_original_entry'].delete(0, END)
            self.widgets['select_original_entry'].insert(0, self.original_path)

    def select_destination_button_event(self):
        self.destination_path = filedialog.askdirectory()
        if self.destination_path != '':
            self.widgets['select_destination_entry'].delete(0, END)
            self.widgets['select_destination_entry'].insert(0, self.destination_path)

    def create_dataset_folder_event(self):
        # Opening JSON file
        f = open(self.json_name)
        data = json.load(f)

        path = Path(self.original_path)
        nb_images = len(list(path.glob('*.jpg'))) + len(list(path.glob('*.png')))
        idx_image = 0

        self.widgets['create_dataset_folder_progressbar'].set(0)
        self.widgets['create_dataset_folder_progressbar'].configure(progress_color='red')

        file_attributes = None

        for key, value in data.items():
            if file_attributes is None:
                for key, value_2 in value['file_attributes'].items():
                    file_attributes = key
                    break
            folder_path = os.path.join(self.destination_path, value['file_attributes'][file_attributes])
            isExist = os.path.exists(folder_path)
            if not isExist:
                os.makedirs(folder_path)
            shutil.move(os.path.join(self.original_path, value['filename']), os.path.join(folder_path, value['filename']))
            idx_image += 1
            self.widgets['create_dataset_folder_progressbar'].set(idx_image / nb_images)
        self.widgets['create_dataset_folder_progressbar'].configure(progress_color='green')