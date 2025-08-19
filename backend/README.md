 Backend Service: Smart Writing Coach API 🧠

This directory contains the FastAPI backend service for the Smart Writing Coach application. It handles all AI/ML model inference for essay grading and communicates with the OpenAI API to generate qualitative feedback.

---

## API Endpoints

This service exposes the following endpoints:

### 1. Predict Scores
-   **Endpoint:** `POST /predict_scores`
-   **Description:** Receives essay text and returns quantitative scores across six writing dimensions.
-   **Request Body:**
    ```json
    {
      "essay_text": "Your essay text goes here..."
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "Cohesion": 4.5, "Syntax": 4.0, "Vocabulary": 5.0,
      "Phraseology": 4.0, "Grammar": 4.5, "Conventions": 4.5
    }
    ```

### 2. Generate Feedback
-   **Endpoint:** `POST /generate_feedback`
-   **Description:** Receives essay text and scores, then returns personalised, qualitative feedback from an LLM.
-   **Request Body:**
    ```json
    {
      "essay_text": "Your essay text...",
      "scores": { "Cohesion": 4.5, "Syntax": 4.0, ... }
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "feedback": "### Great Work! Your writing is very clear..."
    }
    ```
---

## Tech Stack

-   **Framework:** FastAPI
-   **Server:** Uvicorn
-   **ML/AI:** PyTorch, Hugging Face Transformers
-   **LLM Integration:** OpenAI API

---

## Running Standalone (for Development)

While this service is designed to be run with Docker Compose, you can run it as a standalone API for development.

1.  **Navigate to this directory:**
    ```bash
    cd src
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Or .\venv\Scripts\Activate.ps1 on Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your `.env` file** in the project's root directory.

5.  **Run the Uvicorn server:**
    ```bash
    uvicorn main:app --reload
    ```
The API will be available at `http://127.0.0.1:8000`.