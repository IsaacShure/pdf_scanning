import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import pypdf
    import pdf2image
    import pytesseract
    import itertools
    from collections.abc import Sequence
    return Sequence, itertools, os, pdf2image, pypdf, pytesseract


@app.cell
def _(os):
    os.listdir()
    return


@app.cell
def _(os):
    def get_pdfs(input_directory, newest_first=True):
        files = os.listdir(input_directory)
        pdf_files = [f for f in files if f.endswith(".pdf")]
        return sorted(pdf_files, key=os.path.getmtime, reverse=newest_first)
    return (get_pdfs,)


@app.cell
def _(pdf2image, pypdf, pytesseract):
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
    return (autorotate_pdf,)


@app.cell
def _(autorotate_pdf, get_pdfs, itertools, pypdf):
    def __main__(input_directory, output_filename, newest_first=True, autorotate=True):
        writer = pypdf.PdfWriter()
        pdf_filenames = get_pdfs(input_directory, newest_first=newest_first)

        if autorotate is True:
            pages = itertools.chain.from_iterable([autorotate_pdf(filename) for filename in pdf_filenames])
        else:
            pages = itertools.chain.from_iterable([pypdf.PdfReader(filename).pages for filename in pdf_filenames])

        for page in pages:
            writer.add_page(page)

        with open(output_filename, "wb") as f:
            writer.write(f)
    return (__main__,)


@app.cell
def _(Sequence, pypdf):
    def rotate_pages(filename, page_numbers, rotations):
        assert isinstance(page_numbers, Sequence)
        assert isinstance(rotations, Sequence)
        assert len(page_numbers) == len(rotations)

        pages = pypdf.PdfReader(filename).pages

        for page_number, rotation in zip(page_numbers, rotations):
            pages[page_number].rotate(rotation)

        writer = pypdf.PdfWriter()

        for page in pages:
            writer.add_page(page)

        with open(filename, "wb") as f:
            writer.write(f)
    return


@app.cell
def _():
    #rotate_pages("H.pdf",[])
    return


@app.cell
def _(__main__):
    __main__("H.pdf")
    return


@app.cell
def _(os):
    sorted(os.listdir(), key=lambda x: os.path.getmtime(x))
    return


@app.cell
def _(get_pdfs):
    get_pdfs()
    return


@app.cell
def _(os):
    [(file, os.path.getmtime(file)) for file in os.listdir()]
    return


@app.cell
def _(pypdf):
    reader = pypdf.PdfReader("doc18569820250520125844.pdf")
    return (reader,)


@app.cell
def _(reader):
    reader.pages[0]
    return


@app.cell
def _(pdf2image):
    images = pdf2image.convert_from_path("doc18569820250520125844.pdf")
    return (images,)


@app.cell
def _(images):
    images
    return


@app.cell
def _(images, pytesseract):
    osd = pytesseract.image_to_osd(images[0], output_type=pytesseract.Output.DICT)
    return (osd,)


@app.cell
def _(osd):
    osd
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
