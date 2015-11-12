"""
Sample code for drawing text (or other stuff) on an existing pdf.
Also output the merged pdf.

Library used: reportlab, PyPDF2
Reference: http://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python
"""

class PDFGenerate(View):
    @staticmethod
    def generate_pdf():
        # settings.MEDIA_ROOT + '/certification_application_document/placeholder.pdf'
        pdf_template = PdfFileReader(open('placeholder.pdf', 'rb'))
        # create a file-like string object for new contents
        string = StringIO.StringIO()
        # initiate reportlab canvas object with string object
        p = canvas.Canvas(string)
        # draw text
        p.drawString(100, 100, "Hello world.")
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        # go back to the zero position
        string.seek(0)
        input_pdf = PdfFileReader(string)
        output_pdf = PdfFileWriter()
        page = pdf_template.getPage(0)
        page.mergePage(input_pdf.getPage(0))
        output_pdf.addPage(page)
        output_stream = file('destination.pdf', "wb")
        output_pdf.write(output_stream)
        output_stream.close()
