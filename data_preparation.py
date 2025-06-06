import pandas as pd
import re
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Define text cleaning function
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()  # lowercase
    text = re.sub(r'\s+', ' ', text)  # remove extra whitespace
    text = re.sub(r'[^a-zA-Z0-9,.!?\'\" ]', '', text)  # keep letters, numbers, basic punctuation
    return text.strip()

# Main function to prepare the dataset
def main():
    # Load full dataset
    df = pd.read_csv("C:\\Users\\tatia\\OneDrive\\Desktop\\CODING\\smart_writing_coach\\data\\ELLIPSE_Final_github.csv\\ELLIPSE_Final_github.csv")

    # Clean the text column
    df['cleaned_text'] = df['full_text'].apply(clean_text)

    # Drop missing or invalid entries
    df = df.dropna(subset=['cleaned_text', 'Overall'])

    # Map overall scores to integer labels
    labels = sorted(df['Overall'].unique())
    label2id = {label: i for i, label in enumerate(labels)}
    df['label'] = df['Overall'].map(label2id)

    # Split dataset
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['label']
    )
    train_df, val_df = train_test_split(
        train_df, test_size=0.1, random_state=42, stratify=train_df['label']
    )

    # Save splits
    train_df.to_csv('train.csv', index=False)
    val_df.to_csv('val.csv', index=False)
    test_df.to_csv('test.csv', index=False)

    print(f"Train size: {len(train_df)}")  # 4666
    print(f"Validation size: {len(val_df)}")  # 519
    print(f"Test size: {len(test_df)}")  # 1297

    # Visualise distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x='Overall', data=train_df, order=labels)
    plt.title('Distribution of Overall Proficiency Scores (Train Set)')
    plt.xlabel('Proficiency Score')
    plt.ylabel('Number of Essays')
    plt.show()

    # Show some cleaned examples
    print(train_df[['full_text', 'cleaned_text']].head())
    print(val_df[['full_text', 'cleaned_text']].head())
    print(test_df[['full_text', 'cleaned_text']].head())


if __name__ == "__main__":
    main()
