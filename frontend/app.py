import streamlit as st
import plotly.graph_objects as go
from streamlit_extras.let_it_rain import rain
import base64
import sys 
import os
import requests

# --------------------------------------------------------------------------
# 1. Call backend API
# --------------------------------------------------------------------------

# Get the backend URL from the environment variable. Default to localhost for non-Docker development.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Your classes now become API clients
class EssayGrader:
    def predict_scores(self, text):
        response = requests.post(f"{BACKEND_URL}/predict_scores", json={"essay_text": text})
        return response.json()

class FeedbackGenerator:
    def generate_feedback(self, text, scores):
        response = requests.post(f"{BACKEND_URL}/generate_feedback", json={"essay_text": text, "scores": scores})
        return response.json()["feedback"]


# --------------------------------------------------------------------------
# 2. UI Configuration & Styling
# --------------------------------------------------------------------------

def setup_page():
    """Configures the page settings and metadata."""
    st.set_page_config(
        page_title="Smart Writing Coach",
        page_icon="✍️", # Using an emoji as a favicon
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'About': "The Smart Writing Coach provides AI-powered feedback for English essays."
        }
    )

def load_css():
    """Injects custom CSS for a more polished look."""
    st.markdown("""
    <style>
        /* Import Google Fonts: Lato for body, Poppins for headers */
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Poppins:wght@600&display=swap');

        /* General Styling */
        body {
            font-family: 'Lato', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .font-poppins {
            font-family: 'Poppins', sans-serif;
        }
        
        .textarea-label {
            font-size: 1.1rem !important; /* !important to override default */
            font-weight: 500;
            margin-bottom: -10px; /* Adjust spacing */
        }
        
        hr {
            height: 1px !important;
            border: none !important;
            background-color: #e1e1e1 !important;
            margin: 2rem 0 !important;
        }

        .card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.05);
            border: 1px solid #e1e1e1;
            transition: all 0.3s ease;
        }
        [data-theme="dark"] .card {
            background-color: #262730;
            border: 1px solid #444;
        }
    </style>
    """, unsafe_allow_html=True)

def get_placeholder_svg():
    """Generates a cleaner, more modern SVG for the placeholder."""
    svg_content = """
    <svg width="100%" height="100%" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
      <style>
        .text { font-family: 'Lato', sans-serif; font-size: 16px; fill: #aaa; text-anchor: middle; }
        .icon { stroke: #ccc; stroke-width: 2; fill: none; }
        .icon-fill { fill: #f8f9fa; }
        [data-theme="dark"] .icon-fill { fill: #262730; }
      </style>
      <rect width="400" height="300" fill="transparent"/>
      <path class="icon-fill" d="M120 80 H240 V220 H120 Z" rx="5" ry="5"/>
      <path class="icon" d="M120 80 H240 V220 H120 Z" rx="5" ry="5"/>
      <line class="icon" x1="135" y1="100" x2="225" y2="100" />
      <line class="icon" x1="135" y1="120" x2="225" y2="120" />
      <line class="icon" x1="135" y1="140" x2="195" y2="140" />
      <circle class="icon-fill" cx="240" cy="160" r="40"/>
      <circle class="icon" cx="240" cy="160" r="40"/>
      <line class="icon" x1="268" y1="188" x2="300" y2="220" stroke-width="4"/>
      <text x="200" y="250" class="text">Your Feedback Report Will Appear Here</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg_content.encode('utf-8')).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64_svg}"

def create_radar_chart(scores):
    """Creates a radar chart from a dictionary of scores."""
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Scores'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=False,
        height=400,
        margin=dict(l=60, r=60, t=40, b=40)
    )
    
    return fig

# --------------------------------------------------------------------------
# 3. Model & Backend Logic
# --------------------------------------------------------------------------

@st.cache_resource
def load_models():
    """Loads all necessary models and classes into memory."""
    print("INFO: Loading models and setting up classes...", file=sys.stderr)
    openai_api_key = st.secrets["OPENAI_API_KEY"] 

    grader = EssayGrader()
    feedback_gen = FeedbackGenerator(api_key=openai_api_key)
    return grader, feedback_gen


# --------------------------------------------------------------------------
# 4. Main Application UI
# --------------------------------------------------------------------------

def main():
    setup_page()
    load_css()
    
    if 'results_generated' not in st.session_state:
        st.session_state.results_generated = False
        st.session_state.scores = None
        st.session_state.feedback = None
        
    grader, feedback_gen = load_models()

    st.title("Smart Writing Coach ✍️")
    st.markdown("<p class='font-poppins'>Get AI-powered feedback on your English essays.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.2])

    with left_col:
        st.markdown("<h2 class='font-poppins'>📝 Your Essay</h2>", unsafe_allow_html=True)
        st.markdown("<p class='textarea-label'>Paste or type your essay here to begin:</p>", unsafe_allow_html=True)
        essay_text = st.text_area(
            "Paste or type your essay here to begin:",  
            label_visibility="collapsed",
            height=425,
            placeholder="Start writing..."
        )
        
        word_count = len(essay_text.strip().split()) if essay_text else 0
        st.markdown(f"<p style='text-align: right; color: #888;'>Word Count: {word_count}</p>", unsafe_allow_html=True)
        
        if st.button("Get My Feedback Report", use_container_width=True, type="primary"):
            if word_count == 0:
                st.warning("Please enter some text before getting feedback.")
            else:
                with st.spinner("Your coach is reading your essay..."):
                    st.session_state.scores = grader.predict_scores(essay_text)
                    st.session_state.feedback = feedback_gen.generate_feedback(essay_text, st.session_state.scores)
                    st.session_state.results_generated = True
        
        # Add rain emoji feature

    with right_col:
        header_text = "Feedback Report" if st.session_state.results_generated else "Marking Criteria"
        # Add explanation of criteria here
        st.markdown(f"<h2 class='font-poppins'>{header_text}</h2>", unsafe_allow_html=True)

        if st.session_state.results_generated:
            with st.container():
                st.subheader("Score Visualization")
                radar_fig = create_radar_chart(st.session_state.scores)
                st.plotly_chart(radar_fig, use_container_width=True)
                st.markdown("<hr>", unsafe_allow_html=True)
                
            with st.container():
                st.subheader("Quantitative Scores")
                score_cols = st.columns(3)
                score_items = list(st.session_state.scores.items())
                for i, (item, score) in enumerate(score_items):
                    with score_cols[i % 3]:
                        st.metric(label=item.capitalize(), value=f"{score}/10.0")
                st.markdown("<hr>", unsafe_allow_html=True)

            with st.container():
                st.subheader("Personalized Feedback")
                st.markdown(st.session_state.feedback, unsafe_allow_html=True)

            st.balloons()
        
        else:
            st.image(get_placeholder_svg(), use_container_width=True)


if __name__ == "__main__":
    main()