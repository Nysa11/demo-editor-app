from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PIL import Image, ImageEnhance
import os

class ImageProcessor:
    def __init__(self):
        self.current_image = None
        self.current_filename = ''
        self.history = []  # To keep track of image states for undo

    def loadImage(self, folder, filename):
        self.current_filename = filename
        image_path = os.path.join(folder, filename)
        self.current_image = Image.open(image_path)
        self.history = [self.current_image.copy()]  # Reset history with the original image

    def showImage(self, label):
        if self.current_image:
            self.current_image.save('temp.png')  # Save the current image as a temporary file
            pixmap = QPixmap('temp.png')  # Load the temporary file into QPixmap
            label.setPixmap(pixmap)  # Set the QPixmap on the QLabel

    def do_bw(self):
        if self.current_image:
            self.history.append(self.current_image.copy())  # Save current state to history
            self.current_image = self.current_image.convert("L")
            self.showImage(label_image)  # Refresh the displayed image

    def do_mirror(self):
        if self.current_image:
            self.history.append(self.current_image.copy())  # Save current state to history
            self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.showImage(label_image)  # Refresh the displayed image

    def do_left(self):
        if self.current_image:
            self.history.append(self.current_image.copy())  # Save current state to history
            self.current_image = self.current_image.rotate(90, expand=True)
            self.showImage(label_image)  # Refresh the displayed image

    def do_right(self):
        if self.current_image:
            self.history.append(self.current_image.copy())  # Save current state to history
            self.current_image = self.current_image.rotate(-90, expand=True)
            self.showImage(label_image)  # Refresh the displayed image

    def do_sharpness(self):
        if self.current_image:
            self.history.append(self.current_image.copy())  # Save current state to history
            if self.current_image.mode != 'RGB':
                self.current_image = self.current_image.convert('RGB')
            enhancer = ImageEnhance.Sharpness(self.current_image)
            self.current_image = enhancer.enhance(2)  # Increase sharpness
            self.showImage(label_image)  # Refresh the displayed image

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()  # Remove the last state
            self.current_image = self.history[-1].copy()  # Revert to the previous state
            self.showImage(label_image)  # Refresh the displayed image

    def saveImage(self, folder):
        if self.current_image:
            modified_dir = os.path.join(folder, 'Modified')
            os.makedirs(modified_dir, exist_ok=True)
            save_path = os.path.join(modified_dir, self.current_filename)
            self.current_image.save(save_path)
            print(f"Image saved to {save_path}")

app = QApplication([])
window = QWidget()
window.resize(700, 500)
window.setWindowTitle('Easy Editor')

# Interface elements
label_image = QLabel("Image")
label_image.setAlignment(Qt.AlignCenter)
list_files = QListWidget()

# Button elements
button_folder = QPushButton("Folder")
button_left = QPushButton("Left")
button_right = QPushButton("Right")
button_mirror = QPushButton("Mirror")
button_sharpness = QPushButton("Sharpness")
button_bw = QPushButton("B/W")
button_undo = QPushButton("Undo")

# Layout setup
row1 = QHBoxLayout()
row2 = QHBoxLayout()
column1 = QVBoxLayout()
column2 = QVBoxLayout()

column1.addWidget(button_folder)
column1.addWidget(list_files)

column2.addWidget(label_image)

row2.addWidget(button_left)
row2.addSpacing(10)  # Add spacing between buttons
row2.addWidget(button_right)
row2.addSpacing(10)  # Add spacing between buttons
row2.addWidget(button_mirror)
row2.addSpacing(10)  # Add spacing between buttons
row2.addWidget(button_sharpness)
row2.addSpacing(10)  # Add spacing between buttons
row2.addWidget(button_bw)
row2.addSpacing(10)  # Add spacing between buttons
row2.addWidget(button_undo)

column2.addLayout(row2)

row1.addLayout(column1)
row1.addLayout(column2)

window.setLayout(row1)

# Global variable to store the selected work directory
workdir = ''

# Event handling function to open folder dialog and set workdir
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory(window, 'Select Folder', os.getcwd())
    if workdir:
        handler()

# Function to filter and return files with specific extensions
def filter():
    extensions = ['.png', '.jpg', '.jpeg', '.gif']
    return [file_name for file_name in os.listdir(workdir) if any(file_name.lower().endswith(ext) for ext in extensions)]

# Handler function for Folder button click
def handler():
    if workdir:
        list_files.clear()
        filtered_files = filter()
        for file_name in filtered_files:
            item = QListWidgetItem(file_name)
            item.setForeground(QColor('white'))  # Set file name color to white
            list_files.addItem(item)

# Create an instance of ImageProcessor
image_processor = ImageProcessor()

# Event handling for selecting a file from the list
def onFileSelected(item):
    filename = item.text()
    image_processor.loadImage(workdir, filename)
    image_processor.showImage(label_image)

# Function to apply filters and save the image
def apply_bw_and_save():
    image_processor.do_bw()
    image_processor.saveImage(workdir)

def apply_mirror_and_save():
    image_processor.do_mirror()
    image_processor.saveImage(workdir)

def apply_right_and_save():
    image_processor.do_right()
    image_processor.saveImage(workdir)

def apply_left_and_save():
    image_processor.do_left()
    image_processor.saveImage(workdir)

def apply_sharpness_and_save():
    image_processor.do_sharpness()
    image_processor.saveImage(workdir)

# Connect signals and slots
button_folder.clicked.connect(chooseWorkdir)
list_files.itemClicked.connect(onFileSelected)
button_bw.clicked.connect(apply_bw_and_save)
button_left.clicked.connect(apply_left_and_save)
button_mirror.clicked.connect(apply_mirror_and_save)
button_right.clicked.connect(apply_right_and_save)
button_sharpness.clicked.connect(apply_sharpness_and_save)
button_undo.clicked.connect(image_processor.undo)

# Set background color of window and other styles
window.setStyleSheet("""
    QWidget {
        background-color: #222222;
        color: white;
    }
    QPushButton {
        background-color: #444444;
        color: white;
        border: none;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #555555;
    }
    QPushButton:pressed {
        background-color: #ffffff;
        color: #222222;
    }
    QLabel {
        color: white;
    }
    QListWidget {
        background-color: #333333;
        color: white;
    }
""")

# Show the main window
window.show()

# Start the application event loop
app.exec_()
