import tkinter as tk
import sqlite3
from tkinter import StringVar, ttk
from tkinter import messagebox
import os

class DBConnector():
    def __init__(self): 
        
        if not os.path.exists('baza.db'):
            messagebox.showerror(message="Brak poprawnie podłaczonej bazy")

        self.con = sqlite3.connect('baza.db')
        self.cur = self.con.cursor()

    def insert_book(self, title, author, publisher, category, publish, owner):
        
        print((title, author, publisher, category, publish, owner))
        if title != '' and author != '' and publisher != '' and category != '' and publish != '' and owner != '':
            self.cur.execute(f"INSERT INTO BOOKS(title, author, publisher, category, publish_date, owner) values ('{title}', '{author}', '{publisher}', '{category}', '{publish}', '{owner}');")
            self.con.commit()
        else:
            messagebox.showerror(message="Nie wprowadzono poprawnych danych")

    def get_users(self):
        res = self.cur.execute("SELECT id, name FROM users")
        output = res.fetchall()

        num_list = []
        name_list = []        
        for elem in output:
            num_list.append(elem[0])
            name_list.append(elem[1])

        return num_list, name_list
    


class AddFrame(tk.Frame):
    def __init__(self, db):
        super().__init__(bg="#555555")

        self.db = db

        (num_list, name_list) = db.get_users()

        self.name_dict = {}
        for i in range(len(name_list)):
            self.name_dict[name_list[i]] = num_list[i] 

        # # 1st Section - insert / Sekcja pierwsza - dodawanie
        self.title = tk.Label(master=self, text="Formularz do wstawiania", width=20, bg="#555555", fg="#EEEEEE")
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.title_add = tk.Label(master=self, text="Tytuł", width=20, bg="#555555", fg="#EEEEEE")
        self.title_add.grid(row=1, column=0, padx=10, pady=10)
        self.title_add_input = tk.Entry(master=self)
        self.title_add_input.grid(row=1, column=1, padx=10, pady=10)
        
        self.author_add = tk.Label(master=self, text="Autor", width=20, bg="#555555", fg="#EEEEEE")
        self.author_add.grid(row=2, column=0, padx=10, pady=10)
        self.author_add_input = tk.Entry(master=self)
        self.author_add_input.grid(row=2, column=1, padx=10, pady=10)
        
        self.publisher_add = tk.Label(master=self, text="Wydawca", width=20, bg="#555555", fg="#EEEEEE")
        self.publisher_add.grid(row=3, column=0, padx=10, pady=10)
        self.publisher_add_input = tk.Entry(master=self)
        self.publisher_add_input.grid(row=3, column=1, padx=10, pady=10)
        
        self.category_add = tk.Label(master=self, text="Kategoria", width=20, bg="#555555", fg="#EEEEEE")
        self.category_add.grid(row=4, column=0, padx=10, pady=10)
        self.category_add_input = tk.Entry(master=self)
        self.category_add_input.grid(row=4, column=1, padx=10, pady=10)
        
        self.publish_date_add = tk.Label(master=self, text="Data publikacji", width=20, bg="#555555", fg="#EEEEEE")
        self.publish_date_add.grid(row=5, column=0, padx=10, pady=10)
        self.publish_date_add_input = tk.Entry(master=self)
        self.publish_date_add_input.grid(row=5, column=1, padx=10, pady=10)

        self.owner_add = tk.Label(master=self, text="Właściciel (domowy)", width=20, bg="#555555", fg="#EEEEEE")
        self.owner_add.grid(row=6, column=0, padx=10, pady=10)
        self.value_owner = StringVar(master=self)
        self.value_owner.set(name_list[0])
        self.owner_add_input = tk.OptionMenu(self, self.value_owner, *name_list)
        self.owner_add_input.grid(row=6, column=1, padx=10, pady=10)

        self.button_add = tk.Button(master=self, text="Dodaj książke", command=self.insert_book ,bg="#444444", fg="White")
        self.button_add.grid(row=7, column=0)

    def insert_book(self):
        title = self.title_add_input.get()
        author = self.author_add_input.get()
        publisher = self.publisher_add_input.get()
        category = self.category_add_input.get()
        publish = self.publish_date_add_input.get()
        owner = self.value_owner.get()

        self.db.insert_book(title, author, publisher, category, publish, self.name_dict[owner])

class EditFrame(tk.Frame):
    def __init__(self, db):
        super().__init__(bg="#555555")

        # 1st Section - insert / Sekcja pierwsza - dodawanie
        self.edit_frame_title = tk.Label(master=self, text="Formularz do edycji", width=20, bg="#555555", fg="#EEEEEE")
        self.edit_frame_title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.title_edit = tk.Label(master=self, text="Tytuł", width=20, bg="#555555", fg="#EEEEEE")
        self.title_edit.grid(row=1, column=0, padx=10, pady=10)
        self.title_edit_input = tk.Entry(master=self)
        self.title_edit_input.grid(row=1, column=1, padx=10, pady=10)
        
        self.author_edit = tk.Label(master=self, text="Autor", width=20, bg="#555555", fg="#EEEEEE")
        self.author_edit.grid(row=2, column=0, padx=10, pady=10)
        self.author_edit_input = tk.Entry(master=self)
        self.author_edit_input.grid(row=2, column=1, padx=10, pady=10)
        
        self.publisher_edit = tk.Label(master=self, text="Wydawca", width=20, bg="#555555", fg="#EEEEEE")
        self.publisher_edit.grid(row=3, column=0, padx=10, pady=10)
        self.publisher_edit_input = tk.Entry(master=self)
        self.publisher_edit_input.grid(row=3, column=1, padx=10, pady=10)
        
        self.category_edit = tk.Label(master=self, text="Kategoria", width=20, bg="#555555", fg="#EEEEEE")
        self.category_edit.grid(row=4, column=0, padx=10, pady=10)
        self.category_edit_input = tk.Entry(master=self)
        self.category_edit_input.grid(row=4, column=1, padx=10, pady=10)
        
        self.publish_date_edit = tk.Label(master=self, text="Data publikacji", width=20, bg="#555555", fg="#EEEEEE")
        self.publish_date_edit.grid(row=5, column=0, padx=10, pady=10)
        self.publish_date_edit_input = tk.Entry(master=self)
        self.publish_date_edit_input.grid(row=5, column=1, padx=10, pady=10)

        self.owner_edit = tk.Label(master=self, text="Właściciel (domowy)", width=20, bg="#555555", fg="#EEEEEE")
        self.owner_edit.grid(row=6, column=0, padx=10, pady=10)
        self.owner_edit_input = tk.Entry(master=self)
        self.owner_edit_input.grid(row=6, column=1, padx=10, pady=10)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = DBConnector()

        # Stale / Consts
        self.WINDOW_SIZE_X = 1920
        self.WINDOW_SIZE_Y = 1080

        self.geometry(f"{self.WINDOW_SIZE_X}x{self.WINDOW_SIZE_Y}")

        self.notebook = ttk.Notebook(master=self)
        self.notebook.pack(expand=True, fill="both")
        
        self.add_frame = AddFrame(self.db)
        self.add_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.edit_frame = EditFrame(self.db)
        self.edit_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.notebook.add(self.add_frame, text="Formularz do wstawiania")
        self.notebook.add(self.edit_frame, text="Formularz do edycji")

app_runner = App()
app_runner.mainloop()
