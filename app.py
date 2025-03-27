import io
import requests
from flask import Flask, send_file, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from faker import Faker
from reportlab.lib.utils import ImageReader  # Import ImageReader

app = Flask(__name__)

# We can seed 'faker' with 'en_US' or 'de_DE' for random text generation
fake_en = Faker('en_US')
fake_de = Faker('de_DE')

@app.route("/")
def index():
    return ("<h1>Random PDF Generator</h1>"
            "<p>Try the <a href='/generate?lang=en'>/generate</a> endpoint "
            "with a 'lang' query param (en or de) for random text.</p>")

@app.route("/generate")
def generate_pdf():
    # Decide which language to use based on the query parameter; default to English
    lang = request.args.get('lang', 'en').lower()
    if lang == 'de':
        text = "\n\n".join([fake_de.text() for _ in range(4)])  # Generate 4 paragraphs
        text_after_image = "\n\n".join([fake_de.text() for _ in range(2)])  # Generate 2 paragraphs
    else:
        text = "\n\n".join([fake_en.text() for _ in range(4)])  # Generate 4 paragraphs
        text_after_image = "\n\n".join([fake_en.text() for _ in range(2)])  # Generate 2 paragraphs

    # Fetch a random image from picsum
    image_url = "https://picsum.photos/600/400"
    response = requests.get(image_url)
    image_data = response.content  # raw bytes

    # Create a PDF in memory
    pdf_buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Add text before the image
    pdf_canvas.setFont("Helvetica", 12)
    text_object = pdf_canvas.beginText(50, 780)  # Start at the top-left corner
    text_object.setTextOrigin(50, 780)
    text_object.setFont("Helvetica", 12)

    # Wrap and add the paragraphs
    for paragraph in text.split("\n\n"):
        for line in paragraph.splitlines():
            text_object.textLine(line)
        text_object.textLine("")  # Add a blank line between paragraphs

    pdf_canvas.drawText(text_object)

    # Embed the image
    img_buffer = io.BytesIO(image_data)
    img_reader = ImageReader(img_buffer)  # Process the image data
    pdf_canvas.drawImage(img_reader, 50, 400, width=4 * inch, height=3 * inch)

    # Add text after the image
    text_object = pdf_canvas.beginText(50, 380)  # Start below the image
    text_object.setFont("Helvetica", 12)

    for paragraph in text_after_image.split("\n\n"):
        for line in paragraph.splitlines():
            text_object.textLine(line)
        text_object.textLine("")  # Add a blank line between paragraphs

    pdf_canvas.drawText(text_object)

    # Finalize the PDF
    pdf_canvas.showPage()
    pdf_canvas.save()
    pdf_buffer.seek(0)

    # Return the PDF to the client
    return send_file(pdf_buffer, as_attachment=True, download_name="random.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
