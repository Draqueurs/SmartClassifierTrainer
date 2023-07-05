from customtkinter import CTkTabview, CTkLabel, CTkFont, CTkOptionMenu, CTkButton, CTkSlider, CTkSwitch, CTkEntry, CTkProgressBar


class TasksView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Classification")
        self.add("Detection")

        # add widgets on tabs
        self.label = CTkLabel(master=self.tab("Classification"))
        self.label.grid(row=0, column=0, padx=20, pady=10)