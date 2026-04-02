import numpy as np
import tkinter as tk
from tkinter import *
from tensorflow.keras.models import load_model
from PIL import Image, ImageDraw, ImageOps


print("Loading model...")
model = load_model("two_digit_model.h5")
print(" Model loaded!")


class TwoDigitRecognizerApp(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.title("Two-Digit Handwritten Recognition")
        self.geometry("350x450")
        self.resizable(0,0)
        self.model = model

        self.canvas = Canvas(self, width=280, height=140, bg='white')
        self.canvas.pack(pady=20)

        btn_frame = Frame(self)
        btn_frame.pack()
        Button(btn_frame, text="Predict", command=self.predict_digit).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Clear", command=self.clear_canvas).pack(side=LEFT)

        self.result_label = Label(self, text="Draw two digits side-by-side", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

        self.image = Image.new("L", (280, 140), color=255)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x1, y1 = (event.x-8), (event.y-8)
        x2, y2 = (event.x+8), (event.y+8)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black', outline='black')
        self.draw.ellipse([x1, y1, x2, y2], fill=0)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0,0,280,140], fill=255)
        self.result_label.config(text="Draw two digits side-by-side")

    def predict_digit(self):
        img_resized = self.image.resize((56, 28))
        img_inverted = ImageOps.invert(img_resized)
        img_array = np.array(img_inverted) / 255.0
        img_array = img_array.reshape(1, 28, 56, 1)

        prediction = self.model.predict(img_array)
        num = np.argmax(prediction)
        confidence = np.max(prediction)

        self.result_label.config(text=f"Prediction: {num:02d} (Conf: {confidence*100:.2f}%)")

if __name__ == "__main__":
    app = TwoDigitRecognizerApp(model)
    app.mainloop()

