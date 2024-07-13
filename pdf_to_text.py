from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Input and output file names
input_pdf = 'RACETECH-SUSPENSION-BIBLE.pdf'
output_pdf = 'extracted_text.pdf'

# Create a PDF reader object
reader = PdfReader(input_pdf)

# Create a PDF writer object
writer = PdfWriter()

# Print number of pages in the input PDF file
print(f"Total number of pages: {len(reader.pages)}")

# Loop through all pages, extract text, and create new pages with the extracted text
for page_num in range(len(reader.pages)):
    # Extract text from the current page
    page = reader.pages[page_num]
    text = page.extract_text()
    
    print(f"\n--- Page {page_num + 1} ---")
    print(text)
    
    # Create a new PDF page with the extracted text
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)
    
    # Split the text into lines and write them to the new page
    y = 750  # Start from the top of the page
    for line in text.split('\n'):
        can.drawString(50, y, line)
        y -= 12  # Move to the next line
        if y < 50:  # If we're near the bottom of the page, start a new page
            can.showPage()
            can.setFont("Helvetica", 10)
            y = 750
    
    can.save()
    
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    
    # Add the new page to the writer
    writer.add_page(new_pdf.pages[0])

# Save the new PDF with extracted text
with open(output_pdf, "wb") as output_file:
    writer.write(output_file)

print(f"\nExtracted text has been saved to {output_pdf}")