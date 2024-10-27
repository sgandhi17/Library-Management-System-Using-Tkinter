import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database functions
def setup_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            year_published INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, genre, year_published):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, genre, year_published)
        VALUES (?, ?, ?, ?)
    ''', (title, author, genre, year_published))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book added successfully!")

def get_all_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, title, author, genre, year_published):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books
        SET title = ?, author = ?, genre = ?, year_published = ?
        WHERE id = ?
    ''', (title, author, genre, year_published, book_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book updated successfully!")

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book deleted successfully!")

# GUI functions
def refresh_book_list():
    books = get_all_books()
    book_list.delete(0, tk.END)
    for book in books:
        book_list.insert(tk.END, book)

def add_book_gui():
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    year = entry_year.get()

    if title and author and genre and year.isdigit():
        add_book(title, author, genre, int(year))
        refresh_book_list()
    else:
        messagebox.showwarning("Input Error", "Please enter valid book information.")

def update_book_gui():
    selected = book_list.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a book to update.")
        return

    book_id = book_list.get(selected[0])[0]
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    year = entry_year.get()

    if title and author and genre and year.isdigit():
        update_book(book_id, title, author, genre, int(year))
        refresh_book_list()
    else:
        messagebox.showwarning("Input Error", "Please enter valid book information.")

def delete_book_gui():
    selected = book_list.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a book to delete.")
        return

    book_id = book_list.get(selected[0])[0]
    delete_book(book_id)
    refresh_book_list()

def load_selected_book(event):
    selected = book_list.curselection()
    if not selected:
        return

    book = book_list.get(selected[0])
    entry_title.delete(0, tk.END)
    entry_title.insert(0, book[1])
    entry_author.delete(0, tk.END)
    entry_author.insert(0, book[2])
    entry_genre.delete(0, tk.END)
    entry_genre.insert(0, book[3])
    entry_year.delete(0, tk.END)
    entry_year.insert(0, book[4])

# Setup database and create GUI window
setup_database()

app = tk.Tk()
app.title("Library Management System")

# Center Frame for Inputs and Buttons
center_frame = tk.Frame(app, bd=2, relief="solid",padx=20,pady=20)
center_frame.grid(row=0, column=0, padx=100, pady=100)

# Input fields
tk.Label(center_frame, text="Title of The Book: ",font=("Arial",17)).grid(row=0, column=0)
entry_title = tk.Entry(center_frame, justify="center",width=30)
entry_title.grid(row=0, column=1,padx=(5, 10), pady=(10,10))

tk.Label(center_frame, text="Author Name: ",font=("Arial",17)).grid(row=1, column=0)
entry_author = tk.Entry(center_frame, justify="center",width=30)
entry_author.grid(row=1, column=1,padx=(5, 10), pady=(10, 10))

tk.Label(center_frame, text="Category: ",font=("Arial",17)).grid(row=2, column=0)
entry_genre = tk.Entry(center_frame,  justify="center",width=30)
entry_genre.grid(row=2, column=1,padx=(5, 10), pady=(10, 10))

tk.Label(center_frame, text="Published Year: ",font=("Arial",17)).grid(row=3, column=0)
entry_year = tk.Entry(center_frame,  justify="center",width=30)
entry_year.grid(row=3, column=1,padx=(5, 10), pady=(10, 10))

# Buttons

tk.Button(center_frame, text="Add Book", command=add_book_gui, bg="green", font=("Arial", 15)).grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=(15, 10))
tk.Button(center_frame, text="Update Book", command=update_book_gui, bg="#7CFC00", font=("Arial", 15)).grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 10))
tk.Button(center_frame, text="Delete Book", command=delete_book_gui, bg="red", font=("Arial", 15)).grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 15))

# # Book list
book_list = tk.Listbox(app, width=45,font=("Arial",15))
book_list.grid(row=0, column=2, rowspan=7, padx=10)
book_list.bind('<<ListboxSelect>>', load_selected_book)

# # Initial load of books
refresh_book_list()

# Center the main frame in the window
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

app.mainloop()
