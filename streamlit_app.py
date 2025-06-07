import streamlit as st
import base64
from pathlib import Path
from essay_grader import EssayGrader
from generate_feedback import FeedbackGenerator

# Page Configuration 
# Sets the title and icon that appear in your browser tab.
st.set_page_config(
    page_title="Smart Writing Coach",
    page_icon="assets/favicon.png", # Add handmade drawing as favicon
    layout="wide"
)

# Model & Class Loading (with caching for performance)
@st.cache_resource
def load_models():
    """Loads all necessary models and classes into memory."""
    print("INFO: Loading models and setting up classes...", file=st.stderr)
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    grader = EssayGrader()
    feedback_gen = FeedbackGenerator(api_key=openai_api_key)
    return grader, feedback_gen

# Load background drawings as Base64 for CSS styling.
@st.cache_data
def get_base64_of_image(file_path):
    """Encodes a local image file into Base64 for CSS background styling."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Load the models right at the start
grader, feedback_gen = load_models()

# Custom CSS for the "Revision Notes" Look
# Add these handrawn notes!!
sticky_note_bg_base64 = get_base64_of_image("assets/sticky_note_bg.png")
paper_texture_bg_base64 = get_base64_of_image("assets/paper_texture_bg.png")

app_styling = f"""
<style>
.sticky-note {{
    background-image: url("data:image/png;base64,{sticky_note_bg_base64}");
    background-size: 100% 100%; /* Stretches the image to fit the container */
    padding: 2.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
}}
.paper-texture {{
    background-image: url("data:image/png;base64,{paper_texture_bg_base64}");
    background-size: cover; /* Tries to cover the area while maintaining aspect ratio */
    padding: 2rem;
    border: 1px solid #eee;
    border-radius: 10px;
    margin-bottom: 2rem;
}}
</style>
"""
st.markdown(app_styling, unsafe_allow_html=True)


# User Interface 
# Uses hand-drawn title image instead of st.title() for a custom look
# Add title image here !!
st.image("assets/main_title_drawing.png")
st.write("---") # A simple divider

# Create a multi-column layout for the "Digital Study Desk" aesthetic
left_col, main_col = st.columns([1, 2])

with left_col:
    st.image("assets/instructions_drawing.png") # Add drawing that says "Your Essay" or "Instructions"
    essay_text = st.text_area(
        "Paste your essay here to begin:", 
        height=400, 
        placeholder="Start writing..."
    )
    
    if st.button("Get My Feedback Report ✨", use_container_width=True):
        if not essay_text.strip():
            st.warning("Please enter some text before getting feedback.")
        else:
            # Show a spinner while the AI is working its magic.
            with st.spinner("Your coach is reading your essay..."):
                scores = grader.predict_scores(essay_text)
                feedback = feedback_gen.generate_feedback(essay_text, scores)

            # Store the results in Streamlit's session state to display them
            st.session_state.results_generated = True
            st.session_state.scores = scores
            st.session_state.feedback = feedback

# Results will be displayed in the main column after the button is clicked
with main_col:
    if 'results_generated' in st.session_state:
        st.image("assets/report_title_drawing.png") # Add hand-drawn "Your Report" title
        
        # Display Quantitative Scores in a "paper texture" box
        st.markdown('<div class="paper-texture">', unsafe_allow_html=True)
        st.subheader("Quantitative Scores")
        score_cols = st.columns(3)
        score_items = list(st.session_state.scores.items())
        for i, (item, score) in enumerate(score_items):
            with score_cols[i % 3]:
                st.metric(label=item.capitalize(), value=f"{score}/10.0")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display Personalised Feedback in a "sticky note" box
        st.markdown('<div class="sticky-note">', unsafe_allow_html=True)
        st.subheader("Personalised Feedback")
        st.markdown(st.session_state.feedback) # Use markdown to render ### headings correctly
        st.markdown('</div>', unsafe_allow_html=True)

        st.success("Your report is ready!")
        st.balloons()