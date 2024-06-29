import google.generativeai as genai
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

load_dotenv()
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


# Path to the PDF file
pdf_path = "resume.pdf"

# Extract text from the PDF
resume_text = extract_text_from_pdf(pdf_path)

# Define the prompt
prompt = """Please rewrite the following resume in a professional and polished manner, using strong action verbs and 
emphasizing relevant skills and achievements. Ensure the format is clean and suitable for a job application. Here is the resume text:
"""

# Combine the prompt and the resume text
combined_input = prompt + "\n\n" + resume_text

# Initialize the GenerativeModel
model = genai.GenerativeModel()

# Generate content based on the combined input
response = model.generate_content(combined_input)

# Print the response
print(response.text)
