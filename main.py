import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import sqlite3
import tkinter as tk
from PIL import ImageTk, Image
from random import randint



pages = [1,2,3,4,5]
info = []
images = []
for i in pages:
    url = f'https://alta.ge/phones-and-communications/smartphones-page-{i}.html'

    r = requests.get(url)
    if r.status_code == 200:
        content = r.text

        soup = bs(content, 'html.parser')

        phone_info = soup.find_all('div', {'class':'ty-column3'})
        for each in phone_info:
            images.append(each.find('img', {'class':'ty-pict'})['src'])
            title = each.find('a', {'class':'product-title'}).text
            price = int(each.find('span', {'class':'ty-price-num'}).text)
            info.append((title, price))
        sleep(10)


base = sqlite3.connect("PhoneBase.sqlite")

cursor = base.cursor()
cursor.execute("""  CREATE TABLE phones
                    (id INTEGER PRIMARY KEY AUTOINCREMENT
                    ,name TEXT(50)
                    ,price INT);""")
base.commit()

cursor.executemany("""INSERT INTO phones
(name, price) VALUES (?,?)""", info)
base.commit()

base.close()

index = randint(0, len(images)-1)
phone_name = info[index][0].split()[0]
with open("phone.jpeg", 'wb') as img:
    img_url = images[index]
    r = requests.get(img_url)

    img.write(r.content)



def checker(event):
    global phone_name
    txt = entry_1.get()

    if txt.lower() == phone_name.lower():
        label2.config(text="Correct")
        index2 = randint(0, len(images) - 1)
        phone_name = info[index2][0].split()[0]
        with open("phone.jpeg", 'wb') as img1:
            img_url1 = images[index2]
            r2 = requests.get(img_url1)

            img1.write(r2.content)
        img2 = ImageTk.PhotoImage(Image.open("phone.jpeg"))
        panel.config(image=img2)
        panel.image = img2

    else:
        label2.config(text="Wrong")



window = tk.Tk()
window.title("Join")
window.geometry("300x350")
window.configure(background='grey')

img = ImageTk.PhotoImage(Image.open("phone.jpeg"))


panel = tk.Label(window, image = img)
label_1 = tk.Label(window, text="Guess a phone brand by image")
label_1.pack(side="top", fill="both")
entry_1 = tk.Entry(window)
entry_1.pack(side="top", fill = "both")
button1 = tk.Button(window, text="button1")
button1.pack(side="top", fill="both")
button1.bind("<Button-1>", checker)
label2 = tk.Label(window, text="")
label2.pack(side="top", fill="both")

panel.pack(side = "bottom", fill = "both")


window.mainloop()