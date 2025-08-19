# Frontend Service: Smart Writing Coach UI

This directory contains the Streamlit-based frontend for the Smart Writing Coach application. Its purpose is to provide an interactive and user-friendly web interface for users to submit essays and view their feedback.

---

## Key Features

-   **Essay Input:** A large, clean text area for users to write or paste their essays.
-   **Real-time Updates:** A live word counter that updates as the user types.
-   **Dynamic Results Display:** A multi-tab view for feedback, featuring a Plotly radar chart for score visualization and formatted text for qualitative advice.
-   **API Client:** Communicates with the backend service to offload all heavy AI/ML processing.

---

## Tech Stack

-   **Streamlit:** For building the interactive web application.
-   **Plotly:** For creating the radar chart visualization.
-   **Requests:** For making HTTP requests to the backend API.

---

## Communication with Backend

This frontend service is a client. It does not perform any essay grading or feedback generation itself. It sends the user's essay text to the backend service (defined by the `BACKEND_URL` environment variable) and displays the JSON response it receives.

---

## Running Standalone (for Development)

While this service is designed to be run with Docker Compose, you can run it as a standalone Streamlit app for development, provided the backend service is running separately.

1.  **Navigate to this directory:**
    ```bash
    cd app
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
4.  **Run the app:**
    ```bash
    # You may need to set the BACKEND_URL environment variable
    # if the backend is not running on http://localhost:8000
    streamlit run app.py
    ```