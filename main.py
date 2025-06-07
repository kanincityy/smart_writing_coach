import json
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from essay_grader import EssayGrader
from generate_feedback import FeedbackGenerator

# Define the output directory
OUTPUT_DIR = Path("essay_feedback")

# Load environment variables from .env file
print("Loading environment variables...", file=sys.stderr)
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found. Make sure it's set in your .env file.", file=sys.stderr)
    exit(1) # Exit the script if the key is missing
else:
    masked_key = OPENAI_API_KEY[:5] + "..." + OPENAI_API_KEY[-4:]
    print(f"OpenAI API Key loaded (masked): {masked_key}", file=sys.stderr)

def setup_modules():
    """Initialises and returns the grader and feedback generator modules."""
    print("Initialising modules... (This might take a moment)")
    try:
        grader = EssayGrader()
        feedback_gen = FeedbackGenerator(api_key=OPENAI_API_KEY)
        print("Modules loaded successfully. Ready to begin.", file=sys.stderr)
        return grader, feedback_gen
    except Exception as e:
        print(f"Critical Error: Failed to initialise modules: {e}", file=sys.stderr)
        print("Please check your environment setup and try again.", file=sys.stderr)
        return None, None

def get_user_input() -> str:
    """Prompts the user to enter their essay and returns it as a string."""
    print("\n" + "="*50)
    print("Please enter your essay below.")
    print("When you are finished, press Enter on an empty line.")
    print("="*50)

    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
            
    return "\n".join(lines)

def run_analysis(grader, feedback_gen, essay_text):
    """Runs the grading and feedback generation pipeline."""
    print("\nGrading the essay with the local model...", file=sys.stderr)
    rubric_scores = grader.predict_scores(essay_text)
    if not rubric_scores:
        print("Warning: Could not generate rubric scores.", file=sys.stderr)
        print("Please ensure your essay is well-formed and try again.", file=sys.stderr)
        return None, None # Return None if scoring fails

    print("Generating personalised feedback with GPT-3.5 Turbo...")
    qualitative_feedback = feedback_gen.generate_feedback(essay_text, rubric_scores)
    if "Error:" in qualitative_feedback:
        print("Warning: Could not generate qualitative feedback.", file=sys.stderr)
        print("Please check your essay and try again.", file=sys.stderr)
        return rubric_scores, None # Return scores but no feedback

    return rubric_scores, qualitative_feedback

def save_results(output_data: dict):
    """Saves the final output data to a timestamped JSON file."""
    # Create the output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate a unique filename using the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"feedback_{timestamp}.json"
    file_path = OUTPUT_DIR / filename

    print("\n" + "="*50)
    print(f"Saving results to: {file_path}", file=sys.stderr)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)
        print(f"Successfully saved the complete feedback.", file=sys.stderr)
    except IOError as e:
        print(f"Error: Could not save results to file: {e}", file=sys.stderr)

def main():
    """Main function to orchestrate the entire process."""
    grader, feedback_gen = setup_modules()
    if not all([grader, feedback_gen]):
        return # Exit if modules failed to load

    student_essay = get_user_input()
    if not student_essay.strip():
        print("\nNo text was entered. Exiting program.", file=sys.stderr)
        print("Please try again with a valid essay.", file=sys.stderr)
        return

    print("\nThank you! Processing your essay...", file=sys.stderr)
    rubric_scores, qualitative_feedback = run_analysis(grader, feedback_gen, student_essay)

    # Display Final User Feedback
    print("\n" + "="*50)
    print("Here is your complete feedback!")
    print("="*50)
    if rubric_scores:
        print("\n### Your Quantitative Scores:\n")
        for item, score in rubric_scores.items():
            print(f"- {item.capitalize()}: {score}/10.0")
    
    if qualitative_feedback:
        print("\n### Personalised Feedback:\n")
        print(qualitative_feedback)
    print("\n" + "="*50)

    # Structure and Save the Output 
    final_output = {
        "generation_timestamp_utc": datetime.now().isoformat(),
        "student_essay": student_essay,
        "quantitative_scores": rubric_scores,
        "qualitative_feedback": qualitative_feedback
    }
    save_results(final_output)

if __name__ == "__main__":
    main()