
import eel
import tkinter
import tkinter.filedialog as filedialog
import os
import main


current_pdf = ''
current_csv = ''
current_save_path = ''
current_com_dir = ''

eel.init('web')


def reset_all():
    global current_pdf
    global current_csv
    global current_com_dir
    global current_save_path
    current_pdf = ''
    current_csv = ''
    current_com_dir = ''
    current_save_path = ''


@eel.expose                         # Expose this function to Javascript
def get_pdf():
    global current_pdf
    global current_save_path
    print('pdf')
    filetypes = (
        ('pdf files', '*.pdf'),
    )
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askopenfilename(filetypes=filetypes)
    print(directory_path)
    current_pdf = directory_path
    if current_pdf == '':
        return ''
    pdf_pages_count = main.get_pdf_pages(directory_path)
    print(pdf_pages_count)
    # set deafault save path
    current_save_path = os.path.dirname(current_pdf)
    eel.pathchange(current_save_path)
    # show pages
    eel.show_page_display(pdf_pages_count)
    # return file name
    return os.path.basename(directory_path)


@eel.expose                         # Expose this function to Javascript
def get_csv():
    global current_csv
    print('csv')
    filetypes = (
        ('csv files', '*.csv'),
    )
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askopenfilename(filetypes=filetypes)
    current_csv = directory_path
    if current_csv == '':
        return ''
    name_list = main.get_students_name_by_csv(directory_path)

    eel.show_csv_preview(name_list, len(name_list))

    # return file name
    return os.path.basename(directory_path)


@eel.expose                         # Expose this function to Javascript
def get_com_dir():
    global current_com_dir
    global current_save_path
    print('com_dir')
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory = filedialog.askdirectory()
    print(directory)
    if directory == '':
        return ''
    current_com_dir = directory
    eel.pathchange(current_com_dir)
    current_save_path = current_com_dir
    # return file name
    return current_com_dir


@eel.expose                         # Expose this function to Javascript
def get_save_path():
    global current_save_path
    print('save_path')
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory = filedialog.askdirectory()
    print(directory)
    if directory == '':
        return ''
    current_save_path = directory
    # return file name
    return current_save_path


@eel.expose
def submit_SBS(student_number):
    if student_number == 'None':
        if current_pdf == '':
            eel.show_noti('pdf')
            return 0
        if current_csv == '':
            eel.show_noti('csv')
            return 0
        student_list = main.get_students_name_by_csv(current_csv)
        main.separate_by_students(
            current_pdf, len(student_list), student_list, current_save_path)

        eel.goback()
        eel.sleep(1.0)
        eel.succes_message('Separated', current_save_path)
        reset_all()

    else:
        if current_pdf == '':
            eel.show_noti('pdf')
            return 0
        if student_number == '':
            eel.show_noti('number')
            return 0
        print(current_save_path)
        main.separate_by_students(
            current_pdf, int(student_number), [], current_save_path)

        eel.goback()
        eel.sleep(1.0)
        eel.succes_message('Separated', current_save_path)
        reset_all()


@eel.expose
def submit_SBP(student_number):
    if current_pdf == '':
        eel.show_noti('pdf')
        return 0
    if student_number == '':
        eel.show_noti('number')
        return 0
    main.sperate_by_pages(current_pdf, int(student_number), current_save_path)
    eel.goback()
    eel.sleep(1.0)
    eel.succes_message('Separated', current_save_path)
    reset_all()


@eel.expose
def submit_CBS():
    if current_com_dir == '':
        eel.show_noti('com')
        return 0
    if current_csv == '':
        eel.show_noti('csv')
        return 0
    student_list = main.get_students_name_by_csv(current_csv)
    res = main.combine_by_students(
        current_com_dir, student_list, current_save_path)
    if res == "Folder doesn't contain any PDF files":
        eel.show_noti('nofile')
        return 0
    elif res == "All PDF files should have the same amout of pages":
        eel.show_noti('notsame')
        return 0
    main.combine_by_students(
        current_com_dir, student_list, current_save_path)
    eel.goback()
    eel.sleep(1.0)
    eel.succes_message('Combined', current_save_path)
    reset_all()


eel.start('index.html', size=(1024, 500))
