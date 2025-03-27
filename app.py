import io
import requests
from flask import Flask, send_file, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from faker import Faker

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
        text = fake_de.text()
    else:
        text = fake_en.text()

    # Fetch a random image from picsum (you could also use Unsplash or other services)
    image_url = "https://picsum.photos/600/400"
    response = requests.get(image_url)
    image_data = response.content  # raw bytes

    # Create a PDF in memory
    pdf_buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Add text
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(50, 780, "Random PDF Generator")
    pdf_canvas.drawString(50, 760, f"Language: {lang}")
    text_lines = text.split('\n')
    y_position = 740
    for line in text_lines:
        pdf_canvas.drawString(50, y_position, line)
        y_position -= 15

    # Embed the image
    # First, write the downloaded image to an in-memory buffer
    # Note: For certain image formats, we might need to use PIL to decode properly,
    # but if the response is a jpeg from picsum, this simple approach works.
    img_buffer = io.BytesIO(image_data)
    # let's place the image below the text
    pdf_canvas.drawImage(img_buffer, 50, 400, width=4*inch, height=3*inch)

    # finalize
    pdf_canvas.showPage()
    pdf_canvas.save()
    pdf_buffer.seek(0)

    # Return the PDF to the client
    return send_file(pdf_buffer, as_attachment=True, download_name="random.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
