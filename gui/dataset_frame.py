from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkSlider, CTkSwitch, CTkEntry, CTkProgressBar
from customtkinter import IntVar
from customtkinter import filedialog
from pathlib import Path


class DatasetFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # configure grid system
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # add widgets onto the frame, for example:
        self.label = CTkLabel(self, text='Dataset', font=CTkFont(weight='bold', size=20))
        self.label.grid(row=0, column=0, padx=10, pady=(10,10), sticky="nsew")

        # variables for check if the frame is expand
        self.expand = False
        self.source_images_expand = False
        self.train_test_val_expand = False
        self.preprocessing_expand = False
        self.augmentation_expand = False
        self.generate_expand = False

        # arguments
        self.args = {}
        self.args['data_folder'] = None
        self.args['train_ratio'] = IntVar(value=70)
        self.args['pp_operations'] = []
        self.args['top_ratio'] = IntVar(value=25)
        self.args['bottom_ratio'] = IntVar(value=25)
        self.args['right_ratio'] = IntVar(value=25)
        self.args['left_ratio'] = IntVar(value=25)
        self.args['width'] = None
        self.args['height'] = None
        self.args['aug_operations'] = []
        self.args['rotation'] = IntVar(value=15)
        self.args['blur'] = IntVar(value=1)
        self.args['percent'] = IntVar(value=5)
        self.args['count'] = IntVar(value=10)

        # widgets
        self.widgets = {}
        ## Source Images
        self.widgets['source_images_frame'] = CTkFrame(self)
        self.widgets['source_images_frame'].columnconfigure(0, weight=1)
        self.widgets['source_images_frame'].columnconfigure(1, weight=1)
        self.widgets['source_images_label'] = CTkLabel(self.widgets['source_images_frame'], text='Source Images', font=CTkFont(weight='bold', size=15))
        self.widgets['data_folder_button'] = CTkButton(self.widgets['source_images_frame'], text='Select Data Folder', command=self.data_folder_button_event)
        self.widgets['nb_images_label'] = CTkLabel(self.widgets['source_images_frame'], text='Number of Images: 0')
        self.widgets['nb_class_label'] = CTkLabel(self.widgets['source_images_frame'], text='Number of Classes: 0')
        ## Train/Test/Val Split
        self.widgets['train_test_val_frame'] = CTkFrame(self)
        self.widgets['train_test_val_frame'].columnconfigure(0, weight=1)
        self.widgets['train_test_val_label'] = CTkLabel(self.widgets['train_test_val_frame'], text='Train/Val/Test Split', font=CTkFont(weight='bold', size=15))
        self.widgets['train_test_ratio_label'] = CTkLabel(self.widgets['train_test_val_frame'], text=f'Train: {self.args["train_ratio"].get()}%, Test: {100 - self.args["train_ratio"].get()}%')
        self.widgets['train_test_ratio_slider'] = CTkSlider(self.widgets['train_test_val_frame'], from_=0, to=100, number_of_steps=100, variable=self.args['train_ratio'], command=self.train_test_ratio_slider_callback)
        ## Preprocessing
        self.widgets['preprocessing_frame'] = CTkFrame(self)
        self.widgets['preprocessing_frame'].columnconfigure(0, weight=1)      
        self.widgets['preprocessing_label'] = CTkLabel(self.widgets['preprocessing_frame'], text='Preprocessing', font=CTkFont(weight='bold', size=15))
        ### Crop
        self.widgets['crop_frame'] = CTkFrame(self.widgets['preprocessing_frame'])
        self.widgets['crop_frame'].columnconfigure(0, weight=1)
        self.widgets['crop_frame'].columnconfigure(1, weight=1)
        self.widgets['crop_switch'] = CTkSwitch(self.widgets['crop_frame'] , text='Crop', command=self.crop_switch_event)
        self.widgets['top_ratio_label'] = CTkLabel(self.widgets['crop_frame'], text=f'Top Ratio: {self.args["top_ratio"].get()}%')
        self.widgets['top_ratio_slider'] = CTkSlider(self.widgets['crop_frame'] , from_=0, to=100, number_of_steps=100, variable=self.args['top_ratio'], command=self.top_ratio_slider_callback)
        self.widgets['bottom_ratio_label'] = CTkLabel(self.widgets['crop_frame'], text=f'Bottom Ratio: {self.args["bottom_ratio"].get()}%')
        self.widgets['bottom_ratio_slider'] = CTkSlider(self.widgets['crop_frame'] , from_=0, to=100, number_of_steps=100, variable=self.args['bottom_ratio'], command=self.bottom_ratio_slider_callback)
        self.widgets['right_ratio_label'] = CTkLabel(self.widgets['crop_frame'], text=f'Right Ratio: {self.args["right_ratio"].get()}%')
        self.widgets['right_ratio_slider'] = CTkSlider(self.widgets['crop_frame'] , from_=0, to=100, number_of_steps=100, variable=self.args['right_ratio'], command=self.right_ratio_slider_callback)
        self.widgets['left_ratio_label'] = CTkLabel(self.widgets['crop_frame'], text=f'Left Ratio: {self.args["left_ratio"].get()}%')
        self.widgets['left_ratio_slider'] = CTkSlider(self.widgets['crop_frame'] , from_=0, to=100, number_of_steps=100, variable=self.args['left_ratio'], command=self.left_ratio_slider_callback)
        ### Resize
        self.widgets['resize_frame'] = CTkFrame(self.widgets['preprocessing_frame'])
        self.widgets['resize_frame'].columnconfigure(0, weight=1) 
        self.widgets['resize_frame'].columnconfigure(1, weight=1) 
        self.widgets['resize_switch'] = CTkSwitch(self.widgets['resize_frame'] , text='Resize', command=self.resize_switch_event)
        self.widgets['width'] = CTkEntry(self.widgets['resize_frame'], placeholder_text='Width')
        self.widgets['height'] = CTkEntry(self.widgets['resize_frame'], placeholder_text='Height')
        ### Grayscale
        self.widgets['grayscale_frame'] = CTkFrame(self.widgets['preprocessing_frame'])
        self.widgets['grayscale_switch'] = CTkSwitch(self.widgets['grayscale_frame'] , text='Grayscale')
        ## Augmentation
        self.widgets['augmentation_frame'] = CTkFrame(self)
        self.widgets['augmentation_frame'].columnconfigure(0, weight=1) 
        self.widgets['augmentation_label'] = CTkLabel(self.widgets['augmentation_frame'], text='Augmentation', font=CTkFont(weight='bold', size=15))
        ### Rotation
        self.widgets['rotation_frame'] = CTkFrame(self.widgets['augmentation_frame'])
        self.widgets['rotation_switch'] = CTkSwitch(self.widgets['rotation_frame'] , text='Rotation', command=self.rotation_switch_event)
        self.widgets['rotation_label'] = CTkLabel(self.widgets['rotation_frame'], text=f'Rotation Angle: {self.args["rotation"].get()}°')
        self.widgets['rotation_slider'] = CTkSlider(self.widgets['rotation_frame'] , from_=0, to=45, number_of_steps=45, variable=self.args['rotation'], command=self.rotation_slider_callback)
        ### Blur
        self.widgets['blur_frame'] = CTkFrame(self.widgets['augmentation_frame'])
        self.widgets['blur_switch'] = CTkSwitch(self.widgets['blur_frame'] , text='Blur', command=self.blur_switch_event)
        self.widgets['blur_label'] = CTkLabel(self.widgets['blur_frame'], text=f'Blur: {self.args["blur"].get()}px')
        self.widgets['blur_slider'] = CTkSlider(self.widgets['blur_frame'] , from_=1, to=25, number_of_steps=25, variable=self.args['blur'], command=self.blur_slider_callback)
        ### Cutout
        self.widgets['cutout_frame'] = CTkFrame(self.widgets['augmentation_frame'])
        self.widgets['cutout_switch'] = CTkSwitch(self.widgets['cutout_frame'] , text='Cutout', command=self.cutout_switch_event)
        self.widgets['percent_label'] = CTkLabel(self.widgets['cutout_frame'], text=f'Percent: {self.args["percent"].get()}%')
        self.widgets['percent_slider'] = CTkSlider(self.widgets['cutout_frame'] , from_=0, to=100, number_of_steps=100, variable=self.args['percent'], command=self.percent_slider_callback)
        self.widgets['count_label'] = CTkLabel(self.widgets['cutout_frame'], text=f'Count: {self.args["count"].get()}')
        self.widgets['count_slider'] = CTkSlider(self.widgets['cutout_frame'] , from_=0, to=25, number_of_steps=20, variable=self.args['count'], command=self.count_slider_callback)
        ## Generate
        self.widgets['generate_frame'] = CTkFrame(self)
        self.widgets['generate_frame'].columnconfigure(0, weight=1) 
        self.widgets['generate_label'] = CTkLabel(self.widgets['generate_frame'], text='Generate', font=CTkFont(weight='bold', size=15))
        self.widgets['generate_button'] = CTkButton(self.widgets['generate_frame'], text='Generate', command=self.generate_button_event)
        self.widgets['generate_progressbar'] = CTkProgressBar(self.widgets['generate_frame'], progress_color="red")
        self.widgets['generate_progressbar'].set(0)

        # Grid labels to frames
        self.widgets['source_images_label'].grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsw")
        self.widgets['train_test_val_label'].grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        self.widgets['preprocessing_label'].grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        self.widgets['augmentation_label'].grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        self.widgets['generate_label'].grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        
        self.widgets['crop_switch'].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets['resize_switch'].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets['grayscale_switch'].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets['rotation_switch'].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets['blur_switch'].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets['cutout_switch'].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label.bind('<Button-1>', self.grid_widgets)
        self.widgets['source_images_label'].bind('<Button-1>', self.grid_source_images_widgets)
        self.widgets['train_test_val_label'].bind('<Button-1>', self.grid_train_test_val_widgets)
        self.widgets['preprocessing_label'].bind('<Button-1>', self.grid_preprocessing_widgets)
        self.widgets['augmentation_label'].bind('<Button-1>', self.grid_augmentation_widgets)
        self.widgets['generate_label'].bind('<Button-1>', self.grid_generate_widgets)

    def grid_widgets(self, event):
        if not self.expand:
            self.widgets['source_images_frame'].grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.widgets['train_test_val_frame'].grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            self.widgets['preprocessing_frame'].grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            self.widgets['augmentation_frame'].grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
            self.widgets['generate_frame'].grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        else:
            self.widgets['source_images_frame'].grid_forget()
            self.widgets['train_test_val_frame'].grid_forget()
            self.widgets['preprocessing_frame'].grid_forget()
            self.widgets['augmentation_frame'].grid_forget()
            self.widgets['generate_frame'].grid_forget()
        self.expand = not self.expand

    def grid_source_images_widgets(self, event):
        if not self.source_images_expand:
            self.widgets['data_folder_button'].grid(row=1, column=0, rowspan=2, padx=10, pady=10)
            self.widgets['nb_images_label'].grid(row=1, column=1, padx=10, pady=(10,0), sticky="nsew")
            self.widgets['nb_class_label'].grid(row=2, column=1, padx=10, pady=(0,10), sticky="nsew")
        else:
            self.widgets['data_folder_button'].grid_forget()
            self.widgets['nb_images_label'].grid_forget()
            self.widgets['nb_class_label'].grid_forget()
        self.source_images_expand = not self.source_images_expand

    def grid_train_test_val_widgets(self, event):
        if not self.train_test_val_expand:
            self.widgets['train_test_ratio_label'].grid(row=1, column=0, padx=10, pady=(10,0), sticky="nsew")
            self.widgets['train_test_ratio_slider'].grid(row=2, column=0, padx=10, pady=(0,10), sticky="ew")
        else:
            self.widgets['train_test_ratio_label'].grid_forget()
            self.widgets['train_test_ratio_slider'].grid_forget()
        self.train_test_val_expand = not self.train_test_val_expand

    def grid_preprocessing_widgets(self, event=None):
        if not self.preprocessing_expand:
            ### Crop
            self.widgets['crop_frame'].grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            ### Resize
            self.widgets['resize_frame'].grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            ### Grayscale
            self.widgets['grayscale_frame'].grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        else:
            ### Crop
            self.widgets['crop_frame'].grid_forget()
            ### Resize
            self.widgets['resize_frame'].grid_forget()
            ### Grayscale
            self.widgets['grayscale_frame'].grid_forget()
        self.preprocessing_expand = not self.preprocessing_expand

    def grid_augmentation_widgets(self, event=None):
        if not self.augmentation_expand:
            ### Rotation
            self.widgets['rotation_frame'].grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            ### Blur
            self.widgets['blur_frame'].grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            ### Cutout
            self.widgets['cutout_frame'].grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        else:
            ### Rotation
            self.widgets['rotation_frame'].grid_forget()
            ### Blur
            self.widgets['blur_frame'].grid_forget()
            ### Cutout
            self.widgets['cutout_frame'].grid_forget()
        self.augmentation_expand = not self.augmentation_expand

    def grid_generate_widgets(self, event=None):
        if not self.generate_expand:
            self.widgets['generate_button'].grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.widgets['generate_progressbar'].grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        else:
            self.widgets['generate_button'].grid_forget()
            self.widgets['generate_progressbar'].grid_forget()
        self.generate_expand = not self.generate_expand

    def crop_switch_event(self):
        if self.widgets['crop_switch'].get():
            self.args['pp_operations'].append('crop')
            self.widgets['top_ratio_label'].grid(row=1, column=0, padx=10, pady=10, sticky="w")
            self.widgets['top_ratio_slider'].grid(row=1, column=1, padx=10, pady=10, sticky="ew")
            self.widgets['bottom_ratio_label'].grid(row=2, column=0, padx=10, pady=10, sticky="w")
            self.widgets['bottom_ratio_slider'].grid(row=2, column=1, padx=10, pady=10, sticky="ew")
            self.widgets['right_ratio_label'].grid(row=3, column=0, padx=10, pady=10, sticky="w")
            self.widgets['right_ratio_slider'].grid(row=3, column=1, padx=10, pady=10, sticky="ew")
            self.widgets['left_ratio_label'].grid(row=4, column=0, padx=10, pady=10, sticky="w")
            self.widgets['left_ratio_slider'].grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        else:
            self.args['pp_operations'].remove('crop')
            self.widgets['top_ratio_label'].grid_forget()
            self.widgets['top_ratio_slider'].grid_forget()
            self.widgets['bottom_ratio_label'].grid_forget()
            self.widgets['bottom_ratio_slider'].grid_forget()
            self.widgets['right_ratio_label'].grid_forget()
            self.widgets['right_ratio_slider'].grid_forget()
            self.widgets['left_ratio_label'].grid_forget()
            self.widgets['left_ratio_slider'].grid_forget()

    def resize_switch_event(self):
        if self.widgets['resize_switch'].get():
            self.args['pp_operations'].append('resize')
            self.widgets['width'].grid(row=1, column=0, padx=(10,5), pady=10, sticky="nsew")
            self.widgets['height'].grid(row=1, column=1, padx=(5,10), pady=10, sticky="nsew")
        else:
            self.args['pp_operations'].remove('resize')
            self.widgets['width'].grid_forget()
            self.widgets['height'].grid_forget()
        
    def grayscale_switch_event(self):
        if self.widgets['grayscale_switch'].get():
            self.args['pp_operations'].append('grayscale')
        else:
            self.args['pp_operations'].remove('grayscale')

    def rotation_switch_event(self):
        if self.widgets['rotation_switch'].get():
            self.args['aug_operations'].append('rotation')
            self.widgets['rotation_label'].grid(row=1, column=0, padx=(10,5), pady=10, sticky="ew")
            self.widgets['rotation_slider'].grid(row=1, column=1, padx=(5,10), pady=10, sticky="ew")
        else:
            self.args['aug_operations'].remove('rotation')
            self.widgets['rotation_label'].grid_forget()
            self.widgets['rotation_slider'].grid_forget()

    def blur_switch_event(self):
        if self.widgets['blur_switch'].get():
            self.args['aug_operations'].append('blur')
            self.widgets['blur_label'].grid(row=1, column=0, padx=(10,5), pady=10, sticky="ew")
            self.widgets['blur_slider'].grid(row=1, column=1, padx=(5,10), pady=10, sticky="ew")
        else:
            self.args['aug_operations'].remove('blur')
            self.widgets['blur_label'].grid_forget()
            self.widgets['blur_slider'].grid_forget()

    def cutout_switch_event(self):
        if self.widgets['cutout_switch'].get():
            self.args['aug_operations'].append('cutout')
            self.widgets['percent_label'].grid(row=1, column=0, padx=(10,5), pady=10, sticky="ew")
            self.widgets['percent_slider'].grid(row=1, column=1, padx=(5,10), pady=10, sticky="ew")
            self.widgets['count_label'].grid(row=2, column=0, padx=(10,5), pady=10, sticky="ew")
            self.widgets['count_slider'].grid(row=2, column=1, padx=(5,10), pady=10, sticky="ew")
        else:
            self.args['aug_operations'].remove('cutout')
            self.widgets['percent_label'].grid_forget()
            self.widgets['percent_slider'].grid_forget()
            self.widgets['count_label'].grid_forget()
            self.widgets['count_slider'].grid_forget()

    def data_folder_button_event(self):
        foldername = filedialog.askdirectory()
        if foldername != '':
            self.args['data_folder'] = foldername
            path = Path(foldername)
            self.widgets['nb_images_label'].configure(text=f'Number of Images: {len(list(path.glob("*/*.jpg"))) + len(list(path.glob("*/*.png")))}')
            self.widgets['nb_class_label'].configure(text=f'Number of Classes: {len(list(path.glob("*/")))}')

    def train_test_ratio_slider_callback(self, value):
        self.widgets['train_test_ratio_label'].configure(text=f'Train: {self.args["train_ratio"].get()}%, Test: {100 - self.args["train_ratio"].get()}%')

    def top_ratio_slider_callback(self, value):
        self.widgets['to_ratio_label'].configure(text=f'Top Ratio: {self.args["top_ratio"].get()}%')

    def bottom_ratio_slider_callback(self, value):
        self.widgets['bottom_ratio_label'].configure(text=f'Bottom Ratio: {self.args["bottom_ratio"].get()}%')

    def right_ratio_slider_callback(self, value):
        self.widgets['right_ratio_label'].configure(text=f'Right Ratio: {self.args["right_ratio"].get()}%')

    def left_ratio_slider_callback(self, value):
        self.widgets['left_ratio_label'].configure(text=f'Left Ratio: {self.args["left_ratio"].get()}%')



    def rotation_slider_callback(self, value):
        self.widgets['rotation_label'].configure(text=f'Rotation Angle: {self.args["rotation"].get()}°')

    def blur_slider_callback(self, value):
        self.widgets['blur_label'].configure(text=f'Blur: {self.args["blur"].get()}px')

    def percent_slider_callback(self, value):
        self.widgets['percent_label'].configure(text=f'Percent: {self.args["percent"].get()}%')

    def count_slider_callback(self, value):
        self.widgets['count_label'].configure(text=f'Count: {self.args["count"].get()}')


    def generate_button_event(self):
        self.widgets['generate_progressbar'].configure(progress_color='red')
        self.args['width'] = int(self.widgets['width'].get()) if self.widgets['width'].get() != '' else None
        self.args['height'] = int(self.widgets['height'].get()) if self.widgets['height'].get() != '' else None        
        self.master.generate_dataset(
            self.args['data_folder'],
            self.args['train_ratio'].get() / 100,
            self.args['pp_operations'],
            self.args['top_ratio'].get() / 100,
            self.args['bottom_ratio'].get() / 100,
            self.args['right_ratio'].get() / 100,
            self.args['left_ratio'].get() / 100,
            self.args['width'],
            self.args['height'],
            self.args['aug_operations'],
            self.args['rotation'].get(),
            self.args['blur'].get(),
            self.args['percent'].get() / 100,
            self.args['count'].get(),
            self.widgets['generate_progressbar']
        )