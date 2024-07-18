from flask import Flask, render_template, request, redirect, url_for, send_file
import google.generativeai as genai
import fitz  # PyMuPDF
import os
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
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
        original_resume_text = extract_text_from_pdf(resume_path)

        # Define the prompt for professional rewriting
        prompt = """
        Please rewrite the following resume in a professional and polished manner, using strong action verbs and emphasizing relevant skills and achievements. Ensure the format is clean and suitable for a job application.

        Here is the original resume text:
        """ + original_resume_text

        # Initialize the GenerativeModel
        model = genai.GenerativeModel()

        # Generate content based on the combined input
        response = model.generate_content(prompt)

        # Save rewritten resume text to a variable
        rewritten_resume_text = response.text

        # Render template with both original and rewritten resumes
        return render_template('result.html', original_resume=resume_path, rewritten_resume=rewritten_resume_text)

    return render_template('upload.html')


# @app.route('/onboarding', methods=['GET', 'POST'])
# def onboard_user():
#     if request.method == 'GET':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         skills = request.form.getlist('skills')
#         work_experience = []
#         education = []
#
#         job_titles = request.form.getlist('job_title[]')
#         company_names = request.form.getlist('company_name[]')
#         years_worked = request.form.getlist('years_worked[]')
#
#         degrees = request.form.getlist('degree[]')
#         institutions = request.form.getlist('institution[]')
#         years_attended = request.form.getlist('years_attended[]')
#
#         for job_title, company_name, years in zip(job_titles, company_names, years_worked):
#             work_experience.append([job_title, company_name, years])
#
#         for degree, institution, years in zip(degrees, institutions, years_attended):
#             education.append([degree, institution, years])
#
#         # Print to console or handle the data as needed
#         print("Name:", name)
#         print("Email:", email)
#         print("Phone:", phone)
#         print("Skills:", skills)
#         print("Work Experience:", work_experience)
#         print("Education:", education)
#
#         return "Form submitted successfully!"
#
#     return render_template('onboarding.html')

@app.route('/onboard_user', methods=['GET'])
def onboard_user():
    return render_template('onboarding.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    skills = request.form.getlist('skills')
    github = request.form.get('github')
    linkedin = request.form.get('linkedin')

    work_experiences = []
    job_titles = request.form.getlist('job_title[]')
    company_names = request.form.getlist('company_name[]')
    years_worked = request.form.getlist('years_worked[]')
    for title, company, years in zip(job_titles, company_names, years_worked):
        work_experiences.append(f"{title} at {company} ({years} years)")

    education = []
    degrees = request.form.getlist('degree[]')
    institutions = request.form.getlist('institution[]')
    years_attended = request.form.getlist('years_attended[]')
    for degree, institution, years in zip(degrees, institutions, years_attended):
        education.append(f"{degree} from {institution} ({years} years)")

    data_sentences = [
        f"My name is {name}, my contact info is {email}, {phone}, GitHub: {github}, LinkedIn: {linkedin}.",
        f"My work experiences are: {', '.join(work_experiences)}.",
        f"My education includes: {', '.join(education)}."
    ]
    # Convert data_sentences list to a single string
    data_sentences_str = "\n".join(data_sentences)

    # Define the prompt for professional rewriting
    prompt = f""" Using the information given, please create a professional resume using strong action verbs and also 
    include a career objective or professional summary based on the work experience in 5 sentences.While writing 
    bullet points for workexperinces instead of writing generic description use technical terms based on the year o 
    experience  in the role.List out the skills in an organized way. the whole file should be in jason format

       Here is the information text:
       {data_sentences_str}
       """
    # Replace multiple newlines with single newline
    prompt = " ".join(prompt.splitlines())

    print(prompt)

    # Initialize the GenerativeModel
    model = genai.GenerativeModel()

    # Generate content based on the combined input
    response = model.generate_content(prompt)

    # Save rewritten resume text to a variable
    rewritten_resume_text = response.text

    # Print to console or handle the data as needed
    # print("Name:", name)
    # print("Email:", email)
    # print("Phone:", phone)
    # print("Skills:", skills)
    # print("Work Experience:", work_experience)
    # print("Education:", education)
    print(rewritten_resume_text)

    # return render_template('onboardResult.html', rewritten_resume_text=rewritten_resume_text)
    return "Form submitted successfully!"



if __name__ == '__main__':
    app.run(debug=True)
