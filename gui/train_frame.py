from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkOptionMenu, CTkEntry, CTkProgressBar
from customtkinter import IntVar, StringVar


class TrainFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # configure grid system
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # add widgets onto the frame, for example:
        self.label = CTkLabel(self, text='Train', font=CTkFont(weight='bold', size=20))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,10), sticky="nsew")

        # variables for check if the frame is expand
        self.expand = False
        self.tasks_segemented_button_var = StringVar(value="Classification")

        # arguments
        self.args = {}
        self.args['dataset'] = None
        self.args['model'] = StringVar(value="efficientnetv2-b0")
        self.args['epochs'] = IntVar(value=100)
        self.args['batch_size'] = IntVar(value=32)
        self.args['name'] = None
        self.args['entity'] = None
        self.args['project'] = None

        # widgets
        self.widgets = {}

        self.widgets['models_label'] = CTkLabel(self, text='Model')
        self.widgets['models_optionmenu'] = CTkOptionMenu(self, variable=self.args['model'], values=["efficientnetv2-b0", "efficientnetv2-b1", "efficientnetv2-b2", "efficientnetv2-b3", "efficientnetv2-b4"])
        self.widgets['epochs_label'] = CTkLabel(self, text='Epochs')
        self.widgets['epochs_entry'] = CTkEntry(self, placeholder_text='Number of epochs')
        self.widgets['batch_size_label'] = CTkLabel(self, text='Batch Size')
        self.widgets['batch_size_entry'] = CTkEntry(self, placeholder_text='Size of batch')
        self.widgets['name_label'] = CTkLabel(self, text='Name')
        self.widgets['name_entry'] = CTkEntry(self, placeholder_text='Name of saved model')

        self.widgets['wandb_entity_label'] = CTkLabel(self, text='Wandb Entity')
        self.widgets['wandb_entity_entry'] = CTkEntry(self, placeholder_text='Wandb entity to visualization')
        self.widgets['wandb_project_label'] = CTkLabel(self, text='Wandb Project')
        self.widgets['wandb_project_entry'] = CTkEntry(self, placeholder_text='Wandb project to visualization')

        self.widgets['start_training_button'] = CTkButton(self, text='Start training', command=self.start_training_button_event)
        self.widgets['epochs_progressbar'] = CTkProgressBar(self, progress_color='red')
        self.widgets['epochs_progressbar'].set(0)
        self.widgets['total_progressbar'] = CTkProgressBar(self, progress_color='red')
        self.widgets['total_progressbar'].set(0)

        self.label.bind('<Button-1>', self.grid_widgets)

    def grid_widgets(self, event):
        if not self.expand:

            self.widgets['models_label'].grid(row=2, column=0, padx=10, pady=10, sticky="nsw")
            self.widgets['models_optionmenu'].grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
            self.widgets['epochs_label'].grid(row=3, column=0, padx=10, pady=10, sticky="nsw")
            self.widgets['epochs_entry'].grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
            self.widgets['batch_size_label'].grid(row=4, column=0, padx=10, pady=10, sticky="nsw")
            self.widgets['batch_size_entry'].grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
            self.widgets['name_label'].grid(row=5, column=0, padx=10, pady=10, sticky="nsw")
            self.widgets['name_entry'].grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

            self.widgets['wandb_entity_label'].grid(row=6, column=0, padx=10, pady=10, sticky="nsw")
            self.widgets['wandb_entity_entry'].grid(row=6, column=1, padx=10, pady=10, sticky="nsew")
            self.widgets['wandb_project_label'].grid(row=7, column=0, padx=10, pady=10, sticky="nsw")
            self.widgets['wandb_project_entry'].grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

            self.widgets['start_training_button'].grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            self.widgets['epochs_progressbar'].grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            self.widgets['total_progressbar'].grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        else:

            self.widgets['models_label'].grid_forget()
            self.widgets['models_optionmenu'].grid_forget()
            self.widgets['epochs_label'].grid_forget()
            self.widgets['epochs_entry'].grid_forget()
            self.widgets['batch_size_label'].grid_forget()
            self.widgets['batch_size_entry'].grid_forget()
            self.widgets['name_label'].grid_forget()
            self.widgets['name_entry'].grid_forget()

            self.widgets['wandb_entity_label'].grid_forget()
            self.widgets['wandb_entity_entry'].grid_forget()
            self.widgets['wandb_project_label'].grid_forget()
            self.widgets['wandb_project_entry'].grid_forget()


            self.widgets['start_training_button'].grid_forget()
            self.widgets['epochs_progressbar'].grid_forget()
            self.widgets['total_progressbar'].grid_forget()
        self.expand = not self.expand

    def start_training_button_event(self):
        self.widgets['epochs_progressbar'].set(0)
        self.widgets['total_progressbar'].set(0)
        self.widgets['epochs_progressbar'].configure(progress_color='red')
        self.widgets['total_progressbar'].configure(progress_color='red')
        self.args['epochs'] = int(self.widgets['epochs_entry'].get()) if self.widgets['epochs_entry'].get() != '' else self.args['epochs']
        self.args['batch_size'] = int(self.widgets['batch_size_entry'].get()) if self.widgets['batch_size_entry'].get() != '' else self.args['batch_size']
        self.args['name'] = self.widgets['name_entry'].get() if self.widgets['name_entry'].get() != '' else None
        self.args['entity'] = self.widgets['wandb_entity_entry'].get() if self.widgets['wandb_entity_entry'].get() != '' else None
        self.args['project'] = self.widgets['wandb_project_entry'].get() if self.widgets['wandb_project_entry'].get() != '' else None
        self.master.start_training(
            self.args['model'].get(),
            self.args['epochs'],
            self.args['batch_size'],
            self.args['name'],
            self.args['entity'],
            self.args['project'],
            self.widgets['epochs_progressbar'],
            self.widgets['total_progressbar']
        )