import tkinter as tk
from tkinter import messagebox, Toplevel
from ttkbootstrap import Style
from ttkbootstrap.tableview import Tableview
import sqlite3

def delete_row():
    selected_items = dv.get_selected_items()
    if selected_items:
        confirmation = messagebox.askyesno("Kustuta rida", "Kas olete kindel, et soovite need read kustutada?")
        if confirmation:
            for item in selected_items:
                row_id = item[0]
                dv.delete_row(row_id)
                delete_from_database(row_id)
            show_percentage()

def delete_from_database(row_id):
    connection = sqlite3.connect('epood_tkandmaa.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tkandmaa WHERE id=?', (row_id,))
    connection.commit()
    connection.close()

def show_percentage():
    connection = sqlite3.connect('epood_tkandmaa.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM tkandmaa')
    total_cars = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tkandmaa WHERE car_make=?', ('Audi',))
    audi_count = cursor.fetchone()[0]

    audi_percentage = (audi_count / total_cars) * 100

    percentage_text.set("Audisi kokku on: {:.2f}%".format( audi_percentage))

    cursor.close()
    connection.close()

def add_data():
    add_data_window = Toplevel(root)
    add_data_window.title("Lisa Andmed")

    tk.Label(add_data_window, text="First Name:").grid(row=0, column=0)
    tk.Label(add_data_window, text="Last Name:").grid(row=1, column=0)
    tk.Label(add_data_window, text="Email:").grid(row=2, column=0)
    tk.Label(add_data_window, text="Car Make:").grid(row=3, column=0)
    tk.Label(add_data_window, text="Car Model:").grid(row=4, column=0)
    tk.Label(add_data_window, text="Car Year:").grid(row=5, column=0)
    tk.Label(add_data_window, text="Car Price:").grid(row=6, column=0)

    global entry_first_name, entry_last_name, entry_email, entry_car_make, entry_car_model, entry_car_year, entry_car_price
    entry_first_name = tk.Entry(add_data_window)
    entry_last_name = tk.Entry(add_data_window)
    entry_email = tk.Entry(add_data_window)
    entry_car_make = tk.Entry(add_data_window)
    entry_car_model = tk.Entry(add_data_window)
    entry_car_year = tk.Entry(add_data_window)
    entry_car_price = tk.Entry(add_data_window)

    entry_first_name.grid(row=0, column=1)
    entry_last_name.grid(row=1, column=1)
    entry_email.grid(row=2, column=1)
    entry_car_make.grid(row=3, column=1)
    entry_car_model.grid(row=4, column=1)
    entry_car_year.grid(row=5, column=1)
    entry_car_price.grid(row=6, column=1)

    tk.Button(add_data_window, text="Lisa Andmed", command=save_data).grid(row=7, columnspan=2, pady=10)

def save_data():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    car_make = entry_car_make.get()
    car_model = entry_car_model.get()
    car_year = entry_car_year.get()
    car_price = entry_car_price.get()

    connection = sqlite3.connect('epood_tkandmaa.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tkandmaa (first_name, last_name, email, car_make, car_model, car_year, car_price) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (first_name, last_name, email, car_make, car_model, car_year, car_price))
    connection.commit()
    connection.close()

    messagebox.showinfo("Andmete lisamine", "Andmed on edukalt lisatud andmebaasi.")
    dv.load_table_data()
    show_percentage()

root = tk.Tk()
root.geometry("800x400")
root.title("Andmete Haldamine")
style = Style(theme='darkly')

l1 = [
    {"text": "id", "stretch": False},
    {"text":"first_name","stretch":True},
    {"text":"last_name","stretch":True},
    {"text":"email","stretch":True},
    {"text":"car_make","stretch":True},
    {"text":"car_model","stretch":True},
    {"text":"car_year","stretch":True},
    {"text":"car_price","stretch":True}
]

connection = sqlite3.connect('epood_tkandmaa.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM tkandmaa')
r_set = cursor.fetchall()
connection.close()

dv = Tableview(
    master=root,
    paginated=True,
    coldata=l1,
    rowdata=r_set,
    searchable=True,
    bootstyle='flatly',  # Muuda stiili vastavalt soovile
    pagesize=10,
    height=10
)
dv.grid(row=0, column=0, padx=10, pady=5)
dv.autofit_columns()

tk.Button(root, text="Lisa Andmed", command=add_data).grid(row=1, column=0, padx=10, pady=5)
tk.Button(root, text="Kustuta Valitud Read", command=delete_row).grid(row=2, column=0, padx=10, pady=5)

percentage_text = tk.StringVar()
percentage_label = tk.Label(root, textvariable=percentage_text, font=('Arial', 12), justify='left')
percentage_label.grid(row=3, column=0, padx=10, pady=5)
show_percentage()

root.mainloop()
