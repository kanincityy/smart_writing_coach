import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class EssayGrader:
    """
    A class to load an essay grading model and predict scores for a given text.
    """
    def __init__(self, model_name: str = "KevSun/Engessay_grading_ML"):
        """
        Initializes the EssayGrader by loading the model and tokenizer.

        Args:
            model_name (str): The name of the model on the Hugging Face Hub.
        """
        # Note: The model and tokenizer are from the same repository "KevSun/Engessay_grading_ML"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.item_names = ["cohesion", "syntax", "vocabulary", "phraseology", "grammar", "conventions"]
        self.model.eval()

    def predict_scores(self, text: str) -> dict[str, float]:
        """
        Predicts rubric-based scores for the input essay text.

        Args:
            text (str): The essay text to be graded.

        Returns:
            dict[str, float]: A dictionary mapping rubric items to their predicted scores.
        """
        if not text.strip():
            return {item: 0.0 for item in self.item_names}

        # Tokenize the input text
        encoded_input = self.tokenizer(
            text, 
            return_tensors='pt', 
            padding=True, 
            truncation=True, 
            max_length=512 # Increased max_length for essays
        )

        # Perform inference
        with torch.no_grad():
            outputs = self.model(**encoded_input)

        # Process the predictions
        predictions = outputs.logits.squeeze().numpy()
        
        # Scale predictions from 1 to 5, as per typical essay rubrics
        scaled_scores = predictions
        
        # Round scores to the nearest 0.5
        rounded_scores = [round(score * 2) / 2 for score in scaled_scores]

        # Create a dictionary of scores
        scores = {item: round(score, 1) for item, score in zip(self.item_names, rounded_scores)}
        
        return scores

if __name__ == '__main__':
    # This block runs only when the script is executed directly
    print("Initializing the essay grader...")
    grader = EssayGrader()
    print("Grader ready.")

    # Prompt the student to enter text
    print("\nType your text (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    new_text = "\n".join(lines)
    
    if not new_text.strip():
        print("No text entered. Exiting.")
    else:
        # Get the predicted scores
        predicted_scores = grader.predict_scores(new_text)
        print("\n--- Predicted Scores ---")
        for item, score in predicted_scores.items():
            print(f"{item}: {score:.1f}")

        # Optionally, save the scores to a file
        try:
            with open("predicted_scores.txt", "w") as f:
                f.write("--- Predicted Scores ---\n")
                for item, score in predicted_scores.items():
                    f.write(f"{item}: {score:.1f}\n")
            print("\nScores saved to predicted_scores.txt")
        except IOError as e:
            print(f"\nError saving scores to file: {e}")