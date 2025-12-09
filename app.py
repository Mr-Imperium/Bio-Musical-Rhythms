
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.analysis.signal_processing import SpectralAnalyzer
from src.analysis.mayer_metric import calculate_mayer_score
from src.analysis.biomimetic_model import BaroreflexSimulator
from src.generation.synthesizer import BioResonanceComposer

st.set_page_config(page_title="Bio-Musical Rhythms", page_icon="🫀", layout="wide")

st.title("Bio-Musical Rhythms")

tab1, tab2 = st.tabs(["📊 Analyzer", "🎹 Therapeutic Composer"])

with tab1:
    st.markdown("**Upload existing music to test for entrainment.**")
    uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
    
    if uploaded_file is not None:
        # --- FIX STARTS HERE ---
        # Use tempfile to create a guaranteed-to-exist temporary file path 
        # that is properly handled by the operating system.
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # Write the uploaded file buffer to the temporary file
            tmp_file.write(uploaded_file.getbuffer())
            temp_path = tmp_file.name # Get the unique path to the temp file
        
        try:
            # Process using the guaranteed temporary path
            analyzer = SpectralAnalyzer()
            y = analyzer.load_and_preprocess(temp_path) # Pass the unique path
            envelope = analyzer.extract_envelope(y)
            freqs, powers = analyzer.compute_psd(envelope)
            score = calculate_mayer_score(freqs, powers)
            
            # Visualize
            col1, col2 = st.columns(2)
            col1.metric("Mayer Score", f"{score:.3f}")
            
            # Plot Spectrum
            mask = freqs <= 0.25
            df_psd = pd.DataFrame({"Freq (Hz)": freqs[mask], "Power": powers[mask]})
            fig = px.line(df_psd, x="Freq (Hz)", y="Power", title="Spectral Analysis")
            # Note: 0.05-0.15 Hz is the VLF range for heart rate variability, 
            # often associated with baroreflex and entrainment.
            fig.add_vrect(x0=0.05, x1=0.15, fillcolor="red", opacity=0.1) 
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
            st.warning("Ensure the uploaded file is a valid, uncorrupted WAV or MP3 file.")
        
        finally:
            # Crucially, delete the temporary file after processing to clean up the system
            os.remove(temp_path)
        # --- FIX ENDS HERE ---

with tab2:
    st.header("Algorithmic Therapy Generator")
    st.markdown("Generate a soundscape mathematically optimized for the 0.1 Hz Baroreflex.")
    
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
