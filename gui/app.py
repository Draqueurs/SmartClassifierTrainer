from customtkinter import CTk, CTkFrame, CTkLabel, CTkFont
from . import dataset_frame
from . import train_frame
from . import project_frame
from model import dataset
from model import tftrainer
import threading

################################################################################
#                                     APP                                      #
################################################################################
class App(CTk):

    def __init__(self):
        super().__init__()
        self.title("SmartClassifierTrainer")
        self.minsize(423,38)
        self.resizable(False,False)

        # configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.dataset = None
        self.tftrainer = None

        self.project_frame = project_frame.ProjectFrame(self)
        self.project_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.dataset_frame = dataset_frame.DatasetFrame(self)
        self.dataset_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.train_frame = train_frame.TrainFrame(self)
        self.train_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    
    def create_dataset(self, data_folder,
        train_ratio,
        pp_operations,
        top_ratio, bottom_ratio, right_ratio, left_ratio,
        width, height,
        aug_operations,
        rotation,
        blur,
        percent,
        count,
        slider):
        self.dataset = dataset.Dataset(
            data_folder,
            train_ratio,
            pp_operations,
            top_ratio,
            bottom_ratio,
            right_ratio,
            left_ratio,
            width,
            height,
            aug_operations,
            rotation,
            blur,
            percent,
            count,
            slider
        )

    def generate_dataset(self, data_folder, train_ratio, pp_operations, top_ratio, bottom_ratio, right_ratio, left_ratio,
        width, height, aug_operations, rotation, blur, percent, count, slider):
        thread = threading.Thread(target=self.create_dataset, args=(data_folder, train_ratio, pp_operations, top_ratio, bottom_ratio, right_ratio, left_ratio,
            width, height, aug_operations, rotation, blur, percent, count, slider))
        thread.start()

    def train(self, model, epochs, batch_size, name, wandb_entity, wandb_project, epochs_progressbar, total_progressbar):
        self.trainer = tftrainer.TFTrainer(
            dataset=self.dataset, model=model, epochs=epochs, batch_size=batch_size, name=name,
            wandb_entity=wandb_entity, wandb_project=wandb_project, 
            epochs_progressbar=epochs_progressbar, total_progressbar=total_progressbar
        )
        self.trainer.train()

    def start_training(self, model, epochs, batch_size, name, wandb_entity, wandb_project, epochs_progressbar, total_progressbar):
        thread = threading.Thread(target=self.train, args=(model, epochs, batch_size, name, wandb_entity, wandb_project, epochs_progressbar, total_progressbar))
        thread.start()