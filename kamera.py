import cv2
import sqlite3
import os
import telegram
import asyncio
import numpy as np

# Foydalanuvchi ma'lumotlari saqlanadigan SQLite fayli
USERS_DB = 'users.db'

# SQLite ma'lumotlar bazasiga ulanish va foydalanuvchi ma'lumotlarini olish
def load_users_from_db():
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()

    # Foydalanuvchi ma'lumotlarini olish
    cursor.execute("SELECT id, name, surname, photo FROM users")  # 'user_id' o'rniga 'id'
    users = cursor.fetchall()

    conn.close()

    # Foydalanuvchi ma'lumotlarini dictionary formatida qaytarish
    user_dict = {}
    for user in users:
        user_dict[user[0]] = {'name': user[1], 'surname': user[2], 'photo': user[3]}
    
    return user_dict

# Telegramga xabar yuborish funksiyasi
async def send_alert_via_telegram(token, chat_id, message, photo_path=None, video_path=None):
    bot = telegram.Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

    if photo_path:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id=chat_id, photo=photo)

    if video_path:
        with open(video_path, 'rb') as video:
            await bot.send_video(chat_id=chat_id, video=video)

# Video yozishni boshlash funksiyasi
def start_video_recording(filename, frame_size=(640, 480), fps=20):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(filename, fourcc, fps, frame_size)

# Yuzni aniqlash va foydalanuvchini tanishish
async def detect_face_and_recognize(token, chat_id):
    cap = cv2.VideoCapture(1)  # Telefon kamerasi yoki kompyuter kamerasi
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    users = load_users_from_db()

    # Yuzni tanish uchun LBPH Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Yuzni o'rganish (har bir foydalanuvchining rasmidan)
    faces = []
    ids = []
    for user_id, user_info in users.items():
        user_photo = np.frombuffer(user_info["photo"], dtype=np.uint8)
        known_image = cv2.imdecode(user_photo, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)
        
        # Yuzni aniqlash va tanish uchun o'rnatish
        detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in detected_faces:
            faces.append(gray[y:y + h, x:x + w])
            ids.append(user_id)
    
    # Yuzlarni o'rganish
    recognizer.train(faces, np.array(ids))
    
    video_filename = 'detected_video.avi'
    video_writer = None
    recording = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera tasviri olinmadi.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(detected_faces) > 0 and not recording:
            video_writer = start_video_recording(video_filename, frame_size=(frame.shape[1], frame.shape[0]))
            recording = True
            print("Video yozishni boshladi.")

        if recording:
            video_writer.write(frame)

        for (x, y, w, h) in detected_faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_image = gray[y:y + h, x:x + w]
            
            # Yuzni tanish
            user_id, confidence = recognizer.predict(face_image)
            if confidence < 100:
                found_user = users.get(user_id, None)
                if found_user:
                    await send_alert_via_telegram(
                        token, chat_id, 
                        f"Foydalanuvchi: {found_user['name']} {found_user['surname']}", 
                        "detected_person.jpg"
                    )
                    cv2.putText(frame, f"{found_user['name']} {found_user['surname']}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                await send_alert_via_telegram(token, chat_id, "Foydalanuvchi aniqlanmadi.", "detected_person.jpg")

        cv2.imshow("Yuzni aniqlash", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if recording:
                recording = False
                video_writer.release()
                print("Video yozishni tugatdi.")
                await send_alert_via_telegram(
                    token, chat_id, 
                    "Foydalanuvchi aniqlash jarayonidagi video.", 
                    video_path=video_filename
                )
            break

    cap.release()
    if recording:
        video_writer.release()
    cv2.destroyAllWindows()

# Botning tokeni va chat_id
TOKEN = 'BOT_TOKEN'
CHAT_ID = 'CHat_id' #Admin chat id si yoziladi

async def main():
    await detect_face_and_recognize(TOKEN, CHAT_ID)

asyncio.run(main())
