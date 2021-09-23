from PyPDF2 import PdfFileReader, PdfFileWriter
import csv
import os

print(os.getcwd())


def main():
    # import name list
    l = list()
    with open('names.csv', 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            l.append(row)
    flat_list = [item for sublist in l for item in sublist]

    file_name = input("File name:")
    students = int(input("Number of students:"))
    sperate_by_students(file_name, students, flat_list)
    sperate_by_pages(file_name, students)


# This is unreadable
def sperate_by_pages(pdf_path, number_of_students):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)

        all_pages = pdf.getNumPages()
        pages_per_students = int(all_pages / number_of_students)

        for page in range(pages_per_students):
            pdf_writer = PdfFileWriter()
            for stu in range(number_of_students):
                p = page + stu*pages_per_students
                pdf_writer.addPage(pdf.getPage(p))

            filePath = os.path.join(".\out", f'all_page_{page+1}.pdf')
            completeName = os.path.join(os.getcwd(), filePath)
            with open(completeName, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)


def sperate_by_students(pdf_path, number_of_students, student_list):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        all_pages = pdf.getNumPages()
        pages_per_students = int(all_pages / number_of_students)
        for stu in range(number_of_students):
            pdf_writer = PdfFileWriter()
            for page in range(pages_per_students):
                p = page + stu*pages_per_students
                pdf_writer.addPage(pdf.getPage(p))
            filePath = os.path.join(".\out", f'{student_list[stu]}.pdf')
            completeName = os.path.join(os.getcwd(), filePath)
            with open(completeName, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)


if __name__ == '__main__':
    main()
