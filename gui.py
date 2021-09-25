
import tkinter as tk                # python 3
from tkinter.constants import X  # python 3
import tkinter.font as font

from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from typing_extensions import IntVar

import main


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SBS, SBP, CBS):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btnFont = font.Font(weight="bold", size=20)

        B1 = tk.Button(self, text="Separate by students",
                       command=lambda: controller.show_frame("SBS"), font=btnFont)

        B2 = tk.Button(self, text="Separate by pages",
                       command=lambda: controller.show_frame("SBP"), font=btnFont)

        B3 = tk.Button(self, text="Combine by students",
                       command=lambda: controller.show_frame("CBS"), font=btnFont)

        B1.grid(row=0, column=0, padx=10, pady=10)
        B2.grid(row=0, column=1, padx=10, pady=10)
        B3.grid(row=0, column=2, padx=10, pady=10)


class SBS(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def select_pdf_file():
            filetypes = (
                ('pdf files', '*.pdf'),
            )
            filename = askopenfilename(title='Open a file',
                                       initialdir='/',
                                       filetypes=filetypes)
            fileText.set(filename)
            print(filename)

        def select_csv_file():
            filetypes = (
                ('csv files', '*.csv'),
            )
            filename = askopenfilename(title='Open a file',
                                       initialdir='/',
                                       filetypes=filetypes)
            print(filename)
            csvText.set(filename)

        def start_handler():
            stu = number_of_student.get()
            if fileText.get() == '':
                messagebox.showerror('No pdf file', 'Please pick a pdf file')
            elif stu == 0:
                messagebox.showerror('Input', 'Please enter a valid number')
            elif csvText.get() == '':
                messagebox.showerror('No csv file', 'Please pick a csv file')
            else:
                stu_list = main.get_students_name_by_csv(csvText.get())
                main.sperate_by_students(fileText.get(), stu, stu_list)
                controller.show_frame("StartPage")
                messagebox.showinfo('Successful', 'Seperate successful')

        btnFont = font.Font(weight="bold", size=10)

        returnBtn = tk.Button(self, text="Return to meun",
                              command=lambda: controller.show_frame("StartPage"), font=btnFont)

        label = tk.Label(self, text="Separate by students",
                         font=controller.title_font)
        selectPDFLabel = tk.Label(self, text="selected PDF file:")
        selectCSVLabel = tk.Label(self, text="selected CSV file:")

        fileText = tk.StringVar()
        fileText.set('')
        fileLabel = tk.Label(self, textvariable=fileText)
        selectFileBtn = tk.Button(self, text="Pick PDF File",
                                  command=lambda: select_pdf_file())

        csvText = tk.StringVar()
        csvText.set('')
        csvLabel = tk.Label(self, textvariable=csvText)
        selectCsvBtn = tk.Button(self, text="Pick CSV File",
                                 command=lambda: select_csv_file())

        confirmBtn = tk.Button(self, text="Start",
                               command=lambda: start_handler())

        number_of_student = tk.IntVar()
        entryLabel = tk.Label(self, text="Number of students:")
        studentEntry = tk.Entry(self, textvariable=number_of_student)

        returnBtn.pack()
        label.pack()
        selectPDFLabel.pack()
        fileLabel.pack()
        selectFileBtn.pack()
        selectCSVLabel.pack()
        csvLabel.pack()
        selectCsvBtn.pack()
        entryLabel.pack()
        studentEntry.pack()
        confirmBtn.pack()


class SBP(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def select_pdf_file():
            filetypes = (
                ('pdf files', '*.pdf'),
            )
            filename = askopenfilename(title='Open a file',
                                       initialdir='/',
                                       filetypes=filetypes)
            print(filename)
            fileText.set(filename)

        def start_handler():
            stu = number_of_student.get()
            if fileText.get() == '':
                messagebox.showerror('No pdf file', 'Please pick a pdf file')
            elif stu == 0:
                messagebox.showerror('Input', 'Please enter a valid number')
            else:
                main.sperate_by_pages(fileText.get(), stu)
                controller.show_frame("StartPage")
                messagebox.showinfo('Successful', 'Seperate successful')

        btnFont = font.Font(weight="bold", size=10)

        returnBtn = tk.Button(self, text="Return to meun",
                              command=lambda: controller.show_frame("StartPage"), font=btnFont)

        label = tk.Label(self, text="Separate by pages",
                         font=controller.title_font)
        selectPDFLabel = tk.Label(self, text="selected PDF file:")

        fileText = tk.StringVar()
        fileText.set('')
        fileLabel = tk.Label(self, textvariable=fileText)
        selectFileBtn = tk.Button(self, text="Pick PDF File",
                                  command=lambda: select_pdf_file())

        confirmBtn = tk.Button(self, text="Start",
                               command=lambda: start_handler())

        number_of_student = tk.IntVar()
        entryLabel = tk.Label(self, text="Number of students:")
        studentEntry = tk.Entry(self, textvariable=number_of_student)

        returnBtn.pack()
        label.pack()
        selectPDFLabel.pack()
        fileLabel.pack()
        selectFileBtn.pack()
        entryLabel.pack()
        studentEntry.pack()
        confirmBtn.pack()


class CBS(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def select_csv_file():
            filetypes = (
                ('csv files', '*.csv'),
            )
            filename = askopenfilename(title='Open a file',
                                       initialdir='/',
                                       filetypes=filetypes)
            print(filename)
            csvText.set(filename)

        def select_folder():
            filename = askdirectory()
            print(filename)
            folderText.set(filename)

        def start_handler():
            csv = csvText.get()
            folder = folderText.get()
            flat_list = main.get_students_name_by_csv(csv)
            if csv == '':
                messagebox.showerror('No csv file', 'Please pick a csv file')
            res = main.combine_by_students(folder, flat_list)
            if res == "Folder doesn't contain any PDF files":
                messagebox.showerror('Folder error', res)
            elif res == "All PDF files should have the same amout of pages":
                messagebox.showerror('Folder', res)
            else:
                messagebox.showinfo('Successful', res)
                controller.show_frame("StartPage")

        btnFont = font.Font(weight="bold", size=10)

        returnBtn = tk.Button(self, text="Return to meun",
                              command=lambda: controller.show_frame("StartPage"), font=btnFont)

        label = tk.Label(self, text="Combine by students",
                         font=controller.title_font)

        selectCSVLabel = tk.Label(self, text="selected CSV file:")
        csvText = tk.StringVar()
        csvText.set('')
        csvLabel = tk.Label(self, textvariable=csvText)
        selectCsvBtn = tk.Button(self, text="Pick CSV File",
                                 command=lambda: select_csv_file())

        contextLebal = tk.Label(
            self, text="Pick the folder that contains the files you want to combine\nselected folder:")
        folderText = tk.StringVar()
        folderText.set('')
        folderLabel = tk.Label(self, textvariable=folderText)
        selectFolderBtn = tk.Button(self, text="Pick folder",
                                    command=lambda: select_folder())

        confirmBtn = tk.Button(self, text="Start",
                               command=lambda: start_handler())

        returnBtn.pack()
        label.pack()
        contextLebal.pack()
        folderLabel.pack()
        selectFolderBtn.pack()
        selectCSVLabel.pack()
        csvLabel.pack()
        selectCsvBtn.pack()
        confirmBtn.pack()


if __name__ == "__main__":
    app = MainApp()
    app.title('PDF scipt')
    app.mainloop()
