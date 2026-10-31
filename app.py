import tkinter as tk
import sqlite3
from tkinter import StringVar, ttk
from tkinter import messagebox
import os
from unicodedata import category

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
    
    def get_book_list(self, search_string, sort_by):
        sort_clause = ""
        for k in sort_by.keys():
            v = sort_by[k]
            if v == "ASC" or v =="DESC":
                sort_clause += f"ORDER BY {k} {v};"
        res = self.cur.execute(f"SELECT books.id, title, author, publisher, category, publish_date, creation_date, users.name FROM books JOIN users ON books.owner = users.id WHERE title LIKE '%{search_string}%' OR author LIKE '%{search_string}%' OR publisher LIKE '%{search_string}%' OR category LIKE '%{search_string}%' OR publish_date LIKE '%{search_string}%' OR users.name LIKE '%{search_string}%' {sort_clause}")
        output = res.fetchall()
        
        return output
    
    def update_book(self, id, title, author, publisher, category, publish_date, owner):
        print((id, title, author, publisher, category, publish_date, owner))
        self.cur.execute(f"UPDATE BOOKS SET title='{title}', author='{author}', publisher='{publisher}', category='{category}', publish_date='{publish_date}', owner='{owner}' WHERE id={id};")
        # self.con.commit()

    def get_edit_entry(self, id):
        res = self.cur.execute(f"SELECT title, author, publisher, category, publish_date, users.name FROM Books JOIN Users ON Books.owner = Users.id WHERE Books.id={id};")

        output = res.fetchall()
        return output[0]

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

class EditFrame(tk.Toplevel):
    def __init__(self, db, id, refresh_fn):
        super().__init__(bg="#555555")

        self.id = id
        self.db = db
        self.refresh_fn = refresh_fn
        (num_list, name_list) = db.get_users()

        self.name_dict = {}
        for i in range(len(name_list)):
            self.name_dict[name_list[i]] = num_list[i]

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
        self.value_owner = StringVar(master=self)
        self.value_owner.set(name_list[0])
        self.owner_add_input = tk.OptionMenu(self, self.value_owner, *name_list)
        self.owner_add_input.grid(row=6, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(master=self, text="Zatwierdź", command=self.update_entry)
        self.submit_button.grid(row=7, column=0, padx=10, pady=10, columnspan=2)
        
        entry = self.db.get_edit_entry(self.id)
        self.title_edit_input.insert(0,entry[0])
        self.author_edit_input.insert(0, entry[1])
        self.publisher_edit_input.insert(0, entry[2])
        self.category_edit_input.insert(0, entry[3])
        self.publish_date_edit_input.insert(0, entry[4])
        self.value_owner.set(entry[5])
    
    def update_entry(self):
        title = self.title_edit_input.get()
        author = self.author_edit_input.get()
        publisher = self.publisher_edit_input.get()
        category = self.category_edit_input.get()
        publish = self.publish_date_edit_input.get()
        owner = self.value_owner.get()

        self.db.update_book(self.id, title, author, publisher, category, publish, self.name_dict[owner])
        self.refresh_fn()

class ShowFrame(tk.Frame):
    def __init__(self, db):
        super().__init__()

        self.sort_dict = {
            "books.id": "0",
            "title": "0",
            "author": "0",
            "publisher": "0",
            "category": "0",
            "publish_date": "0", 
            "creation_date": "0",
            "users.name": "0"
        }

        self.config(bg="#555555")
        self.db = db

        self.title_label = tk.Label(master=self, text="Tytul", width=20, bg="#555555", fg="#EEEEEE")
        self.title_label.grid(row=0, column=0,  pady=10)

        self.title_button_up = tk.Button(master=self, text="Up", command=lambda: self.update_dict("title", "DESC"))
        self.title_button_up.grid(row=0, column=1,  pady=10)
        self.title_button_down = tk.Button(master=self, text="Down", command=lambda: self.update_dict("title", "ASC"))
        self.title_button_down.grid(row=0, column=2,  pady=10)

        self.author_label = tk.Label(master=self, text="Autor", width=20, bg="#555555", fg="#EEEEEE")
        self.author_label.grid(row=0, column=3,  pady=10)
        
        self.author_button_up = tk.Button(master=self, text="Up", command=lambda: self.update_dict("author", "DESC"))
        self.author_button_up.grid(row=0, column=4,  pady=10)
        self.author_button_down = tk.Button(master=self, text="Down", command=lambda: self.update_dict("author", "ASC"))
        self.author_button_down.grid(row=0, column=5,  pady=10)

        self.publisher_label = tk.Label(master=self, text="Wydawca", width=20, bg="#555555", fg="#EEEEEE")
        self.publisher_label.grid(row=0, column=6,  pady=10)

        self.publisher_button_up = tk.Button(master=self, text="Up", command=lambda: self.update_dict("publisher", "DESC"))
        self.publisher_button_up.grid(row=0, column=7,  pady=10)
        self.publisher_button_down = tk.Button(master=self, text="Down", command=lambda: self.update_dict("publisher", "ASC"))
        self.publisher_button_down.grid(row=0, column=8,  pady=10)

        self.category_label = tk.Label(master=self, text="Kategoria", width=20, bg="#555555", fg="#EEEEEE")
        self.category_label.grid(row=0, column=9,  pady=10)
        
        self.category_button_up = tk.Button(master=self, text="Up", command=lambda: self.update_dict("category", "DESC"))
        self.category_button_up.grid(row=0, column=10,  pady=10)
        self.category_button_down = tk.Button(master=self, text="Down", command=lambda: self.update_dict("category", "ASC"))
        self.category_button_down.grid(row=0, column=11,  pady=10)

        self.publish_date_label = tk.Label(master=self, text="Data Publikacji", width=20, bg="#555555", fg="#EEEEEE")
        self.publish_date_label.grid(row=0, column=12,  pady=10)

        self.publish_button_up = tk.Button(master=self, text="Up", command=lambda: self.update_dict("publish_date", "DESC"))
        self.publish_button_up.grid(row=0, column=13,  pady=10)
        self.publish_button_down = tk.Button(master=self, text="Down", command=lambda: self.update_dict("publish_date", "ASC"))
        self.publish_button_down.grid(row=0, column=14,  pady=10)

        self.owner_label = tk.Label(master=self, text="Wlasciciel", width=20, bg="#555555", fg="#EEEEEE")
        self.owner_label.grid(row=0, column=15,  pady=10)

        self.owner_button_up = tk.Button(master=self, text="Up", command=lambda: self.update_dict("owner", "DESC"))
        self.owner_button_up.grid(row=0, column=16,  pady=10)
        self.owner_button_down = tk.Button(master=self, text="Down", command=lambda: self.update_dict("owner", "ASC"))
        self.owner_button_down.grid(row=0, column=17,  pady=10)

        self.search_bar = tk.Entry(self)
        self.search_bar.grid(row=0, column=18, padx=10, pady=10)
        self.search_button = tk.Button(self, command=self.refresh)
        self.search_button.grid(row=0, column=19)

        self.elements_list = []
        self.refresh()

    def refresh(self):
        index=1
        search_string = self.search_bar.get()
        book_list = self.db.get_book_list(search_string, self.sort_dict)

        for item_row in self.elements_list:
            for e in item_row:
                e.after(1, e.destroy)
        
        for elem in book_list:
            field_title = tk.Label(self, text=elem[1])
            field_title.grid(row=index, column=0,  pady=10, columnspan=3)
            field_author = tk.Label(self, text=elem[2])
            field_author.grid(row=index, column=3,  pady=10, columnspan=3)
            field_publisher = tk.Label(self, text=elem[3])
            field_publisher.grid(row=index, column=6,  pady=10, columnspan=3)
            field_category = tk.Label(self, text=elem[4])
            field_category.grid(row=index, column=9,  pady=10, columnspan=3)
            field_publish = tk.Label(master=self, text=elem[5])
            field_publish.grid(row=index, column=12,  pady=10, columnspan=3)
            field_owner = tk.Label(self, text=elem[7])
            field_owner.grid(row=index, column=15,  pady=10, columnspan=3)
            edit_button = tk.Button(self, text="Edit", command=lambda book_id=elem[0]: self.create_edit_tab(book_id))
            edit_button.grid(row=index, column=17,  pady=10)
            self.elements_list.append((field_title, field_author, field_publisher, field_category, field_publish, field_owner, edit_button))
            index += 1

    def update_dict(self, ind, val):
        for k in self.sort_dict.keys():
            self.sort_dict[k] = "0"
        self.sort_dict[ind] = val
        self.refresh()

    def create_edit_tab(self, id):
        self.current_edit_tab = EditFrame(self.db, id, self.refresh)

class ReportFrame(tk.Frame):
    def __init__(self, db):
        super().__init__()

        self.db = db

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

        self.show_frame = ShowFrame(self.db)
        self.show_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.report_frame = ReportFrame(self.db)
        self.report_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.notebook.add(self.add_frame, text="Formularz do wstawiania")
        self.notebook.add(self.show_frame, text="Formularz przegladania")
        self.notebook.add(self.report_frame, text="Formularz do raportowania")

app_runner = App()
app_runner.mainloop()
