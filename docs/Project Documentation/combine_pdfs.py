import glob
import os
from PyPDF2 import PdfReader

# Get all the PDF filenames.
pdfFiles = []
for filename in glob.glob('*.pdf'):
    pdfFiles.append(filename)

print(pdfFiles)

#combine all pdfs in the folder into one file
from PyPDF2 import PdfMerger


merger = PdfMerger()

for filename in pdfFiles:
    merger.append(filename)

merger.write("documentation.pdf")
merger.close()

