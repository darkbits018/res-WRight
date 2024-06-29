import os
from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

# Configure the API key
genai.configure(api_key=os.getenv('GENERATIVE_AI_API_KEY'))


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)
        resume_file = request.files['resume']
        if resume_file.filename == '':
            return redirect(request.url)
        resume_path = "uploads/" + resume_file.filename
        resume_file.save(resume_path)

        # Extract text from the uploaded resume
        resume_text = extract_text_from_pdf(resume_path)

        # Define the prompt for professional rewriting
        prompt = """
        Please rewrite the following resume in a professional and polished manner, using strong action verbs and emphasizing relevant skills and achievements. Ensure the format is clean and suitable for a job application.

        Here is the resume text:
        """ + resume_text

        # Initialize the GenerativeModel
        model = genai.GenerativeModel()

        # Generate content based on the combined input
        response = model.generate_content(prompt)

        # Return the rewritten resume text
        return render_template('result.html', rewritten_resume=response.text)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
