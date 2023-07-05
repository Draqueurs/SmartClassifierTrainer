import tensorflow as tf
import numpy as np
import wandb
import os
import keras
import tensorflow_hub as hub
from datetime import datetime

models = {
    "efficientnetv2-b0": "https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_b0/feature_vector/2",
    "efficientnetv2-b1": "https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_b1/feature_vector/2",
    "efficientnetv2-b2": "https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_b2/feature_vector/2",
    "efficientnetv2-b3": "https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_b3/feature_vector/2",
    "efficientnetv2-b4": "https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_b4/feature_vector/2"
}

class CustomCallback(keras.callbacks.Callback):
    def __init__(self, epochs_progressbar, total_progressbar):
        super().__init__()
        self.epochs_progressbar = epochs_progressbar
        self.total_progressbar = total_progressbar

    def on_train_begin(self, logs=None):
        self.total_progressbar.configure(progress_color='red')
        self.total_progressbar.set(0)

    def on_train_end(self, logs=None):
        self.total_progressbar.configure(progress_color='green')

    def on_epoch_begin(self, epoch, logs=None):
        self.epochs_progressbar.configure(progress_color='red')
        self.epochs_progressbar.set(0)

    def on_epoch_end(self, epoch, logs=None):
        self.epochs_progressbar.configure(progress_color='green')
        self.total_progressbar.set((epoch + 1) / self.params.get('epochs', -1))

    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        self.epochs_progressbar.set((batch + 1) / self.params.get('steps', -1))


class TFTrainer:
    def __init__(self, dataset, epochs, batch_size, name=None, model=None, wandb_entity=None, wandb_project=None, epochs_progressbar=None, total_progressbar=None):
        self.dataset = dataset
        self.model = model
        self.epochs = epochs
        self.batch_size = batch_size
        if name == None:
            self.name = datetime.now().strftime("%y%m%d_%H%M%S")
        else:
            self.name = name
        self.entity = wandb_entity
        self.project = wandb_project
        self.epochs_progressbar = epochs_progressbar
        self.total_progressbar = total_progressbar

        self.num_classes = len(dataset.class_names)

        self.model = self.build_model()
        self.best_model_file = os.path.join("models", self.name, f"best_model_{self.name}.h5")

        self.class_names = self.dataset.class_names

    def build_model(self):
        if len(self.dataset.train_data[0].shape) == 2:
            channel = 1
        else:
            channel = 3

        print(self.dataset.train_data[0].shape)
        ''' 
        model = tf.keras.Sequential([
                    tf.keras.layers.Reshape(target_shape=(self.dataset.width, self.dataset.height, channel), input_shape=self.dataset.train_data[0].shape),
                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(self.num_classes, activation='softmax')
                ])
        
        model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(self.dataset.width, self.dataset.height, channel)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dropout(0.5),  # Ajout d'une couche de Dropout pour la régularisation
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.Dense(self.num_classes, activation='softmax')
                ])
        '''
        model = [tf.keras.layers.InputLayer(input_shape=self.dataset.train_data[0].shape)]

        model += [
            hub.KerasLayer(models[self.model], trainable=False),
            tf.keras.layers.Dropout(rate=0.2),
            #tf.keras.layers.Dense(512, activation='gelu'),
            tf.keras.layers.Dense(256, activation='relu'),
            #tf.keras.layers.Dense(128, activation='relu'),
            #tf.keras.layers.Dropout(rate=0.2),
            #tf.keras.layers.Dense(output_size, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(len(self.dataset.class_names)),
            tf.keras.layers.Softmax()
        ]

        model = tf.keras.Sequential(model)
        model.build([None]+[self.dataset.width, self.dataset.height, channel])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model

    def train(self):
        if self.entity is not None and self.project is not None:
            wandb.init(entity=self.entity, project=self.project, name=self.name)
        
        checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            self.best_model_file,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        )

        if self.entity is not None and self.project is not None:
            history = self.model.fit(
                np.array(self.dataset.train_data), np.array(self.dataset.train_labels),
                validation_data=(np.array(self.dataset.val_data), np.array(self.dataset.val_labels)),
                epochs=self.epochs,
                batch_size=self.batch_size,
                callbacks=[wandb.keras.WandbCallback(), checkpoint_callback, CustomCallback(self.epochs_progressbar, self.total_progressbar)]
            )
        else:
            history = self.model.fit(
                np.array(self.dataset.train_data), np.array(self.dataset.train_labels),
                validation_data=(np.array(self.dataset.val_data), np.array(self.dataset.val_labels)),
                epochs=self.epochs,
                batch_size=self.batch_size,
                callbacks=[checkpoint_callback, CustomCallback(self.epochs_progressbar, self.total_progressbar)]
            )

        return history

    def save(self, file_path):
        self.model.save(file_path)
        print(f"Model saved to {file_path}")

    def save_best_model(self):
        self.model.load_weights(self.best_model_file)
        best_model_save_path = self.best_model_file.split('.')[0] + 'saved.h5'
        self.model.save(best_model_save_path)
        print(f"Best model saved to {best_model_save_path}")