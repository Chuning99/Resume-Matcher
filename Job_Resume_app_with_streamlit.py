import streamlit as st
from JD_Resume import JobDescriptionHandler, ResumeHandler, EmbeddingSimilarityCalculator

# # Initialize your handlers
# job_handler = JobDescriptionHandler()
# resume_handler = ResumeHandler()
# similarity_calculator = EmbeddingSimilarityCalculator()

# st.title("Resume and Job Description Matcher")

# st.header("Upload Job Description")
# job_desc_file = st.file_uploader(
#     "Choose a Job Description file", type=['pdf','txt'])

# st.header("Upload Resume")
# resume_file = st.file_uploader("Choose a Resume file", type=['pdf', 'txt'])

# if st.button('Process and Compare'):
#     if job_desc_file is not None and resume_file is not None:
#         # Process Job Description
#         processed_job_desc = job_handler.process_job_description(job_desc_file)
#         job_desc_embedding = job_handler.embed_job_description(
#             processed_job_desc)

#         # Process Resume
#         processed_resume = resume_handler.process_resume(resume_file)
#         resume_embedding = resume_handler.embed_resume_description(
#             processed_resume)

#         # Calculate Similarity
#         similarity_score = similarity_calculator.compute_similarity(
#             job_desc_embedding, resume_embedding)
#         st.write(f"Similarity Score: {similarity_score}")
#     else:
#         st.error("Please upload both a job description and a resume.")

# # if st.button('Process and Compare'):
# #     if job_desc_file is not None and resume_file is not None:
# #         # Process Job Description
# #         job_desc_text = job_handler.read_pdf(job_desc_file) if job_desc_file.name.endswith(
# #             '.pdf') else job_desc_file.getvalue().decode()
# #         processed_job_desc = job_handler.process_job_description(job_desc_text)
# #         job_desc_embedding = job_handler.embed_job_description(
# #             processed_job_desc)

# #         # Process Resume
# #         resume_text = resume_handler.read_pdf(resume_file) if resume_file.name.endswith(
# #             '.pdf') else resume_file.getvalue().decode()
# #         processed_resume = resume_handler.process_resume(resume_text)
# #         resume_embedding = resume_handler.embed_resume_description(
# #             processed_resume)

# #         # Calculate Similarity
# #         similarity_score = similarity_calculator.compute_similarity(
# #             job_desc_embedding, resume_embedding)
# #         st.write(f"Similarity Score: {similarity_score}")
# #     else:
# #         st.error("Please upload both a job description and a resume.")
import streamlit as st
from PIL import Image
import json

# Initialize the handlers (make sure to define the methods called here)
job_description_handler = JobDescriptionHandler()
resume_handler = ResumeHandler()
similarity_calculator = EmbeddingSimilarityCalculator()

# Function to save keywords to a JSON file


def save_keywords_to_json(keywords, filename):
    with open(filename, 'w') as f:
        json.dump(keywords, f)


# Title of the app
st.title('Job Match Application')

# Sidebar for Job Description
st.sidebar.header('Job Description (JD)')
jd_file = st.sidebar.file_uploader("Upload your JD", type=['pdf'])
jd_text = st.sidebar.text_area("Or paste your JD here")

# Sidebar for Resume
st.sidebar.header('Resume')
resume_file = st.sidebar.file_uploader("Upload your resume", type=['pdf'])
resume_text = st.sidebar.text_area("Or paste your resume here")

# If files are uploaded, process them
if jd_file is not None or jd_text is not '':
    jd_data = job_description_handler.process_job_description(
        jd_file if jd_file is not None else jd_text)
    jd_keywords = job_description_handler.job_description_keyword(
        jd_data)  # Replace with actual method
    jd_embedding = job_description_handler.embed_job_description(jd_data)

if resume_file is not None or resume_text is not '':
    resume_data = resume_handler.process_resume(
        resume_file if resume_file is not None else resume_text)
    resume_keywords = resume_handler.resume_keyword(
        resume_data)  # Replace with actual method
    resume_embedding = resume_handler.embed_resume_description(resume_data)

# Display keywords and allow exporting to JSON
if 'jd_keywords' in locals():
    st.write('JD Keywords:', jd_keywords)
    if st.button('Export JD Keywords to JSON'):
        save_keywords_to_json(jd_keywords, 'jd_keywords.json')
        st.success('JD Keywords exported to jd_keywords.json')

if 'resume_keywords' in locals():
    st.write('Resume Keywords:', resume_keywords)
    if st.button('Export Resume Keywords to JSON'):
        save_keywords_to_json(resume_keywords, 'resume_keywords.json')
        st.success('Resume Keywords exported to resume_keywords.json')

# Calculate and display similarity score
if 'jd_embedding' in locals() and 'resume_embedding' in locals():
    similarity_score = similarity_calculator.compute_similarity(
        jd_embedding, resume_embedding)
    st.write('Similarity Score:', similarity_score)
