# import streamlit as st
# from JD_Resume import JobDescriptionHandler, ResumeHandler, EmbeddingSimilarityCalculator

# import streamlit as st
# from PIL import Image
# import json

# # Initialize the handlers (make sure to define the methods called here)
# job_description_handler = JobDescriptionHandler()
# resume_handler = ResumeHandler()
# similarity_calculator = EmbeddingSimilarityCalculator()

# # Function to save keywords to a JSON file


# def save_keywords_to_json(keywords, filename):
#     with open(filename, 'w') as f:
#         json.dump(keywords, f)


# # Title of the app
# st.title('Job Match Application')

# # Sidebar for Job Description
# st.sidebar.header('Job Description (JD)')
# jd_file = st.sidebar.file_uploader("Upload your JD", type=['pdf'])
# jd_text = st.sidebar.text_area("Or paste your JD here")

# # Sidebar for Resume
# st.sidebar.header('Resume')
# resume_file = st.sidebar.file_uploader("Upload your resume", type=['pdf'])
# resume_text = st.sidebar.text_area("Or paste your resume here")

# # If files are uploaded, process them
# if jd_file is not None or jd_text is not '':
#     jd_data = job_description_handler.process_job_description(
#         jd_file if jd_file is not None else jd_text)
#     jd_keywords = job_description_handler.job_description_keyword(
#         jd_data)  # Replace with actual method
#     jd_embedding = job_description_handler.embed_job_description(jd_data)

# if resume_file is not None or resume_text is not '':
#     resume_data = resume_handler.process_resume(
#         resume_file if resume_file is not None else resume_text)
#     resume_keywords = resume_handler.resume_keyword(
#         resume_data)  # Replace with actual method
#     resume_embedding = resume_handler.embed_resume_description(resume_data)

# # Display keywords and allow exporting to JSON
# if 'jd_keywords' in locals():
#     st.write('JD Keywords:', jd_keywords)
#     if st.button('Export JD Keywords to JSON'):
#         save_keywords_to_json(jd_keywords, 'jd_keywords.json')
#         st.success('JD Keywords exported to jd_keywords.json')

# if 'resume_keywords' in locals():
#     st.write('Resume Keywords:', resume_keywords)
#     if st.button('Export Resume Keywords to JSON'):
#         save_keywords_to_json(resume_keywords, 'resume_keywords.json')
#         st.success('Resume Keywords exported to resume_keywords.json')

# # Calculate and display similarity score
# if 'jd_embedding' in locals() and 'resume_embedding' in locals():
#     similarity_score = similarity_calculator.compute_similarity(
#         jd_embedding, resume_embedding)
#     st.write('Similarity Score:', similarity_score)
import streamlit as st
from JD_Resume import JobDescriptionHandler, ResumeHandler, EmbeddingSimilarityCalculator
import json
import os

# Initialize the handlers
job_description_handler = JobDescriptionHandler()
resume_handler = ResumeHandler()
similarity_calculator = EmbeddingSimilarityCalculator()

# Function to save keywords to a JSON file


# def save_keywords_to_json(keywords, filename):
#     with open(filename, 'w') as f:
#         json.dump(keywords, f)


def save_keywords_to_json(keywords, filename):
    # Folder path
    folder_path = 'Data/Keywords'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Complete file path
    file_path = os.path.join(folder_path, filename)

    # Write the JSON data to the file
    with open(file_path, 'w') as f:
        json.dump(keywords, f)

# Title of the app
st.title('Job Match Application')

# Create columns for Job Description and Resume side by side
col1, col2 = st.columns(2)

# Column for Job Description
with col1:
    st.header('Job Description')
    jd_file = st.file_uploader("Upload your JD.pdf", type=[
                               'pdf'], key="jd_uploader")
    jd_text = st.text_area("Or paste your JD here", key="jd_textarea")
    if jd_file or jd_text:
        jd_data = job_description_handler.process_job_description(
            jd_file if jd_file else jd_text)
        jd_keywords = job_description_handler.job_description_keyword(jd_data)
        jd_embedding = job_description_handler.embed_job_description(jd_data)
        st.write('Keywords for the JD:', jd_keywords)
        if st.button('Export JD Keywords to JSON', key='jd_export'):
            save_keywords_to_json(jd_keywords, 'jd_keywords.json')
            st.success('JD Keywords exported to jd_keywords.json')

# Column for Resume
with col2:
    st.header('Resume')
    resume_file = st.file_uploader("Upload your resume.pdf", type=[
                                   'pdf'], key="resume_uploader")
    resume_text = st.text_area(
        "Or paste your resume here", key="resume_textarea")
    if resume_file or resume_text:
        resume_data = resume_handler.process_resume(
            resume_file if resume_file else resume_text)
        resume_keywords = resume_handler.resume_keyword(resume_data)
        resume_embedding = resume_handler.embed_resume(resume_data)
        st.write('Keywords for the candidate resume:', resume_keywords)
        if st.button('Export Resume Keywords to JSON', key='resume_export'):
            save_keywords_to_json(resume_keywords, 'resume_keywords.json')
            st.success('Resume Keywords exported to resume_keywords.json')

# Calculate and display similarity score
# if 'jd_embedding' in locals() and 'resume_embedding' in locals():
#     similarity_score = similarity_calculator.compute_similarity(
#         jd_embedding, resume_embedding)
#     st.metric(label='Similarity Score', value=f"{similarity_score:.2f}")

# Assuming you might want a button to compute the match score, place it outside of columns
if st.button('Compute Match Score'):
    if 'jd_embedding' in locals() and 'resume_embedding' in locals():
        similarity_score = similarity_calculator.compute_similarity(
            jd_embedding, resume_embedding)
        st.metric(label='Match Score', value=f"{similarity_score:.2f}")
