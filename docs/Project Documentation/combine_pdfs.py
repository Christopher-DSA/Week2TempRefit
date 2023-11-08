import glob
from PyPDF4 import PdfFileMerger

# Get all the PDF filenames.
pdfFiles = []
for filename in glob.glob("*.pdf"):
    pdfFiles.append(filename)

print(pdfFiles)

# combine all pdfs in the folder into one file
merger = PdfFileMerger()

for filename in pdfFiles:
    merger.append(filename)

merger.write("documentation.pdf")
merger.close()
