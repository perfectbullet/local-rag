import os
from PyPDF2 import PdfWriter, PdfReader, PdfMerger


def split_pdf_and_merge(file_path, start_page: int, end_page):
    print('pdf path {}'.format(os.path.abspath(file_path)))
    file_name = os.path.basename(file_path)
    dir_name = os.path.dirname(file_name)
    tmp_dir = 'tmp_pdf'
    print('tmp_dir path {}'.format(os.path.abspath(tmp_dir)))
    os.makedirs(tmp_dir, mode=0o777, exist_ok=True)
    inputpdf = PdfReader(open(file_path, "rb"))
    tmp_pdfs = []
    for i in range(start_page, end_page):
        writer = PdfWriter()
        writer.add_page(inputpdf.pages[i])
        split_name_v1 = os.path.join(tmp_dir, "{}-page-{}".format(i, file_name))
        with open(split_name_v1, "wb") as output_pdf:
            writer.write(output_pdf)
        tmp_pdfs.append(split_name_v1)
    # Merge the split PDF files
    merge_pdf = PdfMerger()

    for tmp_pdf in tmp_pdfs:
        merge_pdf.append(open(tmp_pdf, "rb"))

    new_file_name = os.path.join(dir_name, 'merged_page{}_{}_{}'.format(start_page, end_page, file_name))
    with open(new_file_name, "wb") as output_pdf:
        merge_pdf.write(output_pdf)


if __name__ == '__main__':
    file_name = '../经济学百科.pdf'

    start_page = 0
    end_page = 99
    split_pdf_and_merge(file_name, start_page, end_page)