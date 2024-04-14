from PyPDF4 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color, black

from io import BytesIO

from weasyprint import HTML

from document_template import html_text1, html_text2, html_text3, html_degree_title, html_grade_card_title

# Function to add a watermark to a PDF
def create_watermarked_pdf(originalPdfFile, watermarkedPdfFile, watermark_text):
    # Create a PDF file reader for the original pdf
    pdf_reader = PdfFileReader(originalPdfFile)

    # Create a PDF writer for the 
    pdf_writer = PdfFileWriter()

    # Create a canvas for generating the watermark
    buffer = BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)
    # Set the watermark font
    cnv.setFont("Helvetica", 36)
    # Set the fill color with a low alpha for semi-transparent text for the watermark
    cnv.setFillColor(Color(black.red, black.green, black.blue, alpha=0.25))
    # Set the position of the watermark text
    cnv.drawString(125, 300, watermark_text)  
    cnv.save()

    # Revert to the beginning of the buffer since writing took the pointer to the end
    buffer.seek(0)
    # Create a new PDF reader for the watermark
    new_pdf = PdfFileReader(buffer)

    # Get the 1st page of the original PDF
    page = pdf_reader.getPage(0)
    # Merge the new_pdf i.e. watermark to the original PDF
    page.mergePage(new_pdf.getPage(0))
    # Add the merged (watermarked) PDF to PDF writer
    pdf_writer.addPage(page)

    # Write out the watermarked PDF to a file
    with open(watermarkedPdfFile, 'wb') as output_file:
        pdf_writer.write(output_file)

    return watermarkedPdfFile


def create_pdf(studentData, docType):
    name = studentData['Name']
    rollNum = studentData['Roll Number']
    pdfPath = 'pdfs/{}_{}_{}.pdf'.format(docType, name.replace(' ','_'),rollNum)
    watermarkedPdfPath = 'pdfs/watermarked_{}_{}_{}.pdf'.format(docType, name.replace(' ','_'),rollNum)

    if docType=='Degree':
        # Use HTML from weasyprint to write the html content to a PDF file
        HTML(string=html_text1+html_degree_title+html_text2.format(name, rollNum)).write_pdf(pdfPath)
    else:
        HTML(string=html_text1+html_grade_card_title+html_text3.format(
            name,
            rollNum,
            studentData['Subject 1'],
            studentData['Subject 2'],
            studentData['Subject 3'],
            studentData['Subject 4'],
            studentData['Subject 5']
        )).write_pdf(pdfPath)

    # Add a watermark to the PDF
    watermarkText = 'Institute Watermark'
    create_watermarked_pdf(pdfPath, watermarkedPdfPath, watermarkText)
    return watermarkedPdfPath
