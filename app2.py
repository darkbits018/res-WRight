from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('onboarding.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    skills = request.form.getlist('skills')
    work_experience = []
    education = []

    job_titles = request.form.getlist('job_title[]')
    company_names = request.form.getlist('company_name[]')
    years_worked = request.form.getlist('years_worked[]')

    degrees = request.form.getlist('degree[]')
    institutions = request.form.getlist('institution[]')
    years_attended = request.form.getlist('years_attended[]')

    for job_title, company_name, years in zip(job_titles, company_names, years_worked):
        work_experience.append([job_title, company_name, years])

    for degree, institution, years in zip(degrees, institutions, years_attended):
        education.append([degree, institution, years])

    # Print to console or handle the data as needed
    print("Name:", name)
    print("Email:", email)
    print("Phone:", phone)
    print("Skills:", skills)
    print("Work Experience:", work_experience)
    print("Education:", education)

    return "Form submitted successfully!"


if __name__ == '__main__':
    app.run(debug=True)
