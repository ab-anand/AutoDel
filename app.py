from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox

IMAGE = Image.open("location.png")

class MyFirstGUI:
    def __init__(self, master):
        self.master = master

        #self.master.minsize(width=300, height=400)  
        master.title("AutoDel")
        self.label_loc = Label(master, text="Enter folder location: ")
        self.label_loc.grid(row=0, pady=10, sticky=E)

        self.entry_loc = Entry(master)
        self.entry_loc.grid(row=0, column=1, pady=10, sticky=W)

        self.label_ex_loc = Label(master, text="Example of a folder location >>")
        self.label_ex_loc.grid(row=1, column=0)

        # location image
        self.photo = ImageTk.PhotoImage(IMAGE)
        self.label_img = Label(master, image = self.photo)
        self.label_img.grid(row=1, column=1)

        self.label_size_scale = Label(master, text="Select a file size and unit below")
        self.label_size_scale.grid(row=2, columnspan=2, pady=10)

        # scale
        self.scale = Scale(master, from_=0, to=1000, orient=HORIZONTAL)
        self.scale.grid(row=3, column=0, columnspan=2, pady=10)

        # manual entry
        # self.entry_size = Entry(master)
        # self.entry_size.grid(row=3, column=1, pady=10)
        #print self.scale.get()

        # size unit and above/below
        # self.label_size_unit = Label(master, text="Select size unit ")
        # self.label_size_unit.grid(row=4, column=0)
        self.options_size = ['KB','MB', 'GB']
        self.unit_var = StringVar()
        self.unit_var.set('MB')
        self.size_drop = OptionMenu(master, self.unit_var, *self.options_size, command=self.unit_func)
        self.size_drop.grid(row=3, column=1)

        self.label_parameter = Label(master, text="Delete files of size ")
        self.label_parameter.grid(row=4, columnspan=2)
        self.options_parameter = ['Above specified size', 'Below specified size']
        self.param_var = StringVar()
        self.param_var.set('Below specified size')
        self.size_drop = OptionMenu(master, self.param_var, *self.options_parameter, command=self.unit_func)
        self.size_drop.grid(row=5, columnspan=2)

        # delete button
        self.del_button = Button(master, text="Delete files!", command=self.delete)
        self.del_button.grid(row=6, columnspan=2, pady=30)



        # self.greet_button = Button(master, text="Greet", command=self.greet)
        # self.greet_button.grid(row=2, column=1)

        # self.close_button = Button(master, text="Close", command=master.quit)
        # self.close_button.pack()

    def greet(self):
        print type(self.scale.get())
    def unit_func(self):
        pass
    def delete(self):
        tkMessageBox.showinfo("Notification", "243 files deleted!")

root = Tk()
root.iconbitmap('page.ico')
my_gui = MyFirstGUI(root)
root.mainloop()
