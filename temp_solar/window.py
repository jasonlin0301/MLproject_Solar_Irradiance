import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

# Load data from CSV
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2.csv'
data = pd.read_csv(file_path)

# Function to display selected image
def display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((800, 600))  # Resize image to fit in the window
    img = ImageTk.PhotoImage(image)
    img_label.config(image=img)
    img_label.image = img

# Create main window
root = tk.Tk()
root.title("CSV Viewer with Images")

# Create a Treeview widget
tree = ttk.Treeview(root)
tree["columns"] = list(data.columns)
tree["show"] = "headings"

for col in data.columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

# Add data to the treeview
for index, row in data.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(side="left", fill="y")

# Create a Frame for the buttons and image display
frame = ttk.Frame(root)
frame.pack(side="right", fill="both", expand=True)

# Create buttons
button_texts = [
    ("Boxplot", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\boxplot_no_outliers.png"),
    ("Statistical Summary", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\data.png"),
    ("Heatmap", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\heatmap.png"),
    ("Linear Regression 1", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\linear_regression.png"),
    ("Linear Regression 2", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\linear_regression01.png"),
    ("Linear Regression 3", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\linear_regression02.png"),
]

for text, path in button_texts:
    button = ttk.Button(frame, text=text, command=lambda p=path: display_image(p))
    button.pack(fill="x")

# Label to display the image
img_label = ttk.Label(frame)
img_label.pack(fill="both", expand=True)

# Run the application
root.mainloop()
