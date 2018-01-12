from Tkinter import *
from PIL import Image,ImageTk
import tkMessageBox
import os

ICON = 'page.ico'
IMAGE = Image.open("location.png")
UNITS = {"MB": 2**20, "KB": 2**10, "GB": 2**30}

class AutoDel:
    def __init__(self, master):
        self.master = master

        #self.master.minsize(width=300, height=400)  
        master.title("AutoDel")
        self.label_loc = Label(master, text="Enter folder location: ")
        self.label_loc.grid(row=0, pady=10, sticky=E)

        self.entry_loc = Entry(master, width=27)
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
        self.scale = Scale(master, from_=0, to=1000, orient=HORIZONTAL, length=200, troughcolor='blue')
        self.scale.grid(row=3, column=0, columnspan=2, pady=10, padx=25, sticky=W)

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
        self.size_drop = OptionMenu(master, self.unit_var, *self.options_size)
        self.size_drop.grid(row=3, column=1, padx=20, sticky=E)

        self.label_parameter = Label(master, text="Delete files of size ")
        self.label_parameter.grid(row=4, columnspan=2)
        self.options_parameter = ['All Files','Above specified size', 'Below specified size']
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
        loc = get_loc.replace("\\", "/")
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
            # sorted_files = sorted(all_files, key = os.path.abspath.getsize, reverse=True)
            no_files = self.delete(all_files, True, loc, desired_size_in_bytes)
        elif param ==  'All Files':
            #To delete all files at once
            no_files = self.delete(all_files, True, loc,0)
        else:
            #sorted_files = sorted(all_files, key = os.path.getsize)
            no_files =self.delete(all_files, False, loc, desired_size_in_bytes)

        notify = "{} files deleted!".format(no_files)
        tkMessageBox.showinfo("Notification", notify)

    def delete(self, files, reverse, dir, size):
        ''' delete files according to value of reverse '''
        files_count = 0

        if reverse:
            for file in files:
                abspath = dir + '/' + file
                print abspath
                if os.path.getsize(abspath) > size:
                    try:
                        os.remove(abspath)
                        files_count += 1
                    except:
                        pass

        else:
            for file in files:
                abspath = dir + '\\' + file
                # print abspath
                if os.path.getsize(abspath) < size:
                    try:
                        os.remove(abspath)
                        files_count += 1
                    except:
                        pass


        return files_count




root = Tk()
root.iconbitmap(ICON)
my_gui = AutoDel(root)
root.mainloop()
