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
from src.analysis.phrase_detector import PhraseBoundaryDetector
from src.analysis.tempo_validation import validate_tempo_invariance

st.set_page_config(page_title="Bio-Musical Rhythms", page_icon="🫀", layout="wide")

st.title("Bio-Musical Rhythms")

def run_phrase_detection(y_p, sr_p, uploaded_file_name="Uploaded File"):
    try:
        # Assuming the necessary import is available
        from src.analysis.phrase_detector import PhraseBoundaryDetector 

        detector = PhraseBoundaryDetector(sr=sr_p)

        # Detect the period
        period, times, ac_norm = detector.detect_periodicity(
            y_p, min_period=8.0, max_period=12.0
        )

        st.success(f"✓ Analysis Complete: **{uploaded_file_name}**")

        # Display results
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Detected Period", 
                f"{period:.2f} seconds",
                help="The repetition cycle detected via time-domain autocorrelation"
            )

        with col2:
            if 9.0 <= period <= 11.0:
                st.metric(
                    "Entrainment Potential", 
                    "✓ HIGH",
                    delta="Mayer-wave compatible"
                )
                st.success("This aria has **cardiovascular entrainment potential**")
            else:
                st.metric(
                    "Entrainment Potential", 
                    "○ LOW",
                    delta=f"Off by {abs(period-10.0):.1f}s"
                )
                st.info(f"Period is {period:.1f}s (target: 9-11s)")

        with col3:
            predicted_freq = 1.0 / period if period > 0 else 0
            st.metric(
                "Frequency Equivalent",
                f"{predicted_freq:.3f} Hz",
                help="The frequency corresponding to this period"
            )

        # Plot autocorrelation
        st.subheader("Autocorrelation of Onset Envelope")
        st.markdown("""
        **How to read this:** A peak at ~10 seconds indicates strong structural repetition.
        This is the **timing-based** detection Dr. Krishna requested.
        """)
        

        df_ac = pd.DataFrame({
            "Time Lag (seconds)": times,
            "Autocorrelation": ac_norm
        })

        fig_ac = px.line(
            df_ac, 
            x="Time Lag (seconds)", 
            y="Autocorrelation",
            title="Structural Periodicity Detection"
        )

        # Highlight the target zone
        fig_ac.add_vrect(
            x0=8.0, x1=12.0, 
            fillcolor="green", 
            opacity=0.1, 
            annotation_text="Entrainment Zone (8-12s)",
            annotation_position="top left"
        )

        # Mark the detected peak
        fig_ac.add_vline(
            x=period, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Detected: {period:.2f}s"
        )

        st.plotly_chart(fig_ac, use_container_width=True)

        # Show interpretation
        st.subheader("Interpretation")
        if 9.0 <= period <= 11.0:
            st.success(f"""
            ✓ **Entrainment-Inducing Structure Detected**
            
            This aria exhibits the ~10-second phrase structure identified in Bernardi et al. (2009):
            - **Detected period:** {period:.2f} seconds
            - **Predicted cardiovascular effect:** Enhanced parasympathetic tone, increased HRV
            - **Mechanism:** Phrase-timing-driven respiratory pacing → baroreflex entrainment
            """)
        else:
            st.info(f"""
            ○ **Non-Standard Phrase Structure**
            
            This aria's {period:.2f}s period falls outside the 9-11s entrainment window:
            - May not induce Mayer-wave synchronization
            - Could still have musical/emotional effects through other mechanisms
            """)
        
        return period # Return period for validation step
    
    except Exception as e:
        st.error(f"Error during phrase detection: {e}")
        st.code(str(e))
        return None

tab1, tab2, tab3, tab4 = st.tabs(["Spectral Analyzer", "Therapeutic Composer", "Structural Analyzer", "Phrase Structure Detector"])

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
                
            _, audio_data = composer.generate_therapeutic_drone(
                duration_sec=duration, 
                carrier_freq=freq
            )
            
            out_file = "generated_therapy.wav"
            composer.save_to_disk(audio_data, out_file)
            
            st.success("Audio Generated!")
            st.audio(out_file)
            
            viz_mod_freq = mod_freq 
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
        
        if uploaded_file_s.size > 26214400:
             st.error("File is too large for reliable Spectrogram generation. Please upload a file smaller than 25MB.")
             uploaded_file_s = None # Reset the file handle to prevent further processing
          
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file_s:
                tmp_file_s.write(uploaded_file_s.getbuffer())
                temp_path_s = tmp_file_s.name
            
            try:
        
                y_s, sr_s = librosa.load(temp_path_s, sr=None)
                
                st.success(f"File loaded for structural analysis: **{uploaded_file_s.name}**")
                
                D = librosa.stft(y_s)
                S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
                
                # Create the Matplotlib figure
                fig_plt, ax = plt.subplots(figsize=(10, 4))
                img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', sr=sr_s, ax=ax)
                ax.set_title('Spectrogram (Time-Frequency View)')
                fig_plt.colorbar(img, format="%+2.f dB")
                
                st.pyplot(fig_plt)
                
            except Exception as e:
                st.error(f"Error during structural analysis: {e}")
                st.warning("This could be due to a corrupt file or a missing library dependency (like FFmpeg).")
            
            finally:
                plt.close(fig_plt)
                os.remove(temp_path_s)

with tab4:    
    st.header("Phrase Structure Detection (Time-Domain)")    
    st.markdown("""    
    **Direct timing-based detection** of the 10-second 4-phrase units mentioned by Dr. Krishna.        
    This uses **autocorrelation of the onset envelope**, not frequency analysis,     
    to detect structural periodicity in operatic arias.    
    """)        

    st.markdown("###  Quick Demo")
        
    # Map to your demo files
    demo_files = {
        "La donna è mobile (Pavarotti)": "data/demo/verdi_donna.wav",
        "Va, pensiero (Verdi)": "data/demo/verdi_va_pensiero.wav",
        "Beethoven 9th Adagio": "data/demo/beethoven_9th_adagio.wav"
    }

    demo_option = st.selectbox(
        "Or try a pre-loaded example:",
        ["None"] + list(demo_files.keys()),
        key="phrase_demo_select"
    )
    
    temp_path_p = None
    uploaded_file_p = None

    if demo_option != "None":
        st.info(f"Loading demo: {demo_option}")
                
        if demo_option in demo_files:
            demo_path = demo_files[demo_option]
                        
            if os.path.exists(demo_path):
                temp_path_p = demo_path 
                
                try:
                    y_p, sr_p = librosa.load(temp_path_p, sr=22050)
                    st.session_state["last_audio_data_p"] = (y_p, sr_p, temp_path_p, demo_option)
                    run_phrase_detection(y_p, sr_p, uploaded_file_name=demo_option)
                except Exception as e:
                    st.error(f"Could not load demo file: {e}")
            else:
                st.warning(f"Demo file not found at: {demo_path}. Please upload your own audio.")

    uploaded_file_p = st.file_uploader(
        "Upload an Operatic Aria (WAV, MP3)", 
        type=["wav", "mp3"], 
        key="phrase_uploader"
    )        

    if uploaded_file_p is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file_p:
            tmp_file_p.write(uploaded_file_p.getbuffer())
            temp_path_p = tmp_file_p.name

        try:
            y_p, sr_p = librosa.load(temp_path_p, sr=22050)
            st.session_state["last_audio_data_p"] = (y_p, sr_p, temp_path_p, uploaded_file_p.name)
            run_phrase_detection(y_p, sr_p, uploaded_file_name=uploaded_file_p.name)
            
        except Exception as e:
            st.error(f"Error during audio loading/phrase detection: {e}")
            st.code(str(e))
        finally:
            # Clean up the temp file if it was created from upload
            if temp_path_p and temp_path_p not in demo_files.values():
                os.remove(temp_path_p)
                temp_path_p = None

    # Update temp_path_p if data was successfully loaded (either by demo or upload)
    if "last_audio_data_p" in st.session_state:
        _y, _sr, temp_path_p, _name = st.session_state["last_audio_data_p"]

    # --- Tempo Validation Demonstration ---
    st.markdown("---")    
    st.subheader(" Tempo-Invariance Validation")    
    st.markdown("""    
    **Scientific proof** that our method detects **structural timing**, not spectral artifacts.        
    If we speed up the music by 1.3×, the detected period should scale to ~7.7 seconds.    
    """)        
        
    if "last_audio_data_p" in st.session_state:
        if st.button(" Run Tempo Validation Test"):        
            with st.spinner("Testing at multiple speeds..."):            
                try:                
                    from src.analysis.tempo_validation import validate_tempo_invariance                                
                    
                    # Run validation (uses temp_path_p set by the last successful load/upload)
                    df_validation = validate_tempo_invariance(
                        temp_path_p,                     
                        speed_factors=[0.8, 0.9, 1.0, 1.1, 1.2]
                    )                                
                    
                    st.success("✓ Tempo validation complete")                                
                    
                    # Display table
                    st.dataframe(df_validation, use_container_width=True)                                
                    
                    # Plot results
                    fig_val = go.Figure()                                
                    
                    fig_val.add_trace(go.Scatter(
                        x=df_validation["Speed Factor"],
                        y=df_validation["Detected Period (s)"],
                        mode='lines+markers',
                        name='Detected',
                        line=dict(color='blue', width=3)
                    ))                                
                    
                    fig_val.add_trace(go.Scatter(
                        x=df_validation["Speed Factor"],
                        y=df_validation["Expected Period (s)"],
                        mode='lines+markers',
                        name='Expected (10s baseline)',
                        line=dict(color='red', dash='dash', width=2)
                    ))                                
                    
                    fig_val.update_layout(
                        title="Tempo Invariance: Detected vs. Expected Period",
                        xaxis_title="Speed Factor",
                        yaxis_title="Period (seconds)",
                        hovermode='x unified'
                    )                                
                    

                    st.plotly_chart(fig_val, use_container_width=True)                                
                    
                    # Calculate average error
                    avg_error = df_validation["Error (s)"].mean()
                    max_error = df_validation["Error (s)"].max()                                
                    
                    if avg_error < 0.5:
                        st.success(f"""
                        ✓ **Validation Passed**
                        - Average error: {avg_error:.3f}s
                        - Maximum error: {max_error:.3f}s
                        
                        The method successfully tracks **structural timing** across tempo changes.
                        """)
                    else:
                        st.warning(f"""
                        ⚠ **High Error Detected**
                        - Average error: {avg_error:.3f}s
                        
                        The method may be picking up spurious artifacts rather than true structure.
                        """)                                
                    
                except Exception as e:                
                    st.error(f"Validation failed: {e}")
                    st.code(str(e))
    else:
        st.info("Please upload an aria or select a Quick Demo example to enable the Tempo Validation Test.")
    
