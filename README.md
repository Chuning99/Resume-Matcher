[![Resume Matcher + Hacktoberfest](Assets/img/Hacktoberfest_banner.png)](https://github.com/srbhr/Resume-Matcher/issues)

[![Resume Matcher](Assets/img/header_image.png)](https://www.resumematcher.fyi)

<div align="center">

# Resume Matcher

## How does it work?

</div>

The Resume Matcher takes your resume and job descriptions as input, parses them using Python, and mimics the functionalities of an ATS, providing you with insights and suggestions to make your resume ATS-friendly.

The process is as follows:

1. **Parsing**: The system uses Python to parse both your resume and the provided job description, just like an ATS would.

2. **Keyword Extraction**: The tool uses advanced machine learning algorithms to extract the most relevant keywords from the job description. These keywords represent the skills, qualifications, and experiences the employer seeks.

3. **Key Terms Extraction**: Beyond keyword extraction, the tool uses textacy to identify the main key terms or themes in the job description. This step helps in understanding the broader context of what the resume is about.

4. **Vector Similarity Using Qdrant**: The tool uses [Qdrant](https://github.com/qdrant/qdrant), a highly efficient vector similarity search tool, to measure how closely your resume matches the job description. The more similar they are, the higher the likelihood that your resume will pass the ATS screening.

<br/>

<div align="center">

## How to install

</div>

Follow these steps to set up the environment and run the application.

1. Fork the repository [here](https://github.com/srbhr/Resume-Matcher/fork).

2. Clone the forked repository.

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/Resume-Matcher.git
   cd Resume-Matcher
   ```

3. Create a Python Virtual Environment:

   - Using [virtualenv](https://learnpython.com/blog/how-to-use-virtualenv-python/):

     _Note_: Check how to install virtualenv on your system here [link](https://learnpython.com/blog/how-to-use-virtualenv-python/).

     ```bash
     virtualenv env
     ```

   **OR**

   - Create a Python Virtual Environment:

     ```bash
     python -m venv env
     ```

4. Activate the Virtual Environment.

   - On Windows.

     ```bash
     env\Scripts\activate
     ```

   - On macOS and Linux.

     ```bash
     source env/bin/activate
     ```

    **OPTIONAL (For pyenv users)**

5. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Prepare Data:

   - Resumes: Place your resumes in PDF format in the `Data/Resumes` folder. Remove any existing contents in this folder.
   - Job Descriptions: Place your job descriptions in PDF format in the `Data/JobDescription` folder. Remove any existing contents in this folder.

7. Run the Application:

   ```python
   run on the jupyter notebook
   ```
   ```

**Note**: For local versions, you do not need to run "streamlit_second.py" as it is specifically for deploying to Streamlit servers.

**Additional Note**: The Vector Similarity part is precomputed to optimize performance due to the resource-intensive nature of sentence encoders that require significant GPU and RAM resources. If you are interested in leveraging this feature in a Google Colab environment for free, refer to the upcoming blog (link to be provided) for further guidance.


### Running the Web Application

The full stack Next.js (React and FastAPI) web application allows users to interact with the Resume Matcher tool interactively via a web browser.

To run the full stack web application (frontend client and backend api servers), follow the instructions over on the [webapp README](/webapp/README.md) file.

<br/>

### Cohere and Qdrant

1.  Visit [Cohere website registration](https://dashboard.cohere.ai/welcome/register) and create an account.
2.  Go to API keys and copy your cohere api key.
3.  Visit [Qdrant website](https://cloud.qdrant.io/) and create an account.
4.  or use `docker pull qdrant/qdrant` to pull the docker image.
5.  After run docker, version is `API Key` and url is `localhost:6333`
6.  Get your api key and cluster url.
7.  Go to open dashboard in qdrant and enter your api key **for only the first time**

<img src="Assets/img/quadrant_cloud.png" height="60%" width="60%"/>

6.  Now create a yaml file named config.yml in Scripts/Similarity/ folder. 
7.  The format for the conifg file should be as below:
    ```yaml
    cohere:
      api_key: cohere_key
    qdrant:
      api_key: qdrant_api_key
      url: qdrant_cluster_url
    ```
8.  Please replace your values without any quotes.

9. For the Vertex API, please floow the instuction on the official website. [Vertex API](https://cloud.google.com/vertex-ai/docs/predictions/custom-container-automl-models)
10. For the Chatgpt part, please go to openAI website to get the api key. [OpenAI](https://beta.openai.com/)


*Note: Please make sure that Qdrant_client's version is higher than v1.1*
