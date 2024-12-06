import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import os
from flask import Flask, render_template, request
import threading

# Initialize Flask
app = Flask(__name__)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Tkinter GUI-related functions
def speak(text, gender, speed):
    voices = engine.getProperty("voices")

    def setvoice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
        else:
            engine.setProperty('voice', voices[1].id)

        if speed == "Fast":
            engine.setProperty('rate', 250)
        elif speed == "Normal":
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 60)

        engine.say(text)
        engine.runAndWait()

    if text:
        setvoice()

def download(text, gender, speed):
    voices = engine.getProperty("voices")

    def setvoice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
        else:
            engine.setProperty('voice', voices[1].id)

        if speed == "Fast":
            engine.setProperty('rate', 250)
        elif speed == "Normal":
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 60)

        path = filedialog.askdirectory()
        os.chdir(path)
        engine.save_to_file(text, 'text.mp3')
        engine.runAndWait()

    if text:
        setvoice()

# Flask route for the main page
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page for the interface

# Flask route to handle text to speech requests
@app.route('/speak', methods=['POST'])
def flask_speak():
    text = request.form['text']
    gender = request.form['gender']
    speed = request.form['speed']
    threading.Thread(target=speak, args=(text, gender, speed)).start()
    return "Speaking..."

# Flask route to handle download request
@app.route('/download', methods=['POST'])
def flask_download():
    text = request.form['text']
    gender = request.form['gender']
    speed = request.form['speed']
    threading.Thread(target=download, args=(text, gender, speed)).start()
    return "Downloading..."

def start_flask():
    app.run(host='0.0.0.0', port=5000)

# Run Flask app
if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Initialize Tkinter GUI
    root = Tk()
    root.title("Text to Speech")
    root.geometry("900x450+300+200")
    root.resizable(False, False)
    root.configure(bg="#305065")

    # Tkinter Components
    text_area = Text(root, font="Robote 20", bg="white", relief=GROOVE, wrap=WORD)
    text_area.place(x=10, y=150, width=500, height=250)

    gender_combobox = Combobox(root, values=['Male', 'Female'], font="arial 14", state='r', width=10)
    gender_combobox.place(x=550, y=175)
    gender_combobox.set('Male')

    speed_combobox = Combobox(root, values=['Fast', 'Normal', 'Slow'], font="arial 14", state='r', width=10)
    speed_combobox.place(x=730, y=175)
    speed_combobox.set('Normal')

    # Button for speaking text
    speak_button = Button(root, text=" Speak", font="arial 14 bold", command=lambda: speak(text_area.get(1.0, END), gender_combobox.get(), speed_combobox.get()))
    speak_button.place(x=550, y=250)

    # Button for saving text as speech
    save_button = Button(root, text=" Save", font="arial 14 bold", command=lambda: download(text_area.get(1.0, END), gender_combobox.get(), speed_combobox.get()))
    save_button.place(x=730, y=250)

    # Button to clear text
    clear_button = Button(root, text="Clear Text", font="arial 18 bold", command=lambda: text_area.delete(1.0, END))
    clear_button.place(x=550, y=350)

    # Button for closing the Tkinter window
    exit_button = Button(root, text="Exit", bg="red", fg="black", font="arial 18 bold", width=8, command=root.destroy)
    exit_button.place(x=735, y=350)

    root.mainloop()
