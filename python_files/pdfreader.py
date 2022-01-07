truth_file_pdf = "../Truth_Folder/GhibliStudio/generate_pdf.pdf"
test_pdf_file = "../test_reports/GhibliStudio/ghibliStudioApi_raw_pdf_match2.pdf"

with open(truth_file_pdf, 'rb') as pdf_file:
    truth_cont = pdf_file.read()

with open(test_pdf_file, 'rb') as pdf_file2:
    test_cont = pdf_file2.read()

print(truth_cont == test_cont)

# pdf_read = pdf.PdfFileReader(pdf_data)
# print(pdf_read.numPages)
# pdf_pg_data = pdf_read.getPage(0)




