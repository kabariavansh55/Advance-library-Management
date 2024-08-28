from tkinter import *
import pymysql as p
from tkinter import messagebox,ttk,filedialog
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
import datetime
import qrcode
from PIL import ImageTk, Image
import os
import tkinter as tk
from tkinter import font as tkfont
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import webbrowser


b1,b2,b3,b4,cur,con,e1,e2,e3,e4,e5,i,ps=None,None,None,None,None,None,None,None,None,None,None,None,None
window,win=None,None
com1d,com1m,com1y,com2d,com2m,com2y=None,None,None,None,None,None
month=['January','February','March','April','May','June','July','August','September','October','November','December']
y = list(range(2020, 2040))
d = list(range(1,32))

def loginlibr():
    global window
    connectdb()
    cur.execute('SELECT * FROM login')  # Fetch all rows to check against the user input
    for i in range(cur.rowcount):
        data = cur.fetchone()
        if e1.get().strip() == str(data[1]) and e2.get().strip() == str(data[3]):
            record_login(e1.get())  # Record login history
            closedb()
            libr()
            break
    else:
        messagebox.showerror("Error", "Wrong Password!")
        closedb()

# Function to toggle password visibility
def toggle_password():
    if e2.cget('show') == '*':
        e2.config(show='')
        eye_button.config(text='Hide')
    else:
        e2.config(show='*')
        eye_button.config(text='Show')

def loginadmin():
    if e1.get() == 'admin' and e2.get() == 'vansh2807':
        admin()
    else:
        messagebox.showerror("Error", "Wrong Password!")

def record_login(username):
    connectdb()
    q = 'INSERT INTO LoginHistory (username) VALUES (%s)'
    cur.execute(q, (username,))
    con.commit()
    closedb()
def logout():
    win.destroy()  # Close the librarian window
    window.deiconify()  # Show the login window again

def show_about_window():
    about_win = tk.Toplevel()
    about_win.title("About")
    about_win.geometry("800x700")
    about_win.resizable(True, True)

    # Define fonts
    title_font = tkfont.Font(family="Arial", size=16, weight="bold")
    header_font = tkfont.Font(family="Arial", size=12, weight="bold")
    text_font = tkfont.Font(family="Arial", size=12)

    # Create a Canvas and a Frame for the content
    canvas = tk.Canvas(about_win)
    scrollbar_y = tk.Scrollbar(about_win, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(about_win, orient="horizontal", command=canvas.xview)

    content_frame = tk.Frame(canvas)

    # Create a window in the Canvas
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    # Configure the Canvas and Scrollbars
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side='right', fill='y')
    scrollbar_x.pack(side='bottom', fill='x')
    canvas.pack(side='left', fill='both', expand=True)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", on_frame_configure)

    # Add Title
    title_label = tk.Label(content_frame, text="Advance Library Management System", font=title_font, bg="navy", fg="white", pady=10)
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    # Add a line separator
    separator = tk.Frame(content_frame, height=2, bd=1, relief="sunken")
    separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    # Define table headers
    headers = ["Field", "Detail"]
    header_labels = [
        tk.Label(content_frame, text=headers[0], font=header_font, bg="darkgray", fg="white", padx=10, pady=5, relief="ridge"),
        tk.Label(content_frame, text=headers[1], font=header_font, bg="darkgray", fg="white", padx=10, pady=5, relief="ridge")
    ]

    for i, label in enumerate(header_labels):
        label.grid(row=2, column=i, padx=10, pady=5, sticky="ew")

    # Function to change color on hover
    def on_enter(e, widget):
        widget.config(bg="lightblue")

    def on_leave(e, widget):
        widget.config(bg=widget.default_bg_color)

    # Table data
    data = [
        ("Created by:", "Vansh Kabaria"),
        ("Creation Date:", "July 2024"),
        ("Technologies Used:", "Python, Tkinter, MySQL, ReportLab"),
        ("Brief Summary:", "The Advanced Library Management System (ALMS) is a comprehensive application designed to modernize and streamline library operations. "
        "Developed using Python, Tkinter, and MySQL, ALMS offers a robust solution for managing various library activities efficiently. The system integrates "
        "essential features for book management and issuance while incorporating advanced functionalities to enhance user experience and operational efficiency. "
        "This detailed overview highlights the core features and additional functionalities of the system.\n\n"

        "1. Traditional Features\n"
        "ALMS provides a set of core functionalities that are essential for effective library management:\n\n"
        " 1.1 Book Management: Librarians have the capability to add, update, delete, and view books within the system. Each book is assigned a unique serial number and "
        "includes detailed information such as title, author, subject, and quantity. The 'View Books' section presents all available books and supports both search and sort functionalities, "
        "allowing for efficient organization and retrieval of book records.\n\n"
        " 1.2 Book Issuance and Return: The system tracks the issuance and return of books, capturing important details such as the issue date, student ID, and book information. "
        "The 'Issued Book History' section maintains a comprehensive log of all transactions, including timestamps, return dates, and fines, ensuring accurate tracking of book movements.\n\n"
        " 1.3 Login System: A secure login mechanism is implemented for both admins and librarians. This feature includes password masking and supports submission via the Enter key, "
        "enhancing the security and usability of the login process.\n\n"

        "2. Search Functionality\n"
        "The search functionality is a crucial aspect of ALMS, providing users with an efficient method for locating specific books. In the 'View Books' section, users can enter "
        "keywords related to book attributes such as title, author, or subject. The search algorithm filters the displayed records based on the query, enabling librarians and users to "
        "quickly find particular books without manually browsing through the entire inventory. This feature significantly improves the system's usability by delivering quick and accurate search results, "
        "thereby enhancing overall efficiency in managing and retrieving book information.\n\n"

        "3. Sort Functionality\n"
        "The sort functionality allows users to organize book records according to various criteria. In the 'View Books' section, users can sort books by attributes such as title, author, or subject. "
        "This is facilitated through a dropdown menu or similar interface element, allowing users to select their preferred sorting criterion. Sorting helps users arrange books in a specific order, "
        "making data analysis, inventory management, and administrative tasks more manageable. This feature is particularly valuable for librarians who need to access records in a structured and organized format.\n\n"

        "4. Scroll Functionality\n"
        "The scroll functionality is implemented to enhance the user experience when dealing with extensive datasets. Sections such as 'View Books' and 'Issued Book History' include vertical and horizontal scrollbars. "
        "These scrollbars enable users to navigate through long lists of books or transaction records seamlessly. The vertical scrollbar allows for scrolling through lengthy book lists, while the horizontal scrollbar assists in navigating wide tables with numerous columns. "
        "By incorporating scrollbars, ALMS ensures that users can access all necessary information without being overwhelmed by large volumes of data, contributing to a cleaner and more organized interface.\n\n"

        "5. Extra Features Beyond Traditional Capabilities\n"
        "In addition to the core functionalities, ALMS incorporates several advanced features to enhance its capabilities:\n\n"
        "- 5.1 QR Code Integration:** Each book is assigned a unique QR code for efficient tracking and management. This feature simplifies book identification and facilitates quick access to book information through QR code scanning.\n\n"
        "- 5.2D ynamic User Interface (UI) Elements:** The system includes interactive buttons with 3D effects and hover-resize functionality, enhancing the visual appeal and usability of the interface.\n\n"
        "- 5.3 Detailed Issued Book History:** ALMS maintains comprehensive records of issued books, including timestamps and fines, providing a detailed history of book transactions for accurate tracking and reporting.\n\n"
        "- 5.4 Modular Design and Robust Error Handling:** The system features a modular design for easy maintenance and robust error handling mechanisms to ensure system stability and reliability.\n\n"
        "- 5.5 Enhanced Data Visualization:** There is potential for integrating graphical representations of library data, offering visual insights into various aspects of library operations.\n\n"
        "- 5.6 User-Friendly Notifications and Alerts:** The system includes customizable notifications for key actions and alerts for overdue books, improving user engagement and operational oversight.\n\n"
        "- 5.7 Potential PDF Export Facility:** Future enhancements may include the capability to generate and download PDFs for easy sharing and review of library data, facilitating improved data management.\n\n"
        "- 5.8 Google Search Button:** Integration of a Google search button allows users to perform web searches directly from the system interface, enhancing accessibility to external resources.\n\n"
        "- 5.9 WhatsApp Integration:** A WhatsApp button enables direct access to WhatsApp for sending PDFs of view book details or issued book history, facilitating easy communication and document sharing.\n\n"

        "6. Summary\n"
        "The Advanced Library Management System is a comprehensive tool designed to address contemporary library needs effectively. By combining traditional features with advanced functionalities such as search, sort, and scroll, "
        "along with dynamic UI elements and detailed historical records, ALMS offers a powerful solution for managing library operations. The system's design ensures ease of use, efficiency in book management, and adaptability to future enhancements, making it a valuable asset for modern library environments."
)
    ]

    for row_index, (field, detail) in enumerate(data, start=3):
        bg_color = "lightgray" if row_index % 2 == 0 else "lightblue"  # Alternate row colors

        # Create field label
        field_label = tk.Label(content_frame, text=field, font=text_font, bg=bg_color, anchor="w", padx=10, pady=5, relief="ridge", width=20)
        field_label.default_bg_color = bg_color  # Store original color
        field_label.bind("<Enter>", lambda e, w=field_label: on_enter(e, w))
        field_label.bind("<Leave>", lambda e, w=field_label: on_leave(e, w))

        # Create detail label
        detail_label = tk.Label(content_frame, text=detail, font=text_font, bg=bg_color, anchor="w", wraplength=450, padx=10, pady=5, relief="ridge", width=50)
        detail_label.default_bg_color = bg_color  # Store original color
        detail_label.bind("<Enter>", lambda e, w=detail_label: on_enter(e, w))
        detail_label.bind("<Leave>", lambda e, w=detail_label: on_leave(e, w))

        field_label.grid(row=row_index, column=0, padx=10, pady=5, sticky="ew")
        detail_label.grid(row=row_index, column=1, padx=10, pady=5, sticky="ew")

    # Add Close button with white text
    close_button = tk.Button(content_frame, text="Close", command=about_win.destroy, bg="red", fg="white", font=text_font, padx=10, pady=5)
    close_button.grid(row=len(data) + 3, column=0, columnspan=2, pady=10)


def libr():
    global window
    window.withdraw()  # Hide the login window

    global win
    win = tk.Tk()
    win.title('Library')
    win.geometry("700x600+480+180")
    win.resizable(False, False)
    custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

    # Button styles
    button_style = {
        'font': custom_font,
        'bg': 'lightblue',
        'fg': 'black',
        'activebackground': '#f1c40f',
        'width': 20,
        'height': 2,
        'borderwidth': 1,
        'relief': 'flat'
    }

    logout_button_style = {
        'font': custom_font,
        'bg': '#e74c3c',
        'fg': 'white',
        'activebackground': '#c0392b',
        'width': 20,
        'height': 2,
        'borderwidth': 1,
        'relief': 'flat'
    }

    about_button_style = {
        'font': custom_font,
        'bg': '#2ecc71',
        'fg': 'white',
        'activebackground': '#27ae60',
        'width': 20,
        'height': 2,
        'borderwidth': 1,
        'relief': 'flat'
    }

    google_button_style = {
        'font': custom_font,
        'bg': '#4285F4',
        'fg': 'white',
        'activebackground': '#357AE8',
        'width': 20,
        'height': 2,
        'borderwidth': 1,
        'relief': 'flat'
    }

    def on_enter(event):
        event.widget.config(bg=event.widget['activebackground'], font=("Helvetica", 12, "bold"))
        event.widget.config(width=24, height=2)

    def on_leave(event):
        event.widget.config(bg=event.widget['bg'], font=("Helvetica", 12, "bold"))
        event.widget.config(width=20, height=2)

    # Create a frame for the button table
    button_frame = tk.Frame(win, bg='green', borderwidth=4, relief='solid')
    button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    # Define buttons and their commands
    buttons = [
        ('Add Book', addbook),
        ('Issue Book', issuebook),
        ('Return Book', returnbook),
        ('View Book', viewbook),
        ('Issued Book', issuedbook),
        ('Delete Book', deletebook),
        ('Update Book', updatebook),
        ('Total Books', show_total_books),
        ('Issued Books History', issued_books_history),
        ('LogOut', logout),  
        ('Search Google', open_google),  
        ('About', show_about_window) 
    ]

    # Assign styles to special buttons
    special_button_styles = {
        'LogOut': logout_button_style,
        'Search Google': google_button_style,
        'About': about_button_style
    }

    # Create buttons and place them in the button frame
    num_cols = 3
    for i, (text, command) in enumerate(buttons):
        row = i // num_cols
        col = i % num_cols
        button_style_to_use = special_button_styles.get(text, button_style)
        button = tk.Button(button_frame, text=text, command=command, **button_style_to_use)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    # Create an animated label at the top of the window
    animated_label = tk.Label(win, text="Welcome to Advance Library Management system created by Vansh Kabaria", font=("Helvetica", 16, "bold"), fg="blue", bg='lightgray')
    animated_label.place(x=10, y=10)

    def animate_label(x):
        if x > win.winfo_width():
            x = -animated_label.winfo_width()
        animated_label.place(x=x, y=10)
        win.after(50, animate_label, x + 5)

    animate_label(0)

    # Configure grid rows and columns
    win.grid_rowconfigure(1, weight=1)
    win.grid_columnconfigure(0, weight=1)

    button_frame.grid_rowconfigure(tuple(range(4)), weight=1)
    button_frame.grid_columnconfigure(tuple(range(3)), weight=1)

    win.mainloop()

def open_google():
    webbrowser.open('http://www.google.com')

def save_to_pdf(data, filename):
    # Define page size
    pagesize = A4
    c = SimpleDocTemplate(filename, pagesize=pagesize)
    
    # Define table styles and sizes
    table_data = data
    max_col_width = 1 * inch  # Define a maximum column width
    min_col_width = 0.2 * inch  # Define a minimum column width
    
    # Calculate column widths based on content
    col_widths = [max(min_col_width, min(max_col_width, max(len(str(cell)) for cell in col) * 0.1 * inch)) for col in zip(*table_data)]
    total_width = sum(col_widths)
    
    # Adjust font size to fit within the page width
    font_size = 10  # Adjusted font size
    if total_width > pagesize[0] - 1 * inch:
        font_size = max(6, font_size - int((total_width - (pagesize[0] - 1 * inch)) / 10))
    
    # Create a table with data
    table = Table(table_data, colWidths=col_widths)
    
    # Apply styles to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), font_size),  # Adjust font size
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ])
    table.setStyle(style)
    
    # Build the PDF with the table
    elements = [table]
    c.build(elements)

def perform_search_issued_books(search_text, treeview):
    global search_results
    for item in treeview.get_children():
        treeview.delete(item)
    connectdb()
    q = '''
        SELECT ibh.stdid, ibh.serial_number, b.subject, ibh.book_title, ibh.issue_date, ibh.exp_date, ibh.return_timestamp, ibh.return_date, ibh.fine
        FROM issued_book_history ibh
        JOIN book b ON ibh.serial_number = b.serial
        WHERE ibh.book_title LIKE ?
    '''
    cur.execute(q, ('%' + search_text + '%',))
    search_results = cur.fetchall()  # Store search results
    for index, row in enumerate(search_results):
        treeview.insert("", index, value=row)
    closedb()

def download_pdf():
    connectdb()
    # Use search_results if available, otherwise fetch all data
    if search_results:
        details = search_results
    else:
        q = '''
            SELECT ibh.stdid, ibh.serial_number, b.subject, ibh.book_title, ibh.issue_date, ibh.exp_date, ibh.return_timestamp, ibh.return_date, ibh.fine
            FROM issued_book_history ibh
            JOIN book b ON ibh.serial_number = b.serial
        '''
        cur.execute(q)
        details = cur.fetchall()
    closedb()

    if not details:
        messagebox.showinfo("Issued Books History", "No issued books history found.")
        return

    # Prepare data for PDF
    headers = ["Student ID", "Serial No", "Subject", "Book Title", "Issue Date", "Expiry Date", "Return Timestamp", "Return Date", "Fine"]
    details_list = [list(row) for row in details]  # Convert tuples to lists
    data = [headers] + details_list

    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if filename:
        save_to_pdf(data, filename)

def issued_books_history():
    try:
        connectdb()
        q = '''
            SELECT ibh.stdid, ibh.serial_number, b.subject, ibh.book_title, ibh.issue_date, ibh.exp_date, ibh.return_timestamp, ibh.return_date, ibh.fine
            FROM issued_book_history ibh
            JOIN book b ON ibh.serial_number = b.serial
        '''
        cur.execute(q)
        details = cur.fetchall()
        if not details:
            messagebox.showinfo("Issued Books History", "No issued books history found.")
            closedb()
            return

        win = Tk()
        win.title('Issued Books History')
        win.geometry("1200x400+270+180")
        win.resizable(False, False)

        # Create a Frame to hold the Treeview, Search bar, and Scrollbars
        frame = Frame(win)
        frame.pack(fill='both', expand=True)

        # Add a Search Entry and Button
        search_frame = Frame(win)
        search_frame.pack(fill='x', padx=10, pady=5)
        search_label = Label(search_frame, text="Search:")
        search_label.pack(side='left')
        search_entry = Entry(search_frame)
        search_entry.pack(side='left', padx=5)
        search_button = Button(search_frame, text="Search", command=lambda: perform_search_issued_books(search_entry.get(), treeview))
        search_button.pack(side='left')

        # Add a Treeview with scrollbars
        columns = ["Student ID", "Serial No", "Subject", "Book Title", "Issue Date", "Expiry Date", "Return Timestamp", "Return Date", "Fine"]
        treeview = Treeview(frame, columns=columns, show='headings')
        
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, anchor='center')

        # Add vertical scrollbar
        vsb = Scrollbar(frame, orient="vertical", command=treeview.yview)
        vsb.pack(side='right', fill='y')
        treeview.configure(yscrollcommand=vsb.set)

        # Add horizontal scrollbar
        hsb = Scrollbar(frame, orient="horizontal", command=treeview.xview)
        hsb.pack(side='bottom', fill='x')
        treeview.configure(xscrollcommand=hsb.set)
        treeview.pack(fill='both', expand=True)

        # Insert the data into the Treeview
        for index, row in enumerate(details):
            treeview.insert("", index, value=row)

        # Function to handle hover effects
        def on_enter(button):
            button.config(bg='green', fg='white')  # Change background color and text color
        def on_leave(button):
            button.config(bg='red', fg='white')  # Reset background color and text color

        # Add the Download PDF button
        download_button = Button(win, text="Download PDF", bg='green', fg='white', command=download_pdf)
        download_button.pack(side='bottom', pady=10)
        download_button.bind("<Enter>", lambda e: on_enter(download_button))
        download_button.bind("<Leave>", lambda e: on_leave(download_button))

        # Add the Close button
        close_button = Button(win, text="Close", bg='red', fg='white', command=win.destroy)
        close_button.pack(side='bottom', pady=10)
        close_button.bind("<Enter>", lambda e: on_enter(close_button))
        close_button.bind("<Leave>", lambda e: on_leave(close_button))
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        closedb()
def close_window(win):
    win.destroy()

def show_total_books():
    # Create a new top-level window
    top = tk.Toplevel()
    top.title("Total Books")
    top.geometry("500x400")

    # Create a search label and entry box
    search_label = tk.Label(top, text="Search:")
    search_label.pack(pady=5)
    
    search_entry = tk.Entry(top)
    search_entry.pack(pady=5)

    # Create a Treeview widget
    tree = ttk.Treeview(top, columns=("subject", "count"), show="headings", height=10)
    tree.heading("subject", text="Subject", command=lambda: sort_column(tree, "subject", False))
    tree.heading("count", text="Count", command=lambda: sort_column(tree, "count", False))
    
    tree.column("subject", width=250, anchor=tk.CENTER)
    tree.column("count", width=100, anchor=tk.CENTER)

    # Function to populate the treeview
    def populate_treeview(rows):
        # Clear existing data
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Function to search in treeview
    def search():
        query = search_entry.get().lower()
        matching_rows = [row for row in data if query in str(row).lower()]
        populate_treeview(matching_rows)

    # Connect to the database
    conn = p.connect(host='localhost', user='root', password='root', database='library')
    cursor = conn.cursor()

    try:
        # Query to get total number of available books
        cursor.execute("SELECT SUM(quantity) FROM book")
        total_available_books = cursor.fetchone()[0]
        if total_available_books is None:
            total_available_books = 0

        # Query to get the number of books issued
        cursor.execute("SELECT COUNT(*) FROM bookissue")
        total_issued_books = cursor.fetchone()[0]
        if total_issued_books is None:
            total_issued_books = 0

        # Query to get the count of books by subject
        cursor.execute("SELECT subject, SUM(quantity) FROM book GROUP BY subject")
        books_by_subject = cursor.fetchall()

        # Combine data and add total counts at the end
        data = list(books_by_subject) + [("Total Available Books", total_available_books), ("Total Issued Books", total_issued_books)]

        # Populate the treeview with data
        populate_treeview(data)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    
    finally:
        # Close the database connection
        cursor.close()
        conn.close()

    # Function to sort columns
    def sort_column(tree, col, reverse):
        rows = [(tree.set(k, col), k) for k in tree.get_children("")]
        rows.sort(reverse=reverse)

        for index, (val, k) in enumerate(rows):
            tree.move(k, "", index)

        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

    # Add search button
    search_button = tk.Button(top, text="Search", command=search)
    search_button.pack(pady=5)

    # Pack the Treeview
    tree.pack(fill=tk.BOTH, expand=True)
def addbook():
    global win
    win.destroy()
    win = Tk()
    win.title('Add Book')
    win.geometry("400x400+480+180")
    win.resizable(False, False)

    sub = Label(win, text='SUBJECT')
    tit = Label(win, text='TITLE')
    auth = Label(win, text='AUTHOR')
    ser = Label(win, text='SERIAL NO')
    qty = Label(win, text='QUANTITY')  # New label for quantity

    global e1, e2, e3, e4, e5, b, b1

    e1 = Entry(win, width=25)
    e2 = Entry(win, width=25)
    e3 = Entry(win, width=25)
    e4 = Entry(win, width=25)
    e5 = Entry(win, width=25)  # New entry for quantity

    def on_enter(event):
        event.widget.config(bg='#2980b9', fg='white')  # Darker blue and white text for hover

    def on_leave(event):
        event.widget.config(bg='blue', fg='white')  # Original blue color and white text

    def on_close_enter(event):
        event.widget.config(bg='#c0392b', fg='white')  # Darker red and white text for hover

    def on_close_leave(event):
        event.widget.config(bg='red', fg='white')  # Original red color and white text

    b = Button(win, height=2, width=21, text='ADD BOOK TO DB', bg='blue', fg='white', command=addbooks)
    b1 = Button(win, height=2, width=21, text='CLOSE', bg='red', fg='white', command=closebooks)

    # Bind hover events to the "Add Book to DB" button
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

    # Bind hover events to the "Close" button
    b1.bind("<Enter>", on_close_enter)
    b1.bind("<Leave>", on_close_leave)

    sub.place(x=70, y=50)
    tit.place(x=70, y=90)
    auth.place(x=70, y=130)
    ser.place(x=70, y=170)
    qty.place(x=70, y=210)  # New placement for quantity

    e1.place(x=180, y=50)
    e2.place(x=180, y=90)
    e3.place(x=180, y=130)
    e4.place(x=180, y=170)
    e5.place(x=180, y=210)  # New entry placement for quantity

    b.place(x=180, y=250)
    b1.place(x=180, y=292)

    win.mainloop()

def addbooks():
    connectdb()
    # Check if the serial number already exists
    cur.execute('SELECT * FROM book WHERE serial=%s', (int(e4.get()),))
    existing_serial = cur.fetchone()
    if existing_serial:
        messagebox.showerror("Error", "Serial No. already exists!")
        closedb()
        return
    # Set default quantity to 1 if the entry field is empty
    quantity = int(e5.get() or 1)
    # Insert the new book record
    q = 'INSERT INTO book(subject, title, author, serial, quantity) VALUES (%s, %s, %s, %s, %s)'
    cur.execute(q, (e1.get(), e2.get(), e3.get(), int(e4.get()), quantity))
    # Generate QR code for the new book
    book_details = f"Subject: {e1.get()}, Title: {e2.get()}, Author: {e3.get()}, Serial No: {e4.get()}, Quantity: {quantity}"
    qr_file_path = generate_qr_code(int(e4.get()), book_details)
    # Update the book record with QR code path
    q = 'UPDATE book SET qr_code=%s WHERE serial=%s'
    cur.execute(q, (qr_file_path, int(e4.get())))
    # Commit the changes to the database
    con.commit()
    win.destroy()
    messagebox.showinfo("Book", "Book Added!")
    closedb()
    libr()

def generate_qr_code(serial, book_details):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{book_details}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    # Save QR code image
    file_path = f"qr_codes/{serial}.png"
    if not os.path.exists("qr_codes"):
        os.makedirs("qr_codes")
    img.save(file_path)
    return file_path

def show_qr_code(serial):
    # Load QR code image
    qr_code_path = f"qr_codes/{serial}.png"
    if not os.path.exists(qr_code_path):
        print(f"QR code file not found: {qr_code_path}")
        return
    qr_image = Image.open(qr_code_path)
    qr_photo = ImageTk.PhotoImage(qr_image)
    # Create a Tkinter window
    window = tk.Tk()
    window.title("View Book")
    # Display the QR code image
    qr_label = tk.Label(window, image=qr_photo)
    qr_label.pack()
    
    # Keep a reference to the image to prevent garbage collection
    qr_label.image = qr_photo

    # Run the Tkinter event loop
    window.mainloop()

def updatebook():
    global win
    win.destroy()
    win = tk.Tk()
    win.title('Update Book')
    win.geometry("400x400+480+180")
    win.resizable(False, False)

    # Labels and Entry widgets for input
    serial = tk.Label(win, text='SERIAL NO')
    new_name = tk.Label(win, text='NEW NAME')
    new_title = tk.Label(win, text='NEW TITLE')
    new_author = tk.Label(win, text='NEW AUTHOR')
    
    global e1, e2, e3, e4
    e1 = tk.Entry(win, width=25)  # For serial number
    e2 = tk.Entry(win, width=25)  # For new name
    e3 = tk.Entry(win, width=25)  # For new title
    e4 = tk.Entry(win, width=25)  # For new author

    # Define button styles
    button_style = {
        'font': ('Helvetica', 12, 'bold'),
        'bg': 'red',
        'fg': 'white',
        'activebackground': '#c0392b',  # Darker red for hover
        'width': 20,
        'height': 2
    }

    # Functions for hover effects
    def on_enter(event):
        event.widget.config(bg='#c0392b', fg='white')  # Darker red for hover and white text

    def on_leave(event):
        event.widget.config(bg='red', fg='white')  # Original red color and white text

    # Create buttons with hover effect
    update_btn = tk.Button(win, text='UPDATE BOOK', command=updatebooks, **button_style)
    close_btn = tk.Button(win, text='CLOSE', command=closebooks, **button_style)

    # Bind hover events to buttons
    update_btn.bind("<Enter>", on_enter)
    update_btn.bind("<Leave>", on_leave)
    close_btn.bind("<Enter>", on_enter)
    close_btn.bind("<Leave>", on_leave)

    # Place widgets in the window
    serial.place(x=70, y=50)
    new_name.place(x=70, y=90)
    new_title.place(x=70, y=130)
    new_author.place(x=70, y=170)
    e1.place(x=180, y=50)
    e2.place(x=180, y=90)
    e3.place(x=180, y=130)
    e4.place(x=180, y=170)
    update_btn.place(x=180, y=210)
    close_btn.place(x=180, y=250)

    win.mainloop()

def updatebooks():
    connectdb()
    # Check if the serial number exists
    cur.execute('SELECT * FROM book WHERE serial=%s', (int(e1.get()),))
    existing_book = cur.fetchone()
    if existing_book:
        # Update the book details
        q = 'UPDATE book SET title=%s, author=%s WHERE serial=%s'
        cur.execute(q, (e3.get(), e4.get(), int(e1.get())))
        # Commit the changes to the database
        con.commit()
        win.destroy()
        messagebox.showinfo("Update", "Book Updated!")
    else:
        messagebox.showerror("Error", "Book not found!")
    closedb()
    libr()

def closebooks():
    global win
    win.destroy()
    libr()

def issuebooks():
    global e1, e4, com1y, com1m, com1d, com2y, com2m, com2d
    
    connectdb()
    
    q = 'SELECT quantity FROM book WHERE serial=%s'
    cur.execute(q, (e4.get(),))
    result = cur.fetchone()
    
    if result:
        quantity = int(result[0])
        if quantity > 0:
            try:
                i = datetime.datetime(int(com1y.get()), int(com1m.get()), int(com1d.get()))
                e = datetime.datetime(int(com2y.get()), int(com2m.get()), int(com2d.get()))
                i = i.isoformat()
                e = e.isoformat()
                
                q = 'INSERT INTO bookIssue (stdid, serial, issue, exp) VALUES (%s, %s, %s, %s)'
                cur.execute(q, (e1.get(), e4.get(), i, e))
                
                if quantity == 1:
                    cur.execute('DELETE FROM book WHERE serial=%s', (e4.get(),))
                else:
                    cur.execute('UPDATE book SET quantity = quantity - 1 WHERE serial=%s', (e4.get(),))
                
                con.commit()
                win.destroy()
                messagebox.showinfo("Book", "Book Issued!")
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid date format: {ve}")
        else:
            messagebox.showerror("Error", "No copies available to issue!")
    else:
        messagebox.showerror("Error", "Book not found!")
    
    closedb()
    libr()

def issuebook():
    global win, e1, e4, com1y, com1m, com1d, com2y, com2m, com2d
    
    win = tk.Tk()
    win.title('Issue Book')
    win.geometry("400x400+480+180")
    win.resizable(False, False)
    
    custom_font = ('times new roman', 30, 'bold')
    
    labels = {
        "name": tk.Label(win, text='ISSUE', font=custom_font),
        "branch": tk.Label(win, text='BOOK', font=custom_font),
        "sid": tk.Label(win, text='STUDENT ID'),
        "no": tk.Label(win, text='BOOK NO'),
        "issue": tk.Label(win, text='ISSUE DATE'),
        "exp": tk.Label(win, text='EXPIRY DATE')
    }
    
    e1 = tk.Entry(win, width=25)
    e4 = tk.Entry(win, width=25)
    
    y = [str(i) for i in range(2000, 2031)]
    month = [f"{i:02d}" for i in range(1, 13)]
    d = [f"{i:02d}" for i in range(1, 32)]
    
    com1y = Combobox(win, values=y, width=5)
    com1m = Combobox(win, values=month, width=5)
    com1d = Combobox(win, values=d, width=5)
    com2y = Combobox(win, values=y, width=5)
    com2m = Combobox(win, values=month, width=5)
    com2d = Combobox(win, values=d, width=5)
    
    now = datetime.datetime.now()
    com1y.set(now.year)
    com1m.set(f"{now.month:02d}")
    com1d.set(f"{now.day:02d}")
    com2y.set(now.year)
    com2m.set(f"{now.month:02d}")
    com2d.set(f"{now.day:02d}")
    
    button_style = {
        'font': ('Helvetica', 12, 'bold'),
        'bg': 'red',
        'fg': 'white',
        'activebackground': '#c0392b',
        'width': 21,
        'height': 2
    }
    
    def on_enter(event):
        event.widget.config(bg='#c0392b')
        event.widget.config(font=('Helvetica', 12, 'bold'))
    
    def on_leave(event):
        event.widget.config(bg='red')
        event.widget.config(font=('Helvetica', 12, 'bold'))
    
    b = tk.Button(win, text=' ISSUE BOOK ', command=issuebooks, **button_style)
    b1 = tk.Button(win, text=' CLOSE ', command=win.destroy, **button_style)
    
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    b1.bind("<Enter>", on_enter)
    b1.bind("<Leave>", on_leave)
    
    labels["name"].place(x=55, y=30)
    labels["branch"].place(x=225, y=30)
    labels["sid"].place(x=70, y=130)
    labels["no"].place(x=70, y=170)
    labels["issue"].place(x=70, y=210)
    labels["exp"].place(x=70, y=240)
    e1.place(x=180, y=130)
    e4.place(x=180, y=170)
    com1y.place(x=180, y=210)
    com1m.place(x=230, y=210)
    com1d.place(x=280, y=210)
    com2y.place(x=180, y=240)
    com2m.place(x=230, y=240)
    com2d.place(x=280, y=240)
    b.place(x=178, y=270)
    b1.place(x=178, y=312)
    
    win.mainloop()

def returnbook():
    def on_enter(e):
        e.widget['bg'] = 'darkred'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'

    win = tk.Tk()
    win.title('Return Book')
    win.geometry("400x400+480+180")
    win.resizable(False, False)

    ret = tk.Label(win, text='RETURN ', font=('times new roman', 30, 'bold'))
    book = tk.Label(win, text='BOOK', font=('times new roman', 30, 'bold'))
    no = tk.Label(win, text='BOOK NO')
    date = tk.Label(win, text='RETURN DATE')
    qr_scan = tk.Label(win, text='SCAN QR CODE')
    
    global e4, qr_code_entry
    e4 = tk.Entry(win, width=25)
    qr_code_entry = tk.Entry(win, width=25)
    
    com1y = ttk.Combobox(win, values=[str(year) for year in range(2000, 2101)], width=5)
    com1m = ttk.Combobox(win, values=[f"{i:02d}" for i in range(1, 13)], width=5)
    com1d = ttk.Combobox(win, values=[f"{i:02d}" for i in range(1, 32)], width=5)
    
    now = datetime.datetime.now()
    com1y.set(now.year)
    com1m.set(f"{now.month:02d}")
    com1d.set(f"{now.day:02d}")
    
    b = tk.Button(win, height=2, width=21, text='RETURN BOOK', bg='red', fg='white', command=returnbooks)
    b1 = tk.Button(win, height=2, width=21, text='CLOSE', bg='red', fg='white', command=closebooks)
    scan_button = tk.Button(win, height=2, width=21, text='SCAN QR CODE', bg='green', fg='white', command=scan_qr_code)
    
    # Bind hover effects
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    b1.bind("<Enter>", on_enter)
    b1.bind("<Leave>", on_leave)
    scan_button.bind("<Enter>", on_enter)
    scan_button.bind("<Leave>", on_leave)
    
    ret.place(x=55, y=30)
    book.place(x=225, y=30)
    no.place(x=70, y=120)
    date.place(x=70, y=160)
    qr_scan.place(x=70, y=200)
    e4.place(x=180, y=120)
    com1y.place(x=180, y=160)
    com1m.place(x=230, y=160)
    com1d.place(x=280, y=160)
    qr_code_entry.place(x=180, y=200)
    b.place(x=178, y=240)
    b1.place(x=178, y=282)
    scan_button.place(x=178, y=320)
    
    win.mainloop()
def returnbooks():
    connectdb()
    try:
        serial_number = e4.get()
        if not serial_number:
            messagebox.showerror("Error", "Please enter a book serial number.")
            return
        # Check if the book was issued
        q = 'SELECT exp, issue, stdid FROM bookissue WHERE serial=%s'
        cur.execute(q, (serial_number,))
        issued_book = cur.fetchone()
        if issued_book:
            exp_date = str(issued_book[0])
            issue_date = issued_book[1]
            student_id = issued_book[2]
            current_date = datetime.date.today()
            fine_amount = 0
            # Parse expiration date
            exp_date = datetime.date(int(exp_date[:4]), int(exp_date[5:7]), int(exp_date[8:10]))
            # Calculate fine if return is late
            if current_date > exp_date:
                fine_amount = (current_date - exp_date).days * 10
                messagebox.showinfo("Fine", f'Fine: {fine_amount} rupee')
            # Insert the return information into the history table, including the fine amount
            cur.execute('INSERT INTO issued_book_history (serial_number, issue_date, exp_date, return_date, return_timestamp, stdid, fine) VALUES (%s, %s, %s, %s, NOW(), %s, %s)', 
                        (serial_number, issue_date, exp_date, current_date, student_id, fine_amount))
            # Update the book quantity in the book table
            cur.execute('UPDATE book SET quantity = quantity + 1 WHERE serial=%s', (serial_number,))
            # Remove the returned book from the issued book records
            cur.execute('DELETE FROM bookissue WHERE serial=%s', (serial_number,))
            # Commit the transaction
            con.commit()
            messagebox.showinfo("Success", "Book Returned!")
        else:
            messagebox.showerror("Error", "Book not found in issued records!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        win.destroy()
        closedb()
        libr()

def scan_qr_code():
    qr_code = qr_code_entry.get()
    if qr_code:
        # Extract serial number from QR code content
        serial_number = extract_serial_from_qr_code(qr_code)
        e4.delete(0, END)
        e4.insert(0, serial_number)
    else:
        messagebox.showerror("Error", "Please scan a QR code or enter the book serial number.")

def extract_serial_from_qr_code(qr_code_content):
    # Example extraction logic
    parts = qr_code_content.split("Serial No: ")
    if len(parts) > 1:
        return parts[1].strip()
    return ""

def view_books():
    connectdb()
    cur.execute('SELECT * FROM book')
    rows = cur.fetchall()
    for row in rows:
        print(row)  # or update your GUI listbox with book details
    closedb()

def save_to_pdf(data, filename):
    # Define the page size for A4
    pagesize = A4
    width, height = pagesize
    
    # Create a PDF document
    doc = SimpleDocTemplate(filename, pagesize=pagesize)
    
    # Define table styles and sizes
    col_widths = [1.3 * inch] * len(data[0])  # Adjust column width to fit A4
    row_height = 0.3 * inch  # Adjust row height for better fit
    
    # Create a Table object
    table = Table(data, colWidths=col_widths, rowHeights=[row_height] * len(data))
    
    # Define the style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    # Apply the style to the table
    table.setStyle(style)
    
    # Build the PDF document with the table
    doc.build([table])

def perform_search(search_text, treeview):
    for item in treeview.get_children():
        treeview.delete(item)
    
    connectdb()
    
    # Construct the SQL query to search across multiple fields
    q = """
    SELECT * FROM book
    WHERE LOWER(title) LIKE LOWER(%s)
    OR LOWER(subject) LIKE LOWER(%s)
    OR LOWER(author) LIKE LOWER(%s)
    """
    
    # Add wildcard (%) to search text
    search_text = '%' + search_text + '%'
    
    cur.execute(q, (search_text, search_text, search_text))
    details = cur.fetchall()
    global all_data  # Update all_data with search results
    all_data = [('Subject', 'Title', 'Author', 'Serial No', 'Quantity', 'QR Code')] + list(details)
    for row in details:
        qr_image_path = row[5] if row[5] else ""
        # Load QR code image
        qr_image = Image.open(qr_image_path) if qr_image_path else None
        qr_image = qr_image.resize((100, 100)) if qr_image else None
        qr_image_tk = ImageTk.PhotoImage(qr_image) if qr_image else None
        treeview.insert("", 'end', values=row + (qr_image_tk,))
    
    closedb()
def viewbook():
    def on_enter(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'green'
        e.widget['fg'] = 'white'

    def perform_search_with_option():
        search_text = search_entry.get()
        perform_search(search_text, treeview)
    
    def download_pdf():
        connectdb()
        q = 'SELECT * FROM book'
        cur.execute(q)
        details = cur.fetchall()
        # Prepare data for PDF
        data = [('Subject', 'Title', 'Author', 'Serial No', 'Quantity', 'QR Code')] + list(details)
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            save_to_pdf(data, filename)

    def open_whatsapp():
        url = "https://web.whatsapp.com/"  # URL for WhatsApp Web
        webbrowser.open(url)

    win = tk.Tk()
    win.title('View Books')
    win.geometry("1200x400+270+180")
    win.resizable(True, True)  # Allow resizing

    # Create a frame for the search bar and button
    search_frame = tk.Frame(win)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    search_label = tk.Label(search_frame, text="Search by Book Name, Subject, or Author:")
    search_label.pack(side=tk.LEFT, padx=10, pady=10)

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a canvas and scrollbars
    canvas = tk.Canvas(win)
    v_scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    h_scrollbar = tk.Scrollbar(win, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    # Create a frame to hold the Treeview
    frame = tk.Frame(canvas)
    
    # Add the frame to the canvas
    canvas.create_window((0, 0), window=frame, anchor='nw')
    
    # Create the Treeview widget
    columns = ("Subject", "Title", "Author", "Serial No", "Quantity", "QR Code")
    treeview = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        treeview.heading(col, text=col, command=lambda _col=col: sort_by_column(treeview, _col, False))
        treeview.column(col, anchor='center')
    
    # Add data to the Treeview
    connectdb()
    q = 'SELECT * FROM book'
    cur.execute(q)
    details = cur.fetchall()
    for row in details:
        qr_image_path = row[5] if row[5] else ""
        # Load QR code image
        qr_image = Image.open(qr_image_path) if qr_image_path else None
        qr_image = qr_image.resize((100, 100)) if qr_image else None
        qr_image_tk = ImageTk.PhotoImage(qr_image) if qr_image else None
        treeview.insert("", 'end', values=row + (qr_image_tk,))

    # Pack the Treeview
    treeview.pack(fill='both', expand=True)
    
    # Update the canvas scrollregion
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Pack the canvas and scrollbars
    canvas.pack(side='left', fill='both', expand=True)
    v_scrollbar.pack(side='right', fill='y')
    h_scrollbar.pack(side='bottom', fill='x')

    # Add the search button
    search_button = tk.Button(search_frame, text="Search",bg='green',fg='white',command=perform_search_with_option)
    search_button.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Bind hover effects
    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)

    # Add the Download button
    download_button = tk.Button(search_frame, text="Download PDF", command=download_pdf, bg='green', fg='white')
    download_button.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Bind hover effects to the download button
    download_button.bind("<Enter>", on_enter)
    download_button.bind("<Leave>", on_leave)
    
    # Add the WhatsApp button
    whatsapp_button = tk.Button(search_frame, text="WhatsApp", command=open_whatsapp, bg='green', fg='white')
    whatsapp_button.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Bind hover effects to the WhatsApp button
    whatsapp_button.bind("<Enter>", on_enter)
    whatsapp_button.bind("<Leave>", on_leave)
    
    # Add the Close button
    close_button = tk.Button(win, text="Close", command=lambda: win.destroy(), bg='red', fg='white')
    close_button.pack(side='bottom', pady=10)
    
    # Bind hover effects to the close button
    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)
    
    win.mainloop()
    closedb()

def perform_search_issued_books(search_term, treeview):
    connectdb()
    search_term = search_term.strip().lower()
    
    # Adjust the query to search within issued book history based on various fields
    query = '''
        SELECT 
            ibh.stdid, 
            ibh.serial_number, 
            b.subject,
            ibh.book_title, 
            ibh.issue_date, 
            ibh.exp_date, 
            ibh.return_timestamp, 
            ibh.return_date, 
            ibh.fine
        FROM issued_book_history ibh
        JOIN book b ON ibh.serial_number = b.serial
        WHERE LOWER(ibh.stdid) LIKE %s 
        OR LOWER(ibh.serial_number) LIKE %s 
        OR LOWER(b.subject) LIKE %s 
        OR LOWER(ibh.book_title) LIKE %s
        OR LOWER(ibh.issue_date) LIKE %s
        OR LOWER(ibh.exp_date) LIKE %s
        OR LOWER(ibh.return_timestamp) LIKE %s
        OR LOWER(ibh.return_date) LIKE %s
        OR LOWER(ibh.fine) LIKE %s
    '''
    
    # Generate search terms for each field
    search_wildcard = '%' + search_term + '%'
    params = (search_wildcard, search_wildcard, search_wildcard, search_wildcard, 
              search_wildcard, search_wildcard, search_wildcard, search_wildcard, search_wildcard)
    
    cur.execute(query, params)
    results = cur.fetchall()
    
    # Clear the Treeview before inserting search results
    for item in treeview.get_children():
        treeview.delete(item)
    
    if not results:
        messagebox.showinfo("Search Results", "No issued books history found.")
    else:
        for row in results:
            treeview.insert("", 'end', values=row)
    
    closedb()


def sort_by_column(treeview, col_name, descending):
    data = [(treeview.set(child_id, col_name), child_id) for child_id in treeview.get_children('')]
    data.sort(reverse=descending)
    for index, (val, child_id) in enumerate(data):
        treeview.move(child_id, '', index)
    treeview.heading(col_name, command=lambda: sort_by_column(treeview, col_name, not descending))

def close_window(window):
    window.destroy()
    libr()

def issuedbook():
    def on_enter(e):
        e.widget['bg'] = 'darkred'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'

    connectdb()
    q = 'SELECT * FROM bookissue'
    cur.execute(q)
    details = cur.fetchall()
    
    if len(details) != 0:
        win = Tk()
        win.title('Issued Books')
        win.geometry("800x300+270+180")
        win.resizable(False, False)
        
        # Create Treeview widget
        treeview = Treeview(win, columns=("Student ID", "Serial No", "Issue Date", "Expiry Date"), show='headings')
        treeview.heading("Student ID", text="Student ID")
        treeview.heading("Serial No", text="Serial No")
        treeview.heading("Issue Date", text="Issue Date")
        treeview.heading("Expiry Date", text="Expiry Date")
        treeview.column("Student ID", anchor='center')
        treeview.column("Serial No", anchor='center')
        treeview.column("Issue Date", anchor='center')
        treeview.column("Expiry Date", anchor='center')
        
        # Insert data into Treeview
        index = 0
        iid = 0
        for row in details:
            treeview.insert("", index, iid, value=row)
            index = iid = index + 1
        
        treeview.pack(fill='both', expand=True)
        
        # Add the Close button with hover effects
        close_button = Button(win, text="Close", bg='red', fg='white', command=lambda: close_window(win))
        close_button.pack(side='bottom', pady=10)
        
        # Bind hover effects to the close button
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)
        
        win.mainloop()
    else:
        messagebox.showinfo("Books", "No Book Issued")
    
    closedb()
def deletebook():
    def on_enter(e):
        e.widget['bg'] = 'darkred'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'

    global win
    win.destroy()
    win = Tk()
    win.title('Delete Book')
    win.geometry("400x400+480+180")
    win.resizable(False, False)
    
    usid = Label(win, text='Serial NO')
    paswrd = Label(win, text='PASSWORD')
    
    global e1, e2
    e1 = Entry(win)
    e2 = Entry(win, show='*')  # Password field with masked text
    
    b1 = Button(win, height=2, width=17, text=' DELETE ', bg='red', fg='white', command=deletebooks)
    b2 = Button(win, height=2, width=17, text=' CLOSE ', bg='red', fg='white', command=closebooks)
    
    usid.place(x=80, y=100)
    paswrd.place(x=70, y=140)
    e1.place(x=180, y=100)
    e2.place(x=180, y=142)
    b1.place(x=180, y=180)
    b2.place(x=180, y=230)
    
    # Bind hover effects to the buttons
    b1.bind("<Enter>", on_enter)
    b1.bind("<Leave>", on_leave)
    b2.bind("<Enter>", on_enter)
    b2.bind("<Leave>", on_leave)

    win.mainloop()
def deletebooks():
    connectdb()
    if e2.get()=='vansh2807':
        q='DELETE FROM book WHERE serial="%i"'
        cur.execute(q%(int(e1.get())))
        con.commit()
        win.destroy()
        messagebox.showinfo("Delete", "Book Deleted!")
        closedb()
        libr()
    else:
        messagebox.showinfo("Error", "Incorrect Password!")
        closedb()

def loginadmin():
    if e1.get() == 'admin' and e2.get() == 'vansh2807':
        admin()
    else:
        messagebox.showerror("Error", "Wrong Password!")


def admin():
    def on_enter(e):
        e.widget['bg'] = 'darkred'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'

    window.withdraw()  # Assuming 'window' is defined elsewhere
    global win, b1, b2, b3, b4, b5, cur, con
    win = Tk()
    win.title('Admin')
    win.geometry("400x500+480+180")
    win.resizable(False, False)
    
    b1 = Button(win, height=2, width=25, text=' Add User ', bg='blue', fg='white', command=adduser)
    b2 = Button(win, height=2, width=25, text=' View User ', bg='blue', fg='white', command=viewuser)
    b3 = Button(win, height=2, width=25, text=' Delete User ', bg='blue', fg='white', command=deleteuser)
    b4 = Button(win, height=2, width=25, text=' Show Login History ', bg='blue', fg='white', command=show_login_history)
    b5 = Button(win, height=2, width=25, text=' LogOut ', bg='red', fg='white', command=logout)
    
    b1.place(x=110, y=30)
    b2.place(x=110, y=80)
    b3.place(x=110, y=130)
    b4.place(x=110, y=180)
    b5.place(x=110, y=230)
    
    # Bind hover effects to the buttons
    b1.bind("<Enter>", on_enter)
    b1.bind("<Leave>", on_leave)
    b2.bind("<Enter>", on_enter)
    b2.bind("<Leave>", on_leave)
    b3.bind("<Enter>", on_enter)
    b3.bind("<Leave>", on_leave)
    b4.bind("<Enter>", on_enter)
    b4.bind("<Leave>", on_leave)
    b5.bind("<Enter>", on_enter)
    b5.bind("<Leave>", on_leave)

    win.mainloop()

def show_login_history():
    def on_enter(e):
        e.widget['bg'] = 'darkred'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'

    win = Tk()
    win.title('Login History')
    win.geometry("800x400+270+180")
    win.resizable(True, True)
    
    # Create a canvas and scrollbars
    canvas = Canvas(win)
    v_scrollbar = Scrollbar(win, orient="vertical", command=canvas.yview)
    h_scrollbar = Scrollbar(win, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    # Create a frame to hold the Treeview
    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')
    
    # Create the Treeview widget
    treeview = Treeview(frame, columns=("Username", "Login Time"), show='headings', xscrollcommand=h_scrollbar.set)
    treeview.heading("Username", text="Username")
    treeview.heading("Login Time", text="Login Time")
    treeview.column("Username", anchor='center')
    treeview.column("Login Time", anchor='center')
    
    # Add data to the Treeview
    connectdb()
    q = 'SELECT username, login_time FROM LoginHistory'
    cur.execute(q)
    details = cur.fetchall()
    for row in details:
        treeview.insert("", 'end', values=row)
    
    # Pack the Treeview
    treeview.pack(fill='both', expand=True)
    
    # Update the canvas scrollregion
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Pack the canvas and scrollbars
    canvas.pack(side='left', fill='both', expand=True)
    v_scrollbar.pack(side='right', fill='y')
    h_scrollbar.pack(side='bottom', fill='x')
    
    # Add the Close button
    close_button = Button(win, text="Close", bg='red', fg='white', command=lambda: close_window(win))
    close_button.pack(side='bottom', pady=10)
    
    # Bind hover effects to the Close button
    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)
    
    win.mainloop()
    closedb()
def logout():    
    win.destroy()
    try:
        closedb()
    except:
        print("Logged Out")
    home()
def closedb():
    global con  # Ensure you are referring to the global connection object
    if con.open:
        con.close()

def adduser():
    def on_enter(e):
        e.widget['bg'] = 'darkred'
        e.widget['fg'] = 'white'

    def on_leave(e):
        e.widget['bg'] = 'red'
        e.widget['fg'] = 'white'
    
    global win
    win.destroy()
    win = Tk()
    win.title('Add User')
    win.geometry("400x400+480+180")
    win.resizable(False, False)

    name = Label(win, text='NAME')
    usid = Label(win, text='USER ID')
    branch = Label(win, text='BRANCH')
    mob = Label(win, text='MOBILE NO')
    
    global e1, e2, e3, e4
    e1 = Entry(win, width=25)
    e2 = Entry(win, width=25)
    e3 = Entry(win, width=25)
    e4 = Entry(win, width=25)
    
    b = Button(win, height=2, width=21, text=' ADD USER ', bg='red', fg='white', command=addusers)
    b1 = Button(win, height=2, width=21, text=' CLOSE ', bg='red', fg='white', command=closeusers)
    
    name.place(x=70, y=100)
    usid.place(x=70, y=140)
    branch.place(x=70, y=180)
    mob.place(x=70, y=220)
    
    e1.place(x=180, y=100)
    e2.place(x=180, y=140)
    e3.place(x=180, y=180)
    e4.place(x=180, y=220)
    
    b.place(x=178, y=250)
    b1.place(x=178, y=293)
    
    # Bind hover effects to the buttons
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    b1.bind("<Enter>", on_enter)
    b1.bind("<Leave>", on_leave)
    
    win.mainloop()
def addusers():
    connectdb()
    q='INSERT INTO login VALUE("%s","%i","%s","%i")'
    global con,cur
    cur.execute(q%(e1.get(),int(e2.get()),e3.get(),int(e4.get())))
    con.commit()
    win.destroy()
    messagebox.showinfo("User", "User Added!")
    closedb()
    admin()

def closeusers():
    global win
    win.destroy()
    admin()

def viewuser():
    win = Tk()
    win.title('View User')
    win.geometry("800x300+270+180")
    win.resizable(True, True)  # Allow resizing
    # Create a canvas and scrollbars
    canvas = Canvas(win)
    v_scrollbar = Scrollbar(win, orient="vertical", command=canvas.yview)
    h_scrollbar = Scrollbar(win, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    # Create a frame to hold the Treeview
    frame = Frame(canvas)
    # Add the frame to the canvas
    canvas.create_window((0, 0), window=frame, anchor='nw')
    # Create the Treeview widget
    treeview = Treeview(frame, columns=("Name", "User ID", "Branch", "Mobile No"), show='headings')
    treeview.heading("Name", text="Name")
    treeview.heading("User ID", text="User ID")
    treeview.heading("Branch", text="Branch")
    treeview.heading("Mobile No", text="Mobile No")
    treeview.column("Name", anchor='center')
    treeview.column("User ID", anchor='center')
    treeview.column("Branch", anchor='center')
    treeview.column("Mobile No", anchor='center')
    # Add data to the Treeview
    connectdb()
    query = 'SELECT * FROM login'
    cur.execute(query)
    details = cur.fetchall()
    for row in details:
        treeview.insert("", 'end', values=row)
    # Pack the Treeview
    treeview.pack(fill='both', expand=True)
    # Update the canvas scrollregion
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    # Pack the canvas and scrollbars
    canvas.pack(side='left', fill='both', expand=True)
    v_scrollbar.pack(side='right', fill='y')
    h_scrollbar.pack(side='bottom', fill='x')
    win.mainloop()
    closedb()

def deleteuser():
    global win
    win.destroy()
    win=Tk()
    win.title('Delete user')
    win.geometry("400x400+480+180")
    win.resizable(False,False)
    usid=Label(win,text='USER ID')
    paswrd=Label(win,text='ADMIN \n PASSWORD')
    global e1
    e1=Entry(win)
    global e2,b2
    e2=Entry(win)
    b1=Button(win, height=2,width=17,text=' DELETE ',command=deleteusers)
    b2=Button(win, height=2,width=17,text=' CLOSE ',command=closeusers)
    usid.place(x=80,y=100)
    paswrd.place(x=70,y=140)
    e1.place(x=180,y=100)
    e2.place(x=180,y=142)
    b1.place(x=180,y=180)
    b2.place(x=180,y=230)
    win.mainloop()

def deleteusers():
    connectdb()
    if e2.get()=='admin':
        q='DELETE FROM login WHERE userid="%i"'
        cur.execute(q%(int(e1.get())))
        con.commit()
        win.destroy()
        messagebox.showinfo("Delete", "User Deleted")
        closedb()
        admin()
    else:
        messagebox.showinfo("Error", "Incorrect Password!")
        closedb()

def connectdb():
    global con, cur
    con = p.connect(host="localhost", user="root", passwd="root")
    cur = con.cursor()
    cur.execute('CREATE DATABASE IF NOT EXISTS library')
    cur.execute('USE library')
    global enter
    if enter == 1:
        l = 'CREATE TABLE IF NOT EXISTS Login(name varchar(20), userid varchar(10), branch varchar(20), mobile int(10))'
        b = 'CREATE TABLE IF NOT EXISTS Book(subject varchar(20), title varchar(20), author varchar(20), serial int(5), quantity int(5))'
        i = 'CREATE TABLE IF NOT EXISTS BookIssue(stdid varchar(20), serial varchar(10), issue date, exp date)'
        cur.execute(l)
        cur.execute(b)
        cur.execute(i)
        enter = enter + 1
    query = 'SELECT * FROM login'
    cur.execute(query)

def home():
    global window, e1, e2, eye_button, background_image
    
    # Check if 'window' exists and is a valid Tkinter window
    if 'window' in globals() and window is not None and window.winfo_exists():
        window.destroy()  # Destroy the existing window if it exists

    window = Tk()  # Create a new window instance
    window.title('Login')
    window.geometry("500x400+480+180")
    window.resizable(False, False)

    # Load background image and keep a reference to it
    background_image = PhotoImage(file=r"C:\Users\Vansh Kabaria\book 1.png")  # Update with your image path
    background_label = Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Labels
    user_label = Label(window, text='User ID', bg='white')
    pass_label = Label(window, text='Password', bg='white')

    # Entries
    e1 = Entry(window, width=30)
    e2 = Entry(window, width=30, show='*')  # Password Entry masked
    
    # Eye button to toggle visibility
    eye_button = Button(window, text='Show', height="1", command=toggle_password)

    # Buttons with hover effects
    login_button = Button(window, text='Login', width=25, height=2, command=loginlibr)
    login_button.bind("<Enter>", lambda e: on_enter(login_button))
    login_button.bind("<Leave>", lambda e: on_leave(login_button))

    admin_button = Button(window, text='Admin Login', width=25, height=2, command=loginadmin)
    admin_button.bind("<Enter>", lambda e: on_enter(admin_button))
    admin_button.bind("<Leave>", lambda e: on_leave(admin_button))

    # Layout (position in x or y axis)
    user_label.place(x=80, y=100)
    pass_label.place(x=80, y=140)
    e1.place(x=180, y=100)
    e2.place(x=180, y=140)
    eye_button.place(x=400, y=135)  # Position of eye button
    login_button.place(x=180, y=180)
    admin_button.place(x=180, y=230)

    window.mainloop()

def on_enter(e):
    e.config(bg='light blue', cursor='hand2')

def on_leave(e):
    e.config(bg='SystemButtonFace')

enter=1
home()
