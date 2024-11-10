from pypdf import PdfReader
from pdfminer.high_level import extract_text

from enum import Enum, auto
from pathlib import Path
from typing import Any, Optional
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage, LITERAL_PAGE
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdftypes import PDFObjRef

class PDFRefType(Enum):
    """PDF reference type."""

    PDF_OBJ_REF = auto()
    DICTIONARY = auto()
    LIST = auto()
    NAMED_REF = auto()
    UNK = auto()  # fallback

class RefPageNumberResolver:
    """PDF Reference to page number resolver.

    .. note::

       Remote Go-To Actions (see 12.6.4.3 in
       `https://www.adobe.com/go/pdfreference/`__)
       are out of the scope of this resolver.

    Attributes:
        document (:obj:`pdfminer.pdfdocument.PDFDocument`):
            The document that contains the references.
        objid_to_pagenum (:obj:`dict[int, int]`):
            Mapping from an object id to the number of the page that contains
            that object.
    """

    def __init__(self, document: PDFDocument):
        self.document = document
        # obj_id -> page_number
        self.objid_to_pagenum: dict[int, int] = {
            page.pageid: page_num
            for page_num, page in enumerate(PDFPage.create_pages(document), 1)
        }

    @classmethod
    def get_ref_type(cls, ref: Any) -> PDFRefType:
        """Get the type of a PDF reference."""
        if isinstance(ref, PDFObjRef):
            return PDFRefType.PDF_OBJ_REF
        elif isinstance(ref, dict) and "D" in ref:
            return PDFRefType.DICTIONARY
        elif isinstance(ref, list) and any(isinstance(e, PDFObjRef) for e in ref):
            return PDFRefType.LIST
        elif isinstance(ref, bytes):
            return PDFRefType.NAMED_REF
        else:
            return PDFRefType.UNK

    @classmethod
    def is_ref_page(cls, ref: Any) -> bool:
        """Check whether a reference is of type '/Page'.

        Args:
            ref (:obj:`Any`):
                The PDF reference.

        Returns:
            :obj:`bool`: :obj:`True` if the reference references
            a page, :obj:`False` otherwise.
        """
        return isinstance(ref, dict) and "Type" in ref and ref["Type"] is LITERAL_PAGE

    def resolve(self, ref: Any) -> Optional[int]:
        """Resolve a PDF reference to a page number recursively.

        Args:
            ref (:obj:`Any`):
                The PDF reference.

        Returns:
            :obj:`Optional[int]`: The page number or :obj:`None`
            if the reference could not be resolved (e.g., remote Go-To
            Actions or malformed references).
        """
        ref_type = self.get_ref_type(ref)

        if ref_type is PDFRefType.PDF_OBJ_REF and self.is_ref_page(ref.resolve()):
            return self.objid_to_pagenum.get(ref.objid)
        elif ref_type is PDFRefType.PDF_OBJ_REF:
            return self.resolve(ref.resolve())

        if ref_type is PDFRefType.DICTIONARY:
            return self.resolve(ref["D"])

        if ref_type is PDFRefType.LIST:
            # Get the PDFObjRef in the list (usually first element).
            return self.resolve(next(filter(lambda e: isinstance(e, PDFObjRef), ref)))

        if ref_type is PDFRefType.NAMED_REF:
            return self.resolve(self.document.get_dest(ref))

        return None  # PDFRefType.UNK

def m(body, start, title):
    i = start
    j = 0
    while j < len(title) and title[j] == ' ':
        j += 1
    while j < len(title):
        if i >= len(body):
            return None
        c = body[i]
        if c == '\n' or c == ' ':
            i += 1
        elif c == title[j]:
            i += 1
            j += 1
        else:
            return None
        while j < len(title) and title[j] == ' ':
            j += 1
    if i == len(body) or body[i] == '\n':
        return i
    return None

def parse_outlines(file: str):
    """Pretty print the outlines (ToC) of a PDF document."""
    with open(file, "rb") as fp:
        try:
            parser = PDFParser(fp)
            document = PDFDocument(parser)

            ref_pagenum_resolver = RefPageNumberResolver(document)

            outlines = list(document.get_outlines())
            if not outlines:
                print("No outlines found.")
            # title, level, start, end
            prev = [["Document", -1, 0, 0]]
            for (level, title, dest, a, se) in outlines:
                if dest:
                    page_num = ref_pagenum_resolver.resolve(dest)
                elif a:
                    page_num = ref_pagenum_resolver.resolve(a)
                elif se:
                    page_num = ref_pagenum_resolver.resolve(se)
                else:
                    page_num = None
                prev[-1][-1] = page_num
                prev.append([title, level, page_num, -1])
            prev[-1][-1] = len(ref_pagenum_resolver.objid_to_pagenum) - 1
        except PDFNoOutlines:
            print("No outlines found.")
        except PDFSyntaxError:
            print("Corrupted PDF or non-PDF file.")
        finally:
            try:
                parser.close()
            except NameError:
                pass  # nothing to do


        reader = PdfReader(file)
        r = []
        for i in range(len(prev)):
            title, level, start, end = prev[i]
            # print("-----")
            # if "IV Adv" in title:
            #     print("ahh")
            #     print(text)
            text = "\n\n".join(page.extract_text() for page in reader.pages[start - 1: end - 1 + 1])
            for j in range(len(text)):
                ahh = m(text, j, title)
                if ahh is not None:
                    text = text[ahh:]
                    break
            if i + 1 < len(prev):
                title2, _, _, _ = prev[i + 1]
                for j in reversed(range(len(text))):
                    ahh = m(text, j, title2)
                    if ahh is not None:
                        text = text[:j]
                        break
            if level <= 1:
                r.append((title, []))
                if len(text.replace(" ", "").replace("\n", "")) > 20:
                    r[-1][1].append(("Introduction", text))
            else:
                r[-1][1].append((title, text))
        # for chapter, sections in r:
        #     print('--------')
        #     print(chapter)
        #     for title, body in sections:
        #         print('-#----')
        #         print(title)
        #         print(body[:100])
        #         print('-@-')
        #         print(body[-100:])

        r.pop(0)

        return r

            # print(title)
            # print(start)
            # print(end)
            # print("---")
            # print(text[:100])
            # print("-@-")
            # print(text[-100:])



def print_outlines(file: str) -> dict[int, int]:
    """Pretty print the outlines (ToC) of a PDF document."""
    with open(file, "rb") as fp:
        try:
            parser = PDFParser(fp)
            document = PDFDocument(parser)

            ref_pagenum_resolver = RefPageNumberResolver(document)

            outlines = list(document.get_outlines())
            if not outlines:
                print("No outlines found.")
            for (level, title, dest, a, se) in outlines:
                if dest:
                    page_num = ref_pagenum_resolver.resolve(dest)
                elif a:
                    page_num = ref_pagenum_resolver.resolve(a)
                elif se:
                    page_num = ref_pagenum_resolver.resolve(se)
                else:
                    page_num = None

                # Calculate leading spaces and filling dots for formatting.
                leading_spaces = (level-1) * 4
                fill_dots = 80 - len(title) - leading_spaces

                print(
                    f"{' ' * leading_spaces}"
                    f"{title}",
                    f"{'.' * fill_dots}",
                    f"{page_num:>3}"
                )
        except PDFNoOutlines:
            print("No outlines found.")
        except PDFSyntaxError:
            print("Corrupted PDF or non-PDF file.")
        finally:
            try:
                parser.close()
            except NameError:
                pass  # nothing to do


def main():
    # "/home/ben/Downloads/Algorithms.pdf"
    # /Randal E. Bryant, David R. O'Hallaron - Computer Systems_ A Programmer's Perspective, 2nd Edition (2010, Addison Wesley).pdf
    file_name = Path("/home/ben/Downloads/ods-python.pdf")
    parse_outlines(file_name)

    # reader = PdfReader("/home/ben/Downloads/Randal E. Bryant, David R. O'Hallaron - Computer Systems_ A Programmer's Perspective, 2nd Edition (2010, Addison Wesley).pdf")
    # page = reader.pages[37]
    # print(page.extract_text())
    # text = extract_text(file_name, page_numbers = range(38, 39))
    # print(text)

    # print('---')
    # print(m(" Bruh\nYeet\nTheIndustrialRev", 0, "Bruh Yeet"))



if __name__ == "__main__":
    main()