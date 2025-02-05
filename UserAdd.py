import cv2
import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import io

# SQLite baza bilan ishlash
def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        surname TEXT,
                        photo BLOB)''')
    conn.commit()
    conn.close()

def save_user_to_db(name, surname, photos):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Rasmlarni BLOB formatida saqlash
    for photo in photos:
        # Rasmni binar formatga o'tkazish
        photo_binary = convert_to_binary(photo)
        cursor.execute("INSERT INTO users (name, surname, photo) VALUES (?, ?, ?)",
                       (name, surname, photo_binary))

    conn.commit()
    conn.close()

# Rasmni binar formatga o'tkazish
def convert_to_binary(image):
    # Rasmlarni JPEG formatida saqlash va binar formatga aylantirish
    _, buffer = cv2.imencode('.jpg', image)
    return buffer.tobytes()

# Yuzni tanib olish va rasm olish funksiyasi
def capture_images():
    # Web kamerasini ochish
    cam = cv2.VideoCapture(1)
    
    # Yuzni tanish uchun OpenCV cascadi
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Rasm olish va 30 ta rasm saqlash
    images = []
    count = 0
    while count < 50:
        ret, frame = cam.read()
        if not ret:
            break
        
        # Rasmni kulrangga o'tkazish
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yuzni aniqlash
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Foydalanuvchining yuzini kesib olish
            face = frame[y:y + h, x:x + w]
            images.append(face)
            count += 1
        
        # Kamerani namoyish qilish
        cv2.imshow("Frame", frame)

        # "q" tugmasini bosish orqali chiqish
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamerani yopish
    cam.release()
    cv2.destroyAllWindows()

    # Rasmlarni qaytarish
    return images

# GUI oynasini yaratish
def show_gui():
    def on_add_user():
        name = entry_name.get()
        surname = entry_surname.get()
        if name and surname:
            # Foydalanuvchi rasmlarini olish
            photos = capture_images()
            if photos:
                # Rasmlar va foydalanuvchi ma'lumotlarini bazaga saqlash
                save_user_to_db(name, surname, photos)
                messagebox.showinfo("Success", "User added successfully!")
            else:
                messagebox.showerror("Error", "No face detected!")
        else:
            messagebox.showerror("Error", "Please enter name and surname.")

    root = tk.Tk()
    root.title("Add User")

    label_name = tk.Label(root, text="Name")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_surname = tk.Label(root, text="Surname")
    label_surname.pack()
    entry_surname = tk.Entry(root)
    entry_surname.pack()

    button_add_user = tk.Button(root, text="Add User", command=on_add_user)
    button_add_user.pack()

    root.mainloop()

# Dastur ishga tushirish
if __name__ == "__main__":
    create_db()
    show_gui()
