from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import os

# setting various parameters
ICON = 'page.ico'
IMAGE = Image.open("location.png")
UNITS = {"MB": 2**20, "KB": 2**10, "GB": 2**30}

class AutoDel:
    def __init__(self, master):
        self.master = master

        #self.master.minsize(width=300, height=400)  
        master.title("AutoDel")

        # input path
        self.label_loc = Label(master, text="Enter folder location: ")
        self.label_loc.grid(row=0, pady=10, sticky=E)

        self.entry_loc = Entry(master, width=27)
        self.entry_loc.grid(row=0, column=1, pady=10, sticky=W)
        self.entry_loc.bind_class("Entry", "<Button-3><ButtonRelease-3>", self.show_menu)

        self.label_ex_loc = Label(master, text="Example of a folder location >>")
        self.label_ex_loc.grid(row=1, column=0)

        # location image
        self.photo = ImageTk.PhotoImage(IMAGE)
        self.label_img = Label(master, image = self.photo)
        self.label_img.grid(row=1, column=1)

        self.label_size_scale = Label(master, text="Select a file size and unit below")
        self.label_size_scale.grid(row=2, columnspan=2, pady=10)

        # scale
        self.scale = Scale(master, from_=0, to=1000, orient=HORIZONTAL, length=200, troughcolor='blue')
        self.scale.grid(row=3, column=0, columnspan=2, pady=10, padx=25, sticky=W)

        # dropdown buttons
        self.options_size = ['KB','MB', 'GB']
        self.unit_var = StringVar()
        self.unit_var.set('MB')
        self.size_drop = OptionMenu(master, self.unit_var, *self.options_size)
        self.size_drop.grid(row=3, column=1, padx=20, sticky=E)

        # another dropdown
        self.label_parameter = Label(master, text="Delete files of size ")
        self.label_parameter.grid(row=4, columnspan=2)
        self.options_parameter = ['All Files', 'Above specified size', 'Below specified size']
        self.param_var = StringVar()
        self.param_var.set('All Files')
        self.drop_param = OptionMenu(master, self.param_var, *self.options_parameter)
        self.drop_param.grid(row=5, columnspan=2)

        # delete button
        self.del_button = Button(master, text="Delete files!", command=self.get_info, width=17)
        self.del_button.grid(row=6, columnspan=2, pady=30)

    def get_info(self):

        # get parameters
        get_loc = self.entry_loc.get()
        scale_value = self.scale.get()
        unit = self.unit_var.get()
        param = self.param_var.get()

        desired_size_in_bytes = scale_value*UNITS[unit]
        loc = get_loc.replace("\\", "/")  # path format the program requires

        # check if location is valid
        if not os.path.isdir(loc):
            tkMessageBox.showinfo("Error", "Invalid folder location. Please enter location in the format shown in image!")
            return

        # get the list of files in the folder
        all_files = []
        for root, dirs, files in os.walk(loc, topdown=True):
            all_files = files
            break

        # sort files accordingly
        if param == "Above specified size":
            no_files = self.delete(all_files, True, loc, desired_size_in_bytes)
        elif param ==  'All Files':
            # To delete all files at once
            no_files = self.delete(all_files, True, loc, 0)
        else:
            no_files =self.delete(all_files, False, loc, desired_size_in_bytes)

        notify = "{} files deleted!".format(no_files)
        tkMessageBox.showinfo("Notification", notify)

    def delete(self, files, reverse, dir, size):
        ''' delete files according to value of reverse '''
        files_count = 0

        if reverse: # when you've to delete files above a specific size
            for file in files:
                abspath = dir + '/' + file
                if os.path.getsize(abspath) > size:
                    try:
                        os.remove(abspath)
                        files_count += 1
                    except:
                        pass

        else: # when you've to delete files below a specific size
            for file in files:
                abspath = dir + '\\' + file
                if os.path.getsize(abspath) < size:
                    try:
                        os.remove(abspath)
                        files_count += 1
                    except:
                        pass
        return files_count

    def make_menu(self, w):
        ''' creating cut/copy/paste menu'''
        self.the_menu = Menu(w, tearoff=0)
        self.the_menu.add_command(label="Cut")
        self.the_menu.add_command(label="Copy")
        self.the_menu.add_command(label="Paste")

    def show_menu(self, e):
        ''' showing the cut/copy/paste menu'''
        w = e.widget
        self.the_menu.entryconfigure("Cut",
	                            command=lambda: w.event_generate("<<Cut>>"))
        self.the_menu.entryconfigure("Copy",
	                            command=lambda: w.event_generate("<<Copy>>"))
        self.the_menu.entryconfigure("Paste",
	                            command=lambda: w.event_generate("<<Paste>>"))
        self.the_menu.tk.call("tk_popup", self.the_menu, e.x_root, e.y_root)


root = Tk()

root.iconbitmap(ICON)
my_gui = AutoDel(root)
my_gui.make_menu(root)
root.mainloop()
