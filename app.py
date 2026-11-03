import tkinter as tk
import sqlite3
from tkinter import StringVar, ttk
from tkinter import messagebox
import os
from datetime import datetime

class DBConnector():
    def __init__(self): 
        
        if not os.path.exists('baza.db'):
            messagebox.showerror(message="Brak poprawnie podłaczonej bazy")

        self.con = sqlite3.connect('baza.db')
        self.cur = self.con.cursor()

    def insert_book(self, title, author, publisher, category, publish, owner):
        
        if title != '' and author != '' and publisher != '' and category != '' and publish != '' and owner != '':
            self.cur.execute(f"INSERT INTO BOOKS(title, author, publisher, category, publish_date, owner) values ('{title}', '{author}', '{publisher}', '{category}', '{publish}', '{owner}');")
            messagebox.showinfo(message=f"Poprawnie dodano {title}")
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
        self.cur.execute(f"UPDATE BOOKS SET title='{title}', author='{author}', publisher='{publisher}', category='{category}', publish_date='{publish_date}', owner='{owner}' WHERE id={id};")
        self.con.commit()

    def get_edit_entry(self, id):
        res = self.cur.execute(f"SELECT title, author, publisher, category, publish_date, users.name FROM Books JOIN Users ON Books.owner = Users.id WHERE Books.id={id};")

        output = res.fetchall()
        return output[0]

    def delete_book(self, id, name):
        res = self.cur.execute(f"DELETE FROM Books WHERE Books.id={id};")
        messagebox.showinfo(message=f"Pomyślnie usunięto książkę {name}")
        self.con.commit()

    def get_latest_books(self):
        res = self.cur.execute("SELECT title, creation_date FROM books ORDER BY creation_date DESC LIMIT 5;")

        output = res.fetchall()
        return output

    def get_users_book(self):
        res = self.cur.execute("SELECT users.name, COUNT(*) FROM Books JOIN Users ON Books.owner = Users.id GROUP BY Users.id ORDER BY COUNT(*) DESC;")

        output = res.fetchall()
        return output

    def get_books_per_category(self):
        res = self.cur.execute("SELECT category, COUNT(*) FROM Books GROUP BY category ORDER BY COUNT(*) DESC;")

        output = res.fetchall()
        return output

    def get_popular_authors(self):
        res = self.cur.execute(f"SELECT author, COUNT(*) FROM Books GROUP BY author ORDER BY COUNT(*) DESC LIMIT 5;")

        output = res.fetchall()
        return output

class AddFrame(tk.Frame):
    def __init__(self, db, report_frame, show_frame):
        super().__init__(bg="#202734")

        self.db = db
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.report_frame = report_frame
        self.show_frame = show_frame

        (num_list, name_list) = db.get_users()

        self.name_dict = {}
        for i in range(len(name_list)):
            self.name_dict[name_list[i]] = num_list[i]

        # # 1st Section - insert / Sekcja pierwsza - dodawanie
        self.title = tk.Label(master=self, text="Formularz do wstawiania", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        self.title_add = tk.Label(master=self, text="Tytuł", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.title_add.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.title_add_input = tk.Entry(master=self, font=("Arial", 15, "bold"))
        self.title_add_input.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        self.author_add = tk.Label(master=self, text="Autor", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.author_add.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.author_add_input = tk.Entry(master=self, font=("Arial", 15, "bold"))
        self.author_add_input.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        self.publisher_add = tk.Label(master=self, text="Wydawca", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.publisher_add.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.publisher_add_input = tk.Entry(master=self, font=("Arial", 15, "bold"))
        self.publisher_add_input.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        self.category_add = tk.Label(master=self, text="Kategoria", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.category_add.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.category_add_input = tk.Entry(master=self, font=("Arial", 15, "bold"))
        self.category_add_input.grid(row=4, column=1, padx=20, pady=10, sticky="ew")
        
        self.publish_date_add = tk.Label(master=self, text="Data publikacji", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.publish_date_add.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.publish_date_add_input = tk.Entry(master=self, font=("Arial", 15, "bold"))
        self.publish_date_add_input.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        self.owner_add = tk.Label(master=self, text="Właściciel (domowy)", width=20, bg="#36415A", fg="#EEEEEE", font=("Arial", 15, "bold"))
        self.owner_add.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        self.value_owner = StringVar(master=self)
        self.value_owner.set(name_list[0])
        self.owner_add_input = tk.OptionMenu(self, self.value_owner, *name_list)
        self.owner_add_input.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.button_add = tk.Button(master=self, text="Dodaj książke", command=self.insert_book ,bg="#B7D894", fg="#202734")
        self.button_add.grid(row=7, column=1, columnspan=2)

    def insert_book(self):
        title = self.title_add_input.get()
        author = self.author_add_input.get()
        publisher = self.publisher_add_input.get()
        category = self.category_add_input.get()
        publish = self.publish_date_add_input.get()
        owner = self.value_owner.get()

        if not title.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not author.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not publisher.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not category.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not publish.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not owner.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return

        try:
            datetime.strptime(publish, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(message="Format daty to YYYY-MM-DD", parent=self)
            return

        self.db.insert_book(title, author, publisher, category, publish, self.name_dict[owner])
        self.show_frame.refresh()
        self.report_frame.refresh_report_data()

class EditFrame(tk.Toplevel):
    def __init__(self, db, id, refresh_fn):
        super().__init__(bg="#202734")

        self.id = id
        self.db = db
        self.refresh_fn = refresh_fn
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        (num_list, name_list) = db.get_users()

        self.name_dict = {}
        for i in range(len(name_list)):
            self.name_dict[name_list[i]] = num_list[i]

        # 1st Section - insert / Sekcja pierwsza - dodawanie
        self.edit_frame_title = tk.Label(master=self, text="Formularz do edycji", width=20, bg="#36415A", fg="#EEEEEE")
        self.edit_frame_title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.title_edit = tk.Label(master=self, text="Tytuł", width=20, bg="#36415A", fg="#EEEEEE")
        self.title_edit.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.title_edit_input = tk.Entry(master=self)
        self.title_edit_input.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        self.author_edit = tk.Label(master=self, text="Autor", width=20, bg="#36415A", fg="#EEEEEE")
        self.author_edit.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.author_edit_input = tk.Entry(master=self)
        self.author_edit_input.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.publisher_edit = tk.Label(master=self, text="Wydawca", width=20, bg="#36415A", fg="#EEEEEE")
        self.publisher_edit.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.publisher_edit_input = tk.Entry(master=self)
        self.publisher_edit_input.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        self.category_edit = tk.Label(master=self, text="Kategoria", width=20, bg="#36415A", fg="#EEEEEE")
        self.category_edit.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.category_edit_input = tk.Entry(master=self)
        self.category_edit_input.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
        self.publish_date_edit = tk.Label(master=self, text="Data publikacji", width=20, bg="#36415A", fg="#EEEEEE")
        self.publish_date_edit.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.publish_date_edit_input = tk.Entry(master=self)
        self.publish_date_edit_input.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.owner_edit = tk.Label(master=self, text="Właściciel (domowy)", width=20, bg="#36415A", fg="#EEEEEE")
        self.owner_edit.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.value_owner = StringVar(master=self)
        self.value_owner.set(name_list[0])
        self.owner_add_input = tk.OptionMenu(self, self.value_owner, *name_list)
        self.owner_add_input.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        self.submit_button = tk.Button(master=self, text="Zatwierdź", command=self.update_entry, bg="#B7D894")
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

        if not title.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not author.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not publisher.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not category.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not publish.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return
        if not owner.strip():
            messagebox.showerror(message="Pola nie mogą być puste", parent=self)
            return

        try:
            datetime.strptime(publish, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(message="Format daty to YYYY-MM-DD", parent=self)
            return

        self.db.update_book(self.id, title, author, publisher, category, publish, self.name_dict[owner])
        messagebox.showinfo(message="Poprawnie zaaktualizowano książkę", parent=self)
        self.refresh_fn()

class ShowFrame(tk.Frame):
    def __init__(self, db, rep_frame):
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

        self.config(bg="#202734")
        self.db = db
        self.rep_frame = rep_frame

        self.canvas = tk.Canvas(master=self, bg="#202734")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbarx = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollbarx.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scrollbarx.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.inner_frame = tk.Frame(master=self.canvas, bg="#202734")
        self.canvas_window = self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.title_label = tk.Label(master=self.inner_frame, text="Tytul", width=20, bg="#202734", fg="#EEEEEE", font=("Arial", 12, "bold"))
        self.title_label.grid(row=0, column=0,  pady=10)

        self.title_button_up = tk.Button(master=self.inner_frame, text="▲", command=lambda: self.update_dict("title", "DESC"))
        self.title_button_up.grid(row=0, column=1,  pady=10)
        self.title_button_down = tk.Button(master=self.inner_frame, text="▼", command=lambda: self.update_dict("title", "ASC"))
        self.title_button_down.grid(row=0, column=2,  pady=10)

        self.author_label = tk.Label(master=self.inner_frame, text="Autor", width=20, bg="#202734", fg="#EEEEEE", font=("Arial", 12, "bold"))
        self.author_label.grid(row=0, column=3,  pady=10)
        
        self.author_button_up = tk.Button(master=self.inner_frame, text="▲", command=lambda: self.update_dict("author", "DESC"))
        self.author_button_up.grid(row=0, column=4,  pady=10)
        self.author_button_down = tk.Button(master=self.inner_frame, text="▼", command=lambda: self.update_dict("author", "ASC"))
        self.author_button_down.grid(row=0, column=5,  pady=10)

        self.publisher_label = tk.Label(master=self.inner_frame, text="Wydawca", width=20, bg="#202734", fg="#EEEEEE", font=("Arial", 12, "bold"))
        self.publisher_label.grid(row=0, column=6,  pady=10)

        self.publisher_button_up = tk.Button(master=self.inner_frame, text="▲", command=lambda: self.update_dict("publisher", "DESC"))
        self.publisher_button_up.grid(row=0, column=7,  pady=10)
        self.publisher_button_down = tk.Button(master=self.inner_frame, text="▼", command=lambda: self.update_dict("publisher", "ASC"))
        self.publisher_button_down.grid(row=0, column=8,  pady=10)

        self.category_label = tk.Label(master=self.inner_frame, text="Kategoria", width=20, bg="#202734", fg="#EEEEEE", font=("Arial", 12, "bold"))
        self.category_label.grid(row=0, column=9,  pady=10)
        
        self.category_button_up = tk.Button(master=self.inner_frame, text="▲", command=lambda: self.update_dict("category", "DESC"))
        self.category_button_up.grid(row=0, column=10,  pady=10)
        self.category_button_down = tk.Button(master=self.inner_frame, text="▼", command=lambda: self.update_dict("category", "ASC"))
        self.category_button_down.grid(row=0, column=11,  pady=10)

        self.publish_date_label = tk.Label(master=self.inner_frame, text="Data Publikacji", width=20, bg="#202734", fg="#EEEEEE", font=("Arial", 12, "bold"))
        self.publish_date_label.grid(row=0, column=12,  pady=10)

        self.publish_button_up = tk.Button(master=self.inner_frame, text="▲", command=lambda: self.update_dict("publish_date", "DESC"))
        self.publish_button_up.grid(row=0, column=13,  pady=10)
        self.publish_button_down = tk.Button(master=self.inner_frame, text="▼", command=lambda: self.update_dict("publish_date", "ASC"))
        self.publish_button_down.grid(row=0, column=14,  pady=10)

        self.owner_label = tk.Label(master=self.inner_frame, text="Wlasciciel", width=20, bg="#202734", fg="#EEEEEE", font=("Arial", 12, "bold"))
        self.owner_label.grid(row=0, column=15,  pady=10)

        self.owner_button_up = tk.Button(master=self.inner_frame, text="▲", command=lambda: self.update_dict("users.name", "DESC"))
        self.owner_button_up.grid(row=0, column=16,  pady=10)
        self.owner_button_down = tk.Button(master=self.inner_frame, text="▼", command=lambda: self.update_dict("users.name", "ASC"))
        self.owner_button_down.grid(row=0, column=17,  pady=10)

        self.search_bar = tk.Entry(master=self.inner_frame)
        self.search_bar.grid(row=0, column=18, pady=10)
        self.search_button = tk.Button(master=self.inner_frame, command=self.refresh, text="✔")
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
        self.elements_list.clear()
        
        for elem in book_list:
            field_title = tk.Label(self.inner_frame, text=elem[1], bg="#36415A", font=("Arial", 10, "bold"), fg="White")
            field_title.grid(row=index, column=0,  pady=10, columnspan=3, sticky="ew")
            field_author = tk.Label(self.inner_frame, text=elem[2], bg="#36415A", font=("Arial", 10, "bold"), fg="White")
            field_author.grid(row=index, column=3,  pady=10, columnspan=3, sticky="ew")
            field_publisher = tk.Label(self.inner_frame, text=elem[3], bg="#36415A", font=("Arial", 10, "bold"), fg="White")
            field_publisher.grid(row=index, column=6,  pady=10, columnspan=3, sticky="ew")
            field_category = tk.Label(self.inner_frame, text=elem[4], bg="#36415A", font=("Arial", 10, "bold"), fg="White")
            field_category.grid(row=index, column=9,  pady=10, columnspan=3, sticky="ew")
            field_publish = tk.Label(master=self.inner_frame, text=elem[5], bg="#36415A", font=("Arial", 10, "bold"), fg="White")
            field_publish.grid(row=index, column=12,  pady=10, columnspan=3, sticky="ew")
            field_owner = tk.Label(self.inner_frame, text=elem[7], bg="#36415A", font=("Arial", 10, "bold"), fg="White")
            field_owner.grid(row=index, column=15,  pady=10, columnspan=3, sticky="ew")
            edit_button = tk.Button(self.inner_frame, text="Edytuj", command=lambda book_id=elem[0]: self.create_edit_tab(book_id), bg="#E0F8C7")
            edit_button.grid(row=index, column=18,  pady=10)
            delete_button = tk.Button(self.inner_frame, text="Usuń", command=lambda book_id=elem[0], title=elem[1]: self.delete_book_refresh(book_id, title), bg="#B62C2C")
            delete_button.grid(row=index, column=19,  pady=10)
            self.elements_list.append((field_title, field_author, field_publisher, field_category, field_publish, field_owner, edit_button, delete_button))
            index += 1

        self.rep_frame.refresh_report_data()

    def update_dict(self, ind, val):
        for k in self.sort_dict.keys():
            self.sort_dict[k] = "0"
        self.sort_dict[ind] = val
        self.refresh()

    def create_edit_tab(self, id):
        self.current_edit_tab = EditFrame(self.db, id, self.refresh)

    def delete_book_refresh(self, id, name):
        self.db.delete_book(id, name)
        self.refresh()

class ReportFrame(tk.Frame):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.report_items = []

        self.main_containter = tk.Frame(self)
        self.main_containter.pack(expand=True, fill="both")

        self.latest_books = tk.Frame(self.main_containter, bg="#202734", highlightthickness=1)
        self.latest_books.grid(row=0, column=0, sticky="nsew")
        self.latest_books_label = tk.Label(self.latest_books, text="Najnowsze książki", bg="#36415A", font=("Arial", 12, "bold"), fg="White")
        self.latest_books_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.books_per_person = tk.Frame(self.main_containter, bg="#202734", highlightthickness=1)
        self.books_per_person.grid(row=0, column=1, sticky="nsew")
        self.books_per_person_label = tk.Label(self.books_per_person, text="Ilość książek każdej osoby", bg="#36415A", font=("Arial", 12, "bold"), fg="White")
        self.books_per_person_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.categories = tk.Frame(self.main_containter, bg="#202734", highlightthickness=1)
        self.categories.grid(row=1, column=0, sticky="nsew")
        self.categories_label = tk.Label(self.categories, text="Ilość książek na kategorię", bg="#36415A", font=("Arial", 12, "bold"), fg="White")
        self.categories_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.authors = tk.Frame(self.main_containter, bg="#202734", highlightthickness=1)
        self.authors.grid(row=1, column=1, sticky="nsew")
        self.authors_label = tk.Label(self.authors, text="Najpopularniejsi autorzy", bg="#36415A", font=("Arial", 12, "bold"), fg="White")
        self.authors_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_containter.grid_rowconfigure(0, weight=1)
        self.main_containter.grid_rowconfigure(1, weight=1)
        self.main_containter.grid_columnconfigure(0, weight=1)
        self.main_containter.grid_columnconfigure(1, weight=1)

        self.latest_books.grid_columnconfigure(0, weight=1)

        self.books_per_person.grid_columnconfigure(0, weight=1)
        self.books_per_person.grid_columnconfigure(1, weight=1)

        self.categories.grid_columnconfigure(0, weight=1)
        self.categories.grid_columnconfigure(1, weight=1)

        self.authors.grid_columnconfigure(0, weight=1)
        self.authors.grid_columnconfigure(1, weight=1)

        self.refresh_report_data()


    def refresh_report_data(self):
        latest_books = self.db.get_latest_books()
        people_books = self.db.get_users_book()
        category_books = self.db.get_books_per_category()
        authors = self.db.get_popular_authors()

        for e in self.report_items:
            e.destroy()
        self.report_items.clear()

        for i, elem in enumerate(latest_books):
            label = tk.Label(self.latest_books, text=elem[0], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label.grid(row=i+1, column=0, sticky="ew", padx=10, pady=10)
            label_2 = tk.Label(self.latest_books, text=elem[1], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label_2.grid(row=i+1, column=1, sticky="ew", padx=10, pady=10)
            self.report_items.append(label)
            self.report_items.append(label_2)

        for j, elem in enumerate(people_books):
            label = tk.Label(self.books_per_person, text=elem[0], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label.grid(row=j+1, column=0, sticky="ew", padx=10, pady=10)
            label_2 = tk.Label(self.books_per_person, text=elem[1], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label_2.grid(row=j+1, column=1, sticky="ew", padx=10, pady=10)
            self.report_items.append(label)
            self.report_items.append(label_2)

        for k, elem in enumerate(category_books):
            label = tk.Label(self.categories, text=elem[0], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label.grid(row=k+1, column=0, sticky="ew", padx=10, pady=10)
            label_2 = tk.Label(self.categories, text=elem[1], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label_2.grid(row=k+1, column=1, sticky="ew", padx=10, pady=10)
            self.report_items.append(label)
            self.report_items.append(label_2)

        for l, elem in enumerate(authors):
            label = tk.Label(self.authors, text=elem[0], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label.grid(row=l+1, column=0, sticky="ew", padx=10, pady=10)
            label_2 = tk.Label(self.authors, text=elem[1], bg="#36415A", font=("Arial", 12, "bold"), fg="White")
            label_2.grid(row=l+1, column=1, sticky="ew", padx=10, pady=10)
            self.report_items.append(label)
            self.report_items.append(label_2)

            

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
        
        self.report_frame = ReportFrame(self.db)
        self.show_frame = ShowFrame(self.db, self.report_frame)
        self.add_frame = AddFrame(self.db, self.report_frame, self.show_frame)

        self.add_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.show_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.report_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.notebook.add(self.add_frame, text="Formularz do wstawiania")
        self.notebook.add(self.show_frame, text="Formularz przegladania")
        self.notebook.add(self.report_frame, text="Formularz do raportowania")

app_runner = App()
app_runner.mainloop()
