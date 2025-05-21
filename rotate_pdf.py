import argparse
import pypdf
import itertools

parser = argparse.ArgumentParser(description="Rotate pages in a pdf file")
parser.add_argument('filename', nargs=1, help="pdf file to modify")
parser.add_argument('page_rotations', nargs='+', help="Specify pages to rotate as follows: '[page #] [rotation] [page #] [rotation]...' Page numbers start from 1 and rotations are in clockwise degrees.")

args = parser.parse_args()

if len(args.page_rotations) % 2 != 0:
    parser.error(f"Received {len(args.page_rotations)} page rotations, expected an even number. Please provide page rotations in the form '[page #] [rotation] [page #] [rotation] etc.'")

    
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

def is_valid_page_number(page_number):
    try:
        assert isinstance(page_number, int)
        assert page_number > 0
        return True
    except:
        return False

def is_valid_rotation(rotation):
    try:
        assert isinstance(rotation, int)
        assert rotation >=0 and rotation <=360
        return True
    except:
        return False

if __name__ == "__main__":
    page_numbers = args.page_rotations[::2]
    rotations = args.page_rotations[1::2]

    for page_number in page_numbers:
        if not is_valid_page_number(page_number):
            parser.error(f"Provided page number {page_number} is invalid")

    for rotation in rotations:
        if not is_valid_rotation(rotation):
            parser.error(f"Provided rotation {rotation} is invalid")

    rotate_pages(args.filename, page_numbers, rotations)
