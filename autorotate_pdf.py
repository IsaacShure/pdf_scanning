import logging
import os
import argparse
import pypdf
import pytesseract
import itertools

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description="Automatically rotate pages in pdf files using pytesseract")
parser.add_argument('filenames', nargs='+', help="Files to autorotate")
inplace_or_output_group = parser.add_mutually_exclusive_group(required=True)
inplace_or_output_group.add_argument('--output', '-o', help='Output filename')
inplace_or_output_group.add_argument('--inplace', action='store_true', help='Modify files in place')
parser.add_argument('--newest-first', '-n', action='store_true', help='Order merged pdf by newest files first.')

args = parser.parse_args()

if args.newest_first and args.inplace:
    logger.warning("Warning: ignoring merge modifier --newest-first due to specification of mergeless --inplace manipulation")



def get_pdfs(input_directory, newest_first=True):
    files = os.listdir(input_directory)
    pdf_files = [f"{input_directory}/{f}" for f in files if f.endswith(".pdf")]
    return sorted(pdf_files, key=os.path.getmtime, reverse=newest_first)


def autorotate_pdf(filename):
    reader = pypdf.PdfReader(filename)
    images = pdf2image.convert_from_path(filename)

    pages = []

    for page, image in zip(reader.pages, images):
        osd = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
        rotation = int(osd['rotate'])

        if rotation != 0:
            page.rotate(rotation)

        pages.append(page)

    return pages

if __name__ == "__main__":
    print(args)
