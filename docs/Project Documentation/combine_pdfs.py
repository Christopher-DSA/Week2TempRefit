import os
from PyPDF4 import PdfFileMerger
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

# Define a function to convert markdown to PDF.
def markdown_to_pdf(md_file, pdf_file):
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    with open(md_file, 'r') as f:
        for line in f:
            story.append(Paragraph(line, style=styles["Normal"]))
    doc.build(story)

# Get all the Markdown filenames in all subfolders.
mdFiles = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.md'):
            mdFiles.append(os.path.join(root, file))

# Convert each Markdown file to a temporary PDF.
pdfFiles = []
for mdFile in mdFiles:
    pdfFile = mdFile.replace('.md', '.pdf')
    markdown_to_pdf(mdFile, pdfFile)
    pdfFiles.append(pdfFile)

# Combine all PDFs into one file.
merger = PdfFileMerger()
for filename in pdfFiles:
    merger.append(filename)
merger.write("documentation.pdf")
merger.close()

# Clean up the temporary PDF files.
for pdfFile in pdfFiles:
    os.remove(pdfFile)

print("Documentation PDF created successfully.")
