import os
import cv2
import numpy as np
import random
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from pathlib import Path

from utils import images_utils

class Dataset:
    def __init__(self,
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
                 slider):
        self.data_folder = data_folder
        self.train_ratio = train_ratio
        self.val_ratio = 1 - train_ratio
        self.pp_operations = pp_operations
        self.top_ratio = top_ratio
        self.bottom_ratio = bottom_ratio
        self.right_ratio = right_ratio
        self.left_ratio = left_ratio
        self.width = width
        self.height = height
        self.aug_operations = aug_operations
        self.rotation = rotation
        self.blur = blur
        self.percent = percent
        self.count = count
        self.slider = slider
        self.class_names = self.extract_class_names()
        self.train_data, self.train_labels, self.val_data, self.val_labels = self.load_data()
                
    def extract_class_names(self):
        class_names = []
        for root, dirs, files in os.walk(self.data_folder):
            for dir_name in dirs:
                class_names.append(dir_name)
        return class_names
    
    def load_data(self):
        data = []
        labels = []
        num_samples = len(self.class_names)
        path = Path(self.data_folder)
        nb_images = len(list(path.glob('*/*.jpg'))) + len(list(path.glob('*/*.png')))
        idx_image = 0

        for class_idx, class_name in enumerate(self.class_names):
            class_folder = os.path.join(self.data_folder, class_name)
            class_data = []
            class_labels = []
            class_progress_bar = tqdm(os.listdir(class_folder), desc=f"Loading class {class_name}")

            for file_name in class_progress_bar:
                idx_image += 1
                file_path = os.path.join(class_folder, file_name)
                image = cv2.imread(file_path)  # Charger l'image avec OpenCV
                if image is not None:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    preprocessed_image = self.preprocess_image(image)  # Prétraiter l'image
                    class_data.append(preprocessed_image)
                    class_labels.append(class_idx)
                self.slider.set(idx_image / nb_images)

            data.extend(class_data)
            labels.extend(class_labels)

            class_progress_bar.close()
        self.slider.configure(progress_color="green")

        if len(self.aug_operations) > 0:
            balanced_data, balanced_labels = self.balance_class_names(data, labels)
        else:
            balanced_data = data
            balanced_labels = labels

        # Mélanger les données et les labels tout en conservant l'association
        combined_data = list(zip(balanced_data, balanced_labels))
        random.shuffle(combined_data)
        balanced_data[:], balanced_labels[:] = zip(*combined_data)

        # Séparation en ensembles d'entraînement et de validation
        train_data, val_data, train_labels, val_labels = train_test_split(balanced_data, balanced_labels,
                                                                            test_size=self.val_ratio,
                                                                            stratify=balanced_labels,
                                                                            random_state=42)

        # Affichage du nombre d'images par classe dans l'ensemble d'entraînement
        print("Nombre d'images par classe dans l'ensemble d'entraînement:")
        train_counts = {class_name: train_labels.count(class_idx) for class_idx, class_name in enumerate(self.class_names)}
        for class_name, count in train_counts.items():
            print(f"{class_name}: {count}")

        # Affichage du nombre d'images par classe dans l'ensemble de validation
        print("\nNombre d'images par classe dans l'ensemble de validation:")
        val_counts = {class_name: val_labels.count(class_idx) for class_idx, class_name in enumerate(self.class_names)}
        for class_name, count in val_counts.items():
            print(f"{class_name}: {count}")

        return train_data, train_labels, val_data, val_labels

    
    def balance_class_names(self, data, labels):
        class_counts = np.bincount(labels)
        max_class_count = np.max(class_counts)
        num_class_names = len(class_counts)

        balanced_data = []
        balanced_labels = []

        for class_idx in range(num_class_names):
            class_data = [d for d, l in zip(data, labels) if l == class_idx]
            class_labels = [l for l in labels if l == class_idx]
            class_count = len(class_data)
            num_augmentations = max_class_count - class_count

            if num_augmentations > 0:
                augmented_data, augmented_labels = self.augment_data(class_data, class_labels, num_augmentations)
                balanced_data.extend(augmented_data)
                balanced_labels.extend(augmented_labels)

            balanced_data.extend(class_data)
            balanced_labels.extend(class_labels)

        return balanced_data, balanced_labels
    
    def augment_data(self, data, labels, num_augmentations):
        augmented_data = []
        augmented_labels = []
        count_class = len(data)
        count = 0
        
        while count < num_augmentations:
            if num_augmentations - count > count_class:
                for j in range(len(data)):
                    image = data[j]
                    label = labels[j]
                    
                    augmented_image = self.apply_augmentation(image)
                    
                    augmented_data.append(augmented_image)
                    augmented_labels.append(label)
                count += count_class
            else:
                for j in range(num_augmentations - count):
                    image = data[j]
                    label = labels[j]
                    
                    augmented_image = self.apply_augmentation(image)
                    
                    augmented_data.append(augmented_image)
                    augmented_labels.append(label)
                count += num_augmentations - count
        
        return augmented_data, augmented_labels
    
    def apply_augmentation(self, image):
        augmented_image = image.copy()
        
        selected_operation = np.random.choice(self.aug_operations)
        if selected_operation == 'blur':
            augmented_image = images_utils.apply_blur(augmented_image, self.blur)
        elif selected_operation == 'cutout':
            augmented_image = images_utils.apply_cutout(augmented_image, self.count, self.percent)
        elif selected_operation == 'rotate':
            augmented_image = images_utils.rotate_image(augmented_image, self.rotation_angle)
        
        return augmented_image
    
    def preprocess_image(self, image):
        # Effectuer ici les opérations de prétraitement souhaitées sur l'image
        pp_image = images_utils.preprocess_image(image, self.pp_operations, self.width, self.height, self.top_ratio, self.bottom_ratio, self.left_ratio, self.right_ratio)
        return pp_image
    

    def display_samples(self, num_samples=5):
        # Affichage des échantillons d'entraînement
        print("Échantillons d'entraînement :")
        self.display_images(self.train_data, self.train_labels, num_samples)
        print()

        # Affichage des échantillons de validation
        print("Échantillons de validation :")
        self.display_images(self.val_data, self.val_labels, num_samples)
        print()

    def display_images(self, data, labels, num_samples):
        for i in range(num_samples):
            image = data[i]
            label = labels[i]
            plt.imshow(image, cmap="gray")
            plt.title(f"Classe : {self.class_names[label]}")
            plt.axis("off")
            plt.show()
