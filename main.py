from PyPDF2 import PdfFileReader, PdfFileWriter
import csv
import os
import re


def get_students_name_by_csv(csv_path):
    l = list()
    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            l.append(row)
    flat_list = [item for sublist in l for item in sublist]
    return flat_list


def get_pdf_pages(path):
    pdf = PdfFileReader(open(path, 'rb'))
    return pdf.getNumPages()


# This is unreadable
def sperate_by_pages(pdf_path, number_of_students, save_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)

        all_pages = pdf.getNumPages()
        pages_per_students = int(all_pages / number_of_students)

        for page in range(pages_per_students):
            pdf_writer = PdfFileWriter()
            for stu in range(number_of_students):
                p = page + stu*pages_per_students
                pdf_writer.addPage(pdf.getPage(p))

            filePath = os.path.join(save_path, f'all_page_{page+1}.pdf')
            completeName = filePath
            with open(completeName, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)


def separate_by_students(pdf_path, number_of_students, student_list, save_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        all_pages = pdf.getNumPages()
        pages_per_students = int(all_pages / number_of_students)
        for stu in range(number_of_students):
            pdf_writer = PdfFileWriter()
            for page in range(pages_per_students):
                p = page + stu*pages_per_students
                pdf_writer.addPage(pdf.getPage(p))
            if len(student_list) == number_of_students:
                filePath = os.path.join(save_path, f'{student_list[stu]}.pdf')
            else:
                filePath = os.path.join(save_path, f'{stu+1}.pdf')

            completeName = filePath
            with open(completeName, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)


def combine_by_students(folder_path, student_list, save_path):
    def key_for_sorting(name):
        mo = re.findall(r"\d+", name)
        return int(mo[-1])

    all_files = os.listdir(folder_path)
    pdf_files = [os.path.join(folder_path, name)
                 for name in all_files if '.pdf' in name]
    pdf_files.sort(key=key_for_sorting)

    # check if directory is empty
    if pdf_files == []:
        return "Folder doesn't contain any PDF files"
    # check if all files have the same amout of pages
    with open(pdf_files[0], 'rb') as f:
        pdf = PdfFileReader(f)
        num_of_pages = pdf.getNumPages()
    for file in pdf_files:
        with open(file, 'rb') as f:
            pdf = PdfFileReader(f)
            nop = pdf.getNumPages()
        if nop != num_of_pages:
            return "All PDF files should have the same amout of pages"
    # ------------------------------------------------

    for stu in range(num_of_pages):
        pdf_writer = PdfFileWriter()
        for page in range(len(pdf_files)):
            with open(pdf_files[page], 'rb') as f:
                pdf = PdfFileReader(f)
                pdf_writer.addPage(pdf.getPage(stu))
                filePath = os.path.join(
                    save_path, f'{student_list[stu]}.pdf')
                completeName = filePath
                with open(completeName, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)
    return "Combine successfully"


if __name__ == '__main__':
    # flat_list = get_students_name_by_csv('names.csv')
    print(separate_by_students(
        'E:\Local repository\pdfscript\_demo_\original.pdf', 5, ['Kris', 'Hi', 'fjds', 'fdsfh', 'dsfdsf'], 'E:\\'))
