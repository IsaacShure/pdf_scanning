import os
import argparse
import pypdf
import pytesseract
import itertools


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

def main():
    parser = argparse.ArgumentParser(description="Merge all pdf files in a directory, automatically rotating pages with pytesseract ocr")
    parser.add_argument('input_directory', nargs=1, help="Directory containing pdf files to merge and autorotate")
    parser.add_argument('--output', '-o', required=True, help='Output filename')
    parser.add_argument('--newest-first', '-n', action='store_true', help='Order merged pdf by newest files first.')
    parser.add_argument('--disable-autorotate', '-d', action='store_true', help='Disables ocr page autorotation.')

    args = parser.parse_args()

    writer = pypdf.PdfWriter()
    pdf_filenames = get_pdfs(args.input_directory, newest_first=args.newest_first)

    if args.disable_autorotate:
        pages = itertools.chain.from_iterable([pypdf.PdfReader(filename).pages for filename in pdf_filenames])
    else: 
        pages = itertools.chain.from_iterable([autorotate_pdf(filename) for filename in pdf_filenames])

    for page in pages:
        writer.add_page(page)

    with open(args.output, "wb") as f:
        writer.write(f)
    
if __name__ == "__main__":
    main()
