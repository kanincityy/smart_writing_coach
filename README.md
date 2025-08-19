# Smart Writing Coach ✍️

An AI-powered web application that provides detailed, rubric-based feedback on EFL (English as a Foreign Language) student essays. This project uses a dual-model, microservice architecture to offer both quantitative scores and qualitative, personalised advice through an interactive Streamlit interface.

---

## Architecture Overview

The Smart Writing Coach operates as a multi-container application, separating the user interface from the heavy machine learning logic for scalability and maintainability.

`[ User ] <--> [ Frontend (Streamlit on Port 8501) ] <--> [ Backend (FastAPI API on Port 8000) ] <--> [ OpenAI API ]`

-   **Frontend:** A user-friendly web interface built with Streamlit.
-   **Backend:** A powerful Python API built with FastAPI that handles the AI/ML model inference and feedback generation.

---

## Features

-   **Interactive Web Interface:** A clean UI built with Streamlit allows users to easily paste their essays and receive feedback in real-time.
-   **Live Word Counter:** Provides immediate feedback on essay length as the user types.
-   **Quantitative Analysis:** Generates scores across key writing dimensions (Cohesion, Syntax, Vocabulary, etc.) via a fine-tuned transformer model.
-   **Visual Score Report:** Displays scores in an intuitive radar chart for a quick overview of strengths and weaknesses.
-   **Qualitative Feedback:** Leverages a Large Language Model (GPT-3.5 Turbo) to generate personalised, easy-to-understand feedback.
-   **Dockerized:** The entire application is containerized with Docker, ensuring a consistent and easy setup process.

---

## Tech Stack

#### Frontend (`frontend/`)
-   **Framework:** Streamlit
-   **Data Visualization:** Plotly
-   **API Communication:** Requests

#### Backend (`backend/`)
-   **Framework:** FastAPI
-   **ML/AI:** PyTorch, Hugging Face Transformers
-   **LLM Integration:** OpenAI API

#### Orchestration
-   **Containerization:** Docker & Docker Compose

---

## Setup & Installation

This project is designed to be run with Docker. Ensure you have Docker and Docker Compose installed on your system.

**1. Clone the Repository**
```bash
git clone [https://github.com/kanincityy/smart_writing_coach.git](https://github.com/kanincityy/smart_writing_coach.git)
cd smart_writing_coach
```

**2. Set Up Your Environment File**
For local development, create a file named .env in the root of the project directory. Add your OpenAI API key to this file, replacing the placeholder text with your actual key:
```bash
OPENAI_API_KEY="YOUR_API_KEY_HERE"
The .gitignore file is already configured to keep this file private.
```

**3. Build and Run the Application**
Use Docker Compose to build the images and start the services.
```bash
docker-compose up --build
```
This command will start both the backend API and the frontend Streamlit app. It may take some time on the first run.

---

## Usage

Once the containers are running, access the Smart Writing Coach in your web browser at:

http://localhost:8501

Paste your essay into the text box and click the "Get My Feedback Report" button to receive your analysis

---

## Future Improvements

[ ] Web Interface: Build a simple web front-end (using Flask or FastAPI) to provide a more user-friendly interface.

[ ] Database Integration: Store user submissions and feedback in a database to track progress over time.

[ ] Support for More Models: Allow users to choose between different LLMs for feedback generation.

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

The core quantitative scoring model used in this project, `KevSun/Engessay_grading_ML`, is based on the research and methods presented in the following paper. A huge thank you to the authors for making their work accessible.

> Sun, K., & Wang, R. (2024). *[Automatic Essay Multi-dimensional Scoring with Fine-tuning and Multiple Regression](https://arxiv.org/abs/2406.01198)*. ArXiv.

---

### Author

**Tatiana Limonova**  
MSc Language Sciences (Technology of Language and Speech) – UCL  
[GitHub Profile](https://github.com/kanincityy) • [LinkedIn](https://linkedin.com/in/tatianalimonova)  

