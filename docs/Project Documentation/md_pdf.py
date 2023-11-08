import markdown
import pdfkit
import os
from PyPDF2 import PdfMerger

def markdown_to_pdf(directory_path):
    # Get all markdown files in the directory
    markdown_files = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    # Initialize a PdfMerger object
    merger = PdfMerger()

    for markdown_file in markdown_files:
        markdown_file_path = os.path.join(directory_path, markdown_file)
        pdf_file_path = os.path.join(directory_path, markdown_file.replace('.md', '.pdf'))

        # Read the markdown file
        with open(markdown_file_path, 'r') as f:
            text = f.read()

        # Convert markdown to html
        html = markdown.markdown(text)

        # Add a style tag to change the font
        html = '<style>body { font-family: Arial, sans-serif; letter-spacing: 0.2em;}</style>' + html

        # Convert html to pdf
        pdfkit.from_string(html, pdf_file_path)

        # Add the pdf to the merger
        merger.append(pdf_file_path)

    # Write all the files into one pdf
    merger.write(os.path.join(directory_path, 'combined.pdf'))
    merger.close()


# Call the function with the path to your directory
markdown_to_pdf('docs\Project Documentation\markdown')





