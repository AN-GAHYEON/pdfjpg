import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import zipfile

# Function to convert PDF page to JPG
def pdf_page_to_jpg(pdf_page):
    # Render PDF page to an image
    pix = pdf_page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

# Function to convert a list of images to a ZIP file
def images_to_zip(images, filenames):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for img, filename in zip(images, filenames):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            zip_file.writestr(filename, img_byte_arr.read())
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit app
st.title("PDF to JPG Converter")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Load the PDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    # List to store images and filenames
    images = []
    filenames = []

    # Iterate through PDF pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        img = pdf_page_to_jpg(page)
        
        # Store the image and filename
        images.append(img)
        filenames.append(f"page_{page_num + 1}.jpg")

    # Create and download ZIP file
    if images:
        zip_buffer = images_to_zip(images, filenames)
        st.download_button(
            label="Download All Pages as ZIP",
            data=zip_buffer,
            file_name="pages.zip",
            mime="application/zip"
        )
