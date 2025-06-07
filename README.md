# Smart Writing Coach

An AI-powered tool to provide detailed, rubric-based feedback on EFL (English as a Foreign Language) student essays. This project uses a dual-model approach to offer both quantitative scores and qualitative, personalised advice.

---

## Project Description

The Smart Writing Coach aims to bridge the gap between simple grammar checkers and human-level feedback. It's designed for English learners who want to understand the specific strengths and weaknesses of their writing across multiple dimensions. The tool first grades an essay using a fine-tuned local transformer model and then uses a powerful Large Language Model (LLM) to interpret these scores and provide encouraging, constructive feedback.

---

## Features  

- **Quantitative Analysis:** Generates scores across six key writing dimensions: Cohesion, Syntax, Vocabulary, Phraseology, Grammar, and Conventions.
- **Qualitative Feedback:** Leverages a Large Language Model (GPT-3.5 Turbo) to generate personalised, easy-to-understand feedback based on the quantitative scores.
- **Interactive:** A simple command-line interface allows a user to input their essay directly.
- **Structured Output:** Saves a detailed report containing the original essay, the scores, and the generated feedback into a web-ready JSON file.
- **Secure & Modular:** Uses best practices like .env files for API key management and a modular codebase for easy maintenance.

---

## Tech Stack

* Python 3
* PyTorch: For running the local transformer model.
* Hugging Face Transformers: To load and use the pre-trained essay grading model.
* OpenAI API: To access GPT-3.5 Turbo for feedback generation.
* python-dotenv: For managing environment variables securely.

---

## How It Works

The application follows a simple, powerful pipeline:

- **User Input:** The script prompts the user to enter their essay via the command line.
- **Quantitative Grading:** The text is passed to a locally-run Hugging Face model (KevSun/Engessay_grading_ML) which has been trained for this specific task. It returns a dictionary of scores from 1-5 for the six writing categories.
- **Prompt Engineering:** The original essay and the dictionary of scores are formatted into a detailed prompt for an LLM. The prompt instructs the LLM to act as an encouraging English teacher.
- **Qualitative Generation:** The prompt is sent to the OpenAI API (using GPT-3.5 Turbo). The LLM returns a qualitative, Markdown-formatted feedback string.
- **Save Results:** The final, combined results are saved to a timestamped JSON file in the essay_feedback/ directory.

## Setup & Installation  

1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart_writing_coach.git
cd smart_writing_coach
```
2. Create and Activate the Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or activate it (macOS/Linux)
source venv/bin/activate
```
3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set Up Your Environment File
Create a file named `.env` in the root of the project directory. Add your OpenAI API key to this file:
```bash
.env OPENAI_API_KEY='sk-YourSecretApiKeyHere'
```
The `.gitignore` file is already configured to keep this file private.

---

## Usage

With your virtual environment active, run the main script from the terminal:

```bash
python main.py
```

You will be prompted to paste your essay. After you are done typing or pasting, press Enter on an empty line to submit. The feedback will be displayed in the terminal, and a JSON file with the full results will be saved in the `writing_feedback/` directory.

--- 

## Example JSON Output

{
    "generation_timestamp_utc": "2025-06-07T10:49:00.123456",
    "student_essay": "Technology has change our lifes in many ways...",
    "quantitative_scores": {
        "cohesion": 3.0,
        "syntax": 2.5,
        "vocabulary": 3.5,
        "phraseology": 3.0,
        "grammar": 2.0,
        "conventions": 2.5
    },
    "qualitative_feedback": "### Great Start!\n\nThis is a solid effort and you've clearly explained your main points about technology. Well done!\n\n### Strengths\n\n* **Vocabulary (Score: 3.5):** You used relevant words like 'communication', 'global', and 'career' which fit the topic perfectly.\n\n### Areas for Improvement\n\n* **Grammar (Score: 2.0):** Your main area to focus on is grammar. For example, the phrase 'Technology has change our lifes' should be 'Technology has changed our lives'..."
}

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

