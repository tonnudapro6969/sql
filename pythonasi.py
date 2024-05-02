import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from ttkbootstrap import Style

conn = sqlite3.connect('epood_tkandmaa.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS tkandmaa (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             first_name VARCHAR(255) NOT NULL,
             last_name VARCHAR(255) NOT NULL,
             email VARCHAR(255) NOT NULL,
             car_make VARCHAR(255) NOT NULL,
             car_model VARCHAR(255) NOT NULL,
             car_year INTEGER NOT NULL,
             car_price REAL NOT NULL
             )''')

# nupud ja asjad
class AutoRakendus:
    def __init__(self, master):
        self.master = master
        self.style = Style(theme='darkly')
        self.frame = ttk.Frame(master)
        self.frame.pack(padx=10, pady=10)

    
        self.tree = ttk.Treeview(self.frame, columns=('Eesnimi', 'Perekonnanimi', 'E-post', 'Autotootja', 'Automudel', 'Aasta', 'Hind'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('Eesnimi', text='Eesnimi')
        self.tree.heading('Perekonnanimi', text='Perekonnanimi')
        self.tree.heading('E-post', text='E-post')
        self.tree.heading('Autotootja', text='Autotootja')
        self.tree.heading('Automudel', text='Automudel')
        self.tree.heading('Aasta', text='Aasta')
        self.tree.heading('Hind', text='Hind')
        self.tree.pack(side=tk.LEFT)

        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscroll=self.scrollbar.set)

 
        self.add_button = ttk.Button(master, text="Lisa", command=self.open_add_window)
        self.add_button.pack(side=tk.BOTTOM, padx=5, pady=5)


        self.delete_button = ttk.Button(master, text="Kustuta", command=self.delete_entry)
        self.delete_button.pack(side=tk.BOTTOM, padx=5, pady=5)

  
        self.search_entry = ttk.Entry(master, width=30)
        self.search_entry.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.search_entry.bind('<KeyRelease>', self.search_data)

        audi_percent = self.calculate_audi_percent()
        self.audi_label = ttk.Label(master, text=f"Audisi on kokku {audi_percent:.2f}%.")
        self.audi_label.pack(side=tk.BOTTOM, padx=5, pady=5)


        self.load_data()


    def load_data(self):

        for record in self.tree.get_children():
            self.tree.delete(record)

        # Haarame andmed andmebaasist
        c.execute("SELECT * FROM tkandmaa")
        rows = c.fetchall()

        # Lisame andmed puusse
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    # Avab eraldi aken "Lisa" nupu vajutamisel
    def open_add_window(self):
        self.add_window = tk.Toplevel(self.master)
        self.add_window.title("Lisa uus kirje")

        # Lisame sisestusväljad
        ttk.Label(self.add_window, text="Eesnimi:").grid(row=0, column=0, sticky='w')
        self.first_name_entry = ttk.Entry(self.add_window)
        self.first_name_entry.grid(row=0, column=1)

        ttk.Label(self.add_window, text="Perekonnanimi:").grid(row=1, column=0, sticky='w')
        self.last_name_entry = ttk.Entry(self.add_window)
        self.last_name_entry.grid(row=1, column=1)

        ttk.Label(self.add_window, text="E-post:").grid(row=2, column=0, sticky='w')
        self.email_entry = ttk.Entry(self.add_window)
        self.email_entry.grid(row=2, column=1)

        ttk.Label(self.add_window, text="Autotootja:").grid(row=3, column=0, sticky='w')
        self.car_make_entry = ttk.Entry(self.add_window)
        self.car_make_entry.grid(row=3, column=1)

        ttk.Label(self.add_window, text="Automudel:").grid(row=4, column=0, sticky='w')
        self.car_model_entry = ttk.Entry(self.add_window)
        self.car_model_entry.grid(row=4, column=1)

        ttk.Label(self.add_window, text="Aasta:").grid(row=5, column=0, sticky='w')
        self.car_year_entry = ttk.Entry(self.add_window)
        self.car_year_entry.grid(row=5, column=1)

        ttk.Label(self.add_window, text="Hind:").grid(row=6, column=0, sticky='w')
        self.car_price_entry = ttk.Entry(self.add_window)
        self.car_price_entry.grid(row=6, column=1)

        # Lisa nupu lisamine
        ttk.Button(self.add_window, text="Lisa", command=self.add_entry).grid(row=7, columnspan=2, pady=5)

    # Uue rea lisamine andmebaasi
    def add_entry(self):
        # Haarame sisestatud väärtused
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        car_make = self.car_make_entry.get()
        car_model = self.car_model_entry.get()
        car_year = int(self.car_year_entry.get())
        car_price = float(self.car_price_entry.get())

        # Lisame andmed andmebaasi
        c.execute("INSERT INTO tkandmaa (first_name, last_name, email, car_make, car_model, car_year, car_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (first_name, last_name, email, car_make, car_model, car_year, car_price))
        conn.commit()
        self.load_data()  # Värskenda andmeid pärast lisamist

        # Sulgeme lisamise akna
        self.add_window.destroy()


        audi_percent = self.calculate_audi_percent()
        self.audi_label.config(text=f"Audisi on kokku {audi_percent:.2f}%.")

    # delete
    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Hoiatus", "Palun valige rida, mida kustutada.")
            return
        confirmed = messagebox.askyesno("Kinnitage kustutamine", "Kas olete kindel, et soovite valitud rea kustutada?")
        if confirmed:
            id = self.tree.item(selected_item)['text']
            c.execute("DELETE FROM tkandmaa WHERE id=?", (id,))
            conn.commit()
            self.load_data()  # refersh

            audi_percent = self.calculate_audi_percent()
            self.audi_label.config(text=f"Audisi on kokku {audi_percent:.2f}%.")

    # search asi
    def search_data(self, event=None):
        search_term = self.search_entry.get()
        if search_term:
            c.execute("SELECT * FROM tkandmaa WHERE first_name LIKE ?", (f'%{search_term}%',))
            rows = c.fetchall()
            for record in self.tree.get_children():
                self.tree.delete(record)
            for row in rows:
                self.tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        else:
            self.load_data()

    # audi protsent
    def calculate_audi_percent(self):
        c.execute("SELECT COUNT(*) FROM tkandmaa WHERE car_make=?", ('Audi',))
        audi_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM tkandmaa")
        total_count = c.fetchone()[0]
        if total_count != 0:
            audi_percent = (audi_count / total_count) * 100
        else:
            audi_percent = 0
        return audi_percent


root = tk.Tk()
root.title("Autode asi")

app = AutoRakendus(root)

root.mainloop()

conn.close()
