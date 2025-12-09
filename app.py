import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import librosa # New import for structural analysis

# Assuming these modules are available in your path setup
# Adjust your sys.path.append as necessary for your project structure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# These imports must be consolidated from both scripts
try:
    from src.analysis.signal_processing import SpectralAnalyzer
    from src.analysis.mayer_metric import calculate_mayer_score
    from src.analysis.biomimetic_model import BaroreflexSimulator # Not explicitly used, but kept for completeness
    from src.generation.synthesizer import BioResonanceComposer
    from src.analysis.phrase_detector import PhraseBoundaryDetector # New import for structural analysis
except ImportError:
    st.error("Missing custom modules. Ensure your 'src' directory is correctly set up.")
    # Define placeholder classes/functions to prevent the app from crashing on import error
    class SpectralAnalyzer:
        def load_and_preprocess(self, file): return np.zeros(100)
        def extract_envelope(self, y): return np.zeros(100)
        def compute_psd(self, envelope): return np.linspace(0, 0.5, 100), np.zeros(100)
    def calculate_mayer_score(freqs, powers): return 0.0
    class BioResonanceComposer:
        def generate_therapeutic_drone(self, duration_sec, carrier_freq): return 0, np.zeros(100)
        def save_to_disk(self, audio_data, out_file): pass
    class PhraseBoundaryDetector:
        def __init__(self, sr): pass
        def detect_periodicity(self, y, min_period, max_period): return 10.0, np.linspace(0, 20, 100), np.zeros(100)


st.set_page_config(page_title="Bio-Musical Rhythms", page_icon="🫀", layout="wide")

st.title("🫀 Bio-Musical Rhythms")
st.markdown("---")

# Use three tabs to separate the original two functions and the new structural analysis
tab1, tab2 = st.tabs(["🎶 Spectrum & Composer", "🔬 Structural Analyzer"])

# --- TAB 1: Spectrum Analyzer & Therapeutic Composer (Original First Script) ---
with tab1:
    st.header("🎶 Spectral Analyzer & Therapeutic Composer")
    st.markdown("Analyze audio for **0.1 Hz Mayer Wave** resonance and generate entrainment tones.")

    tab1_sub1, tab1_sub2 = st.tabs(["📊 Analyzer", "🎹 Therapeutic Composer"])

    with tab1_sub1:
        st.markdown("**Upload existing music to test for spectral entrainment.**")
        uploaded_file_tab1 = st.file_uploader("Upload Audio (Spectral)", type=["wav", "mp3"])
        
        if uploaded_file_tab1 is not None:
            # Save file to disk
            temp_path = "temp_audio_tab1.wav"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file_tab1.getbuffer())
            
            # Process
            analyzer = SpectralAnalyzer()
            y = analyzer.load_and_preprocess(temp_path)
            envelope = analyzer.extract_envelope(y)
            freqs, powers = analyzer.compute_psd(envelope)
            score = calculate_mayer_score(freqs, powers)
            
            # Visualize
            col1, col2 = st.columns(2)
            col1.metric("Mayer Score", f"{score:.3f}")
            
            # Plot Spectrum
            st.subheader("Spectral Analysis (Envelope PSD)")
            mask = freqs <= 0.25
            df_psd = pd.DataFrame({"Freq (Hz)": freqs[mask], "Power": powers[mask]})
            fig = px.line(df_psd, x="Freq (Hz)", y="Power", title="Spectral Analysis")
            # Highlight the Mayer Wave (Baroreflex) range
            fig.add_vrect(x0=0.05, x1=0.15, fillcolor="red", opacity=0.1, annotation_text="Baroreflex Zone")
            st.plotly_chart(fig, use_container_width=True)

    with tab1_sub2:
        st.header("Algorithmic Therapy Generator")
        st.markdown("Generate a soundscape mathematically optimized for the **0.1 Hz Baroreflex** (10-second cycle).")
        
        col_a, col_b = st.columns(2)
        with col_a:
            freq = st.slider("Carrier Frequency (Hz)", 50, 440, 110, help="The pitch of the drone.")
        with col_b:
            duration = st.slider("Duration (seconds)", 30, 300, 60)
            
        if st.button("✨ Generate Bio-Resonance Audio"):
            with st.spinner("Synthesizing waveforms..."):
                composer = BioResonanceComposer()
                _, audio_data = composer.generate_therapeutic_drone(
                    duration_sec=duration, 
                    carrier_freq=freq
                )
                out_file = "generated_therapy.wav"
                composer.save_to_disk(audio_data, out_file)
                
                st.success("Audio Generated!")
                st.audio(out_file)
                
                st.subheader("Visual verification of the 10-second cycle:")
                # Downsample for plot
                viz_data = audio_data[::1000] 
                st.line_chart(viz_data)

# --- TAB 2: Structural Analyzer (Original Second Script) ---
with tab2:
    st.header("🔬 Structural Analysis (Time-Domain)")
    st.markdown("""
    **Time-Domain Autocorrelation for Structural Entrainment**
    """)
    
    with st.sidebar:
        st.markdown("---")
        st.header("Structural Analyzer Controls")
        uploaded_file_tab2 = st.file_uploader("Upload Audio (Structural)", type=["wav", "mp3"])
        
        st.markdown("---")
        st.markdown("**Tempo Modulation Test**")
        speed_factor = st.slider("Playback Speed", 0.7, 1.3, 1.0, 0.1, help="Artificially stretch audio to test if detection follows structural timing.", key="speed_factor_tab2")

    if uploaded_file_tab2:
        # Save file to disk
        temp_path = "temp_audio_tab2.wav"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file_tab2.getbuffer())
        
        y, sr = librosa.load(temp_path, sr=22050)
        
        if speed_factor != 1.0:
            y = librosa.effects.time_stretch(y, rate=speed_factor)
            st.info(f"⚡ Audio stretched by **{speed_factor}x**. Duration: {len(y)/sr:.2f}s")

        detector = PhraseBoundaryDetector(sr=sr)
        
        # Calculate target search windows based on speed factor
        target_window = 10.0 / speed_factor
        min_search = target_window * 0.5
        max_search = target_window * 1.5
        
        best_period, times, ac_norm = detector.detect_periodicity(y, min_period=min_search, max_period=max_search)
        
        # UI 
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Playback Speed", f"{speed_factor}x")
        col2.metric("Detected Cycle", f"**{best_period:.2f} s**")
        
        # Validation Logic
        expected = 10.0 / speed_factor
        is_valid = abs(best_period - expected) < 2.0
        status = "✅ Valid Entrainment" if is_valid else "⚠️ No Entrainment Detected"
        col3.metric("Entrainment Status", status)

        # VISUALIZATION
        st.subheader("Time-Domain Autocorrelation Plot")
        st.markdown("The peak shows the time lag at which the musical structure is most similar to itself (i.e., the structural cycle length).")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=ac_norm, mode='lines', name='Autocorrelation', line=dict(color='#3498db')))
        
        fig.add_vline(x=best_period, line_dash="dash", line_color="green", annotation_text=f"Peak: {best_period:.2f}s")
        
        # Highlight the target 10-second zone, adjusted for the speed factor
        fig.add_vrect(x0=9.0/speed_factor, x1=11.0/speed_factor, fillcolor="green", opacity=0.1, annotation_text="Target Zone")
        
        fig.update_layout(
            xaxis_title="Lag Time (seconds)",
            yaxis_title="Structural Correlation Strength",
            xlim=[0, 20],
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### Structural Entrainment Insight")
        st.info("""
        This time-domain analysis focuses on **structural timing** (like phrase boundaries) rather than raw volume fluctuations (spectral analysis). This method is often more robust for detecting entrainment driven by musical composition.
        """)

    else:
        st.warning("Please upload an audio file in the sidebar to begin the structural analysis.")
