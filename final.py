from tkinter import *
from tkinter import ttk, messagebox
import csv

def create_table():
    global tree
    listheader = ['Name', 'Contact Number', 'Email', 'Address']

    tree = ttk.Treeview(frame3_table, selectmode='extended', columns=listheader, show='headings')

    vsb = ttk.Scrollbar(frame3_table, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(frame3_table, orient='horizontal', command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    tree.heading(0, text='Name', anchor=NW)
    tree.heading(1, text='Contact Number', anchor=NW)
    tree.heading(2, text='Email', anchor=NW)
    tree.heading(3, text='Address', anchor=NW)

    tree.column(0, width=100, anchor='nw')
    tree.column(1, width=130, anchor='nw')
    tree.column(2, width=170, anchor='nw')
    tree.column(3, width=80, anchor='nw')

    frame3_table.grid_rowconfigure(0, weight=1)
    frame3_table.grid_columnconfigure(0, weight=1)

    return tree

def add_contact():
    name = e_name.get().strip()
    contact_number = c_num_entry.get().strip()
    email = e_email.get().strip()
    address = e_add.get().strip()

    # Validate name and contact number
    if not name.isalpha():
        messagebox.showerror("Error", "Name should contain only alphabets.")
        return

    if not contact_number.isdigit():
        messagebox.showerror("Error", "Contact Number should contain only digits.")
        return

    # Check for unique contact number
    for item in tree.get_children():
        existing_contact_number = tree.item(item, 'values')[1]
        if contact_number == existing_contact_number:
            messagebox.showerror("Error", "Contact Number must be unique.")
            return

    tree.insert('', 'end', values=(name, contact_number, email, address))
    clear_entries()

def view_contact_list():
    contacts = [(tree.item(item, 'values')[0], tree.item(item, 'values')[1]) for item in tree.get_children()]
    if contacts:
        contacts_str = "\n".join([f"{name}: {number}" for name, number in contacts])
        messagebox.showinfo("Contact List", contacts_str)
    else:
        messagebox.showinfo("Contact List", "No contacts available.")

def search_contact():
    search_text = e_search.get().lower()
    matching_contacts = []

    for item in tree.get_children():
        values = tree.item(item, 'values')
        if search_text in [str(val).lower() for val in values]:
            matching_contacts.append((values[0], values[1]))

    if matching_contacts:
        contacts_str = "\n".join([f"{name}: {number}" for name, number in matching_contacts])
        messagebox.showinfo("Search Result", contacts_str)
    else:
        messagebox.showinfo("Search Result", "No matching contacts found.")

def clear_entries():
    e_name.delete(0, 'end')
    c_num_entry.delete(0, 'end')
    e_email.delete(0, 'end')
    e_add.delete(0, 'end')

def update_contact():
    selected_item = tree.selection()
    if selected_item:
        name = e_name.get()
        contact_number = c_num_entry.get()
        email = e_email.get()
        address = e_add.get()

        if name and contact_number:
            tree.item(selected_item, values=(name, contact_number, email, address))
            clear_entries()
        else:
            messagebox.showerror("Error", "Name and Contact Number are required.")
    else:
        messagebox.showwarning("Warning", "Please select a contact to update.")

def delete_contact():
    selected_item = tree.selection()
    if selected_item:
        result = messagebox.askyesno("Confirmation", "Are you sure you want to delete this contact?")
        if result:
            tree.delete(selected_item)
            clear_entries()
    else:
        messagebox.showwarning("Warning", "Please select a contact to delete.")


window = Tk()
window.title("Contact Book")
window.iconbitmap('icon.ico')
window.geometry('500x450')
window.configure(background='white')
window.resizable(FALSE, FALSE)

frame1 = Frame(window, width=500, height=50, bg="Green")
frame1.grid(row=0, column=0, padx=0, pady=1)

frame2 = Frame(window, width=500, height=150, bg="white")
frame2.grid(row=1, column=0, padx=0, pady=1)

frame3_table = Frame(window, width=500, height=100, bg="grey")
frame3_table.grid(row=2, column=0, columnspan=2, padx=0, pady=1, sticky=NW)

app_name = Label(frame1, text='ContactBook', height=1, font=("verdana", 17, 'bold'), fg='white', bg='green')
app_name.place(x=5, y=5)

l_name = Label(frame2, text="Name : ", width=20, height=1, font=('ivy', 10), bg='White', anchor=NW)
l_name.place(x=10, y=20)

e_name = Entry(frame2, width=25, justify='left', highlightthickness=1, relief='solid')
e_name.place(x=130, y=20)

c_num_label = Label(frame2, text="Contact Number : ", width=20, height=1, font=('ivy', 10), bg='White', anchor=NW)
c_num_label.place(x=10, y=50)

c_num_entry = Entry(frame2, width=25, justify='left', highlightthickness=1, relief='solid')
c_num_entry.place(x=130, y=50)

l_email = Label(frame2, text="Email : ", width=20, height=1, font=('ivy', 10), bg='White', anchor=NW)
l_email.place(x=10, y=80)

e_email = Entry(frame2, width=25, justify='left', highlightthickness=1, relief='solid')
e_email.place(x=130, y=80)

l_add = Label(frame2, text="Address : ", width=20, height=1, font=('ivy', 10), bg='White', anchor=NW)
l_add.place(x=10, y=110)

e_add = Entry(frame2, width=25, justify='left', highlightthickness=1, relief='solid')
e_add.place(x=130, y=110)

b_search = Button(frame2, text='Search', height=1, bg='Green', fg='White', font=('ivy', 8, 'bold'), command=search_contact)
b_search.place(x=300, y=20)

e_search = Entry(frame2, width=20, justify='left', highlightthickness=1, relief='solid')
e_search.place(x=370, y=20)

b_view_list = Button(frame2, text='View Contact List', height=1, bg='Green', fg='White', font=('ivy', 8, 'bold'), command=view_contact_list)
b_view_list.place(x=300, y=60)

b_add = Button(frame2, text='Add Contact', height=1, bg='Green', fg='White', font=('ivy', 8, 'bold'), command=add_contact)
b_add.place(x=415, y=60)

b_update = Button(frame2, text='Update Contact', height=1, bg='Green', fg='White', font=('ivy', 8, 'bold'), command=update_contact)
b_update.place(x=400, y=100)

b_del = Button(frame2, text='Delete Contact', height=1, bg='Green', fg='White', font=('ivy', 8, 'bold'), command=delete_contact)
b_del.place(x=300, y=100)



tree = create_table()

window.mainloop()
