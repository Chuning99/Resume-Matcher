from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scripts.parsers.ParseResumeToJson import ParseResume
import json
import os
from typing import List
import networkx as nx
import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from annotated_text import annotated_text, parameters
from streamlit_extras import add_vertical_space as avs
from streamlit_extras.badges import badge
from scripts.similarity import get_similarity_score, find_path, read_config
from scripts.utils import get_filenames_from_dir
from scripts import ReadPdf, JobDescriptionProcessor, ResumeProcessor, KeytermsExtraction
import cohere
from scripts.KeytermsExtraction import KeytermExtractor
from scripts.similarity.get_similarity_score import get_similarity_score
import uuid
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scripts.parsers.ParseJobDescToJson import ParseJobDesc
from scripts.parsers.ParseResumeToJson import ParseResume
from pypdf import PdfReader


def read_single_pdf(file_like_object) -> str:
    """
    Read a single PDF file from an in-memory file-like object and extract the text from each page.

    Args:
        file_like_object: An in-memory file-like object representing the PDF file.

    Returns:
        str: A string containing the extracted text from the PDF file.
    """
    output = []
    try:
        pdf_reader = PdfReader(file_like_object)
        for page in pdf_reader.pages:
            output.append(page.extract_text())
    except Exception as e:
        print(f"Error reading PDF file: {str(e)}")
    return " ".join(output)

class JobDescriptionHandler:
    def __init__(self, job_desc_directory="Data/JobDescription/"):
        self.job_desc_directory = job_desc_directory

    def read_pdf(self, file_path):
        # Assuming ReadPdf.read_single_pdf is a function that reads PDF and returns text
        return read_single_pdf(file_path)


    def process_job_description(self, input_data):
        # Check if the input is an uploaded file
        if hasattr(input_data, 'name') and input_data.name.endswith('.pdf'):
            # Handle as a PDF file
            job_desc_text = self.read_pdf(input_data)
            #job_desc_processor = JobDescriptionProcessor(job_desc_text)
            job_desc_processor = ParseJobDesc(job_desc_text).get_JSON()
        else:
            # Handle as text input
            job_desc_text = input_data
            job_desc_processor = ParseJobDesc(job_desc_text).get_JSON()

       #job_desc_processed = job_desc_processor._read_job_desc()
        return job_desc_processor
    # def process_job_description(self, input_data):
    #     # Process input data (PDF file path or text) and return processed job description
    #     if input_data.endswith('.pdf'):
    #         # Handle as a PDF file
    #         # job_desc_processor = JobDescriptionProcessor(input_data)
    #         job_desc_processor = JobDescriptionProcessor(input_data)
    #         #job_desc_processed = job_desc_processor._read_job_desc()
    #     else:
    #         # Handle as text input
    #         job_desc_text = input_data
    #         job_desc_processor = ParseJobDesc(job_desc_text).get_JSON()

    #     job_desc_processed = job_desc_processor._read_job_desc()
    #     return job_desc_processed

    def embed_job_description(self, job_desc_text):
        embeddings = HuggingFaceEmbeddings()
        job_desc_embedding = embeddings.embed_documents(
            [job_desc_text['bi_grams']])
        return job_desc_embedding

    def job_description_keyword(self, job_desc_text):
        return job_desc_text['bi_grams']
    def process_all_job_descriptions(self):
        # Process all job descriptions in the directory
        job_files = [f for f in os.listdir(self.job_desc_directory)
                     if os.path.isfile(os.path.join(self.job_desc_directory, f))]

        job_processed = []
        for job_file in job_files:
            job_processor = JobDescriptionProcessor(job_file)
            job_data = job_processor._read_job_desc()
            job_processor._write_json_file(job_data)
            job_processed.append(job_data)
        return job_processed


class ResumeHandler:
    def __init__(self, resumes_directory="Data/Resumes/"):
        self.resumes_directory = resumes_directory

    def read_pdf(self, file_path):
        # Assuming ReadPdf.read_single_pdf is a function that reads PDF and returns text
        return read_single_pdf(file_path)

    def process_resume(self, input_data):
        # Process input data (PDF file path or text) and return processed resume
        if input_data.endswith('.pdf'):
            # Handle as a PDF file
            resume_processor = ResumeProcessor(input_data)
            print("into this if loop")
        else:
            # Handle as text input
            resume_text = input_data
            resume_processor = ParseResume(resume_text).get_JSON()

        # Process the resume text
        # resume_processor = ResumeProcessor(resume_text)
        resume_data = resume_processor._read_resumes()
        return resume_data

    def process_resume(self, input_data):
        # Check if the input is an uploaded file
        if hasattr(input_data, 'name') and input_data.name.endswith('.pdf'):
            # Handle as a PDF file
            resume_text = self.read_pdf(input_data)
            # job_desc_processor = JobDescriptionProcessor(job_desc_text)
            resume_processor = ParseResume(resume_text).get_JSON()
        else:
            # Handle as text input
            resume_text= input_data
            resume_processor = ParseJobDesc(resume_text).get_JSON()
        return resume_processor
    
    def resume_keyword(self, resume_text):
        return resume_text['bi_grams']
    def process_all_resumes(self):
        # Process all resumes in the directory
        resume_files = [f for f in os.listdir(self.resumes_directory)
                        if os.path.isfile(os.path.join(self.resumes_directory, f))]

        resumes_processed = []
        for resume_file in resume_files:
            resume_processor = ResumeProcessor(resume_file)
            resume_data = resume_processor._read_resumes()
            resume_processor._write_json_file(resume_data)
            resumes_processed.append(resume_data)
        return resumes_processed

    def embed_resume_description(self, resume_text):
        embeddings = HuggingFaceEmbeddings()
        resume_embedding = embeddings.embed_documents(
            [resume_text['bi_grams']])
        return resume_embedding


class EmbeddingSimilarityCalculator:
    def __init__(self):
        pass

    def flatten_embedding(self, embedding):
        if embedding.ndim > 2:
            return embedding.reshape(1, -1)
        return embedding

    def compute_similarity(self, embedding1, embedding2) -> float:
        # Ensure embeddings are numpy arrays and flatten them
        embedding1 = self.flatten_embedding(np.array(embedding1))
        embedding2 = self.flatten_embedding(np.array(embedding2))

        similarity = cosine_similarity(embedding1, embedding2)[0][0]
        return similarity


