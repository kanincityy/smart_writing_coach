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
      "scores": { "Cohesion": 4.5, "Syntax": 4.0, ... },
      "teacher_type": "You can now choose between 3 teacher personalities via the frontend!"
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
-   **Containerisation** Docker
-   **Dependency Management** uv (saved my life honestly)

---

## Running the Service

This service is designed to be run via Docker Compose from the project root:

1. **Build and start all services:**
```bash
    docker-compose up --build
```

2. **Set up your `.env` file** in the project root before running.

The API will be available at `http://localhost:8000`.