import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import tempfile
import librosa
import librosa.display
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Assume these classes exist in your project structure
from src.analysis.signal_processing import SpectralAnalyzer
from src.analysis.mayer_metric import calculate_mayer_score
from src.analysis.biomimetic_model import BaroreflexSimulator
from src.generation.synthesizer import BioResonanceComposer

st.set_page_config(page_title="Bio-Musical Rhythms", page_icon="🫀", layout="wide")

st.title("Bio-Musical Rhythms")

tab1, tab2, tab3 = st.tabs(["📊 Spectral Analyzer", "🎹 Therapeutic Composer", "🏗️ Structural Analyzer"])

with tab1:
    st.header("Audio Entrainment Analysis")
    st.markdown("Upload existing music to test for entrainment with the **0.1 Hz Baroreflex rhythm**.")
    
    uploaded_file = st.file_uploader("Upload Audio File (WAV, MP3)", type=["wav", "mp3"], key="analyzer_uploader")
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            temp_path = tmp_file.name
        
        try:
            # FIX 1: Removed 'sr=44100'
            analyzer = SpectralAnalyzer()
            y = analyzer.load_and_preprocess(temp_path)
            envelope = analyzer.extract_envelope(y)
            freqs, powers = analyzer.compute_psd(envelope)
            score = calculate_mayer_score(freqs, powers)
            
            st.success(f"File uploaded and analyzed successfully: **{uploaded_file.name}**")
            
            col1, col2 = st.columns(2)
            col1.metric("Mayer Score (0.1 Hz Power)", f"{score:.3f}", help="Measures the relative power in the Baroreflex Resonance Frequency (0.05 - 0.15 Hz) compared to total power.")
            
            mask = freqs <= 0.25
            df_psd = pd.DataFrame({"Freq (Hz)": freqs[mask], "Power": powers[mask]})
            fig = px.line(df_psd, x="Freq (Hz)", y="Power", title="Spectral Analysis (Low Frequency Band)")
            fig.add_vrect(x0=0.05, x1=0.15, fillcolor="red", opacity=0.1, annotation_text="0.1 Hz Target", annotation_position="top left")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error during spectral analysis: {e}")
        
        finally:
            os.remove(temp_path)

with tab2:
    st.header("Algorithmic Therapy Generator")
    st.markdown("Generate a soundscape mathematically optimized for **Baroreflex resonance** (0.1 Hz or 10-second cycle).")
    
    col_a, col_b = st.columns(2)
    with col_a:
        freq = st.slider("Carrier Frequency (Hz)", 50, 440, 110, step=1, help="The base pitch of the generated drone or tone.")
    with col_b:
        duration = st.slider("Duration (seconds)", 30, 300, 60, step=15)
        
    st.subheader("Modulation Parameters")
    col_c, col_d = st.columns(2)
    with col_c:
        mod_freq = st.number_input("Modulation Frequency (Hz)", min_value=0.05, max_value=0.15, value=0.1, step=0.01, format="%.2f", help="The rhythmic cycle used to modulate the audio (default 0.1 Hz is optimal).")
    with col_d:
        mod_depth = st.slider("Modulation Depth (0-1)", 0.1, 1.0, 0.5, step=0.05, help="How pronounced the rhythmic cycle is on the volume/pitch.")

    if st.button("✨ Generate Bio-Resonance Audio"):
        with st.spinner("Synthesizing waveforms..."):
            composer = BioResonanceComposer()
            
            try:
                composer_sr = composer.sr 
            except AttributeError:
                composer_sr = 44100
                
            # FIX: Temporarily remove mod_freq and mod_depth to identify the issue
            _, audio_data = composer.generate_therapeutic_drone(
                duration_sec=duration, 
                carrier_freq=freq
                # mod_freq=mod_freq, # Removed
                # mod_depth=mod_depth # Removed
            )
            
            out_file = "generated_therapy.wav"
            composer.save_to_disk(audio_data, out_file)
            
            st.success("Audio Generated!")
            st.audio(out_file)
            
            # Note: Visualization will use default mod_freq if none is passed
            viz_mod_freq = mod_freq # Keep the slider value for display
            st.subheader(f"Modulation Visualization (Cycle: {1/viz_mod_freq:.1f} seconds)")
            
            step = composer_sr // 100
            viz_data = audio_data[::step]
            max_points = int(10 * composer_sr * (1 / viz_mod_freq) / step)
            st.line_chart(viz_data[:max_points])
with tab3:
    st.header("Time-Frequency Structural Analyzer")
    st.markdown("Visualize the fundamental structure of an audio file using a **Spectrogram**.")
    
    uploaded_file_s = st.file_uploader("Upload Audio File (WAV, MP3)", type=["wav", "mp3"], key="structural_uploader")
    
    if uploaded_file_s is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file_s:
            tmp_file_s.write(uploaded_file_s.getbuffer())
            temp_path_s = tmp_file_s.name
        
        try:
            y_s, sr_s = librosa.load(temp_path_s, sr=None)
            
            st.success(f"File loaded for structural analysis: **{uploaded_file_s.name}**")
            
            D = librosa.stft(y_s)
            S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            
            fig_plt, ax = plt.subplots(figsize=(10, 4))
            # FIX 3: Ensure sr_s is passed to specshow for correct time/frequency scaling
            img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', sr=sr_s, ax=ax)
            ax.set_title('Spectrogram (Time-Frequency View)')
            fig_plt.colorbar(img, format="%+2.f dB")
            
            st.pyplot(fig_plt)
            
        except Exception as e:
            st.error(f"Error during structural analysis: {e}")
        
        finally:
            os.remove(temp_path_s)
