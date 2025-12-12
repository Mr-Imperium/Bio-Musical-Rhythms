
import os
import re
import json
import yt_dlp
import os
import re
import json
import yt_dlp

def parse_raw_list(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    entries = []
    # Regex captures standard and shorts URLs
    url_pattern = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtube\.com/shorts/|youtu\.be/)([\w-]+))'
    time_pattern = r'(\d{1,2}:\d{2})'
    
    for line in lines:
        line = line.strip()
        if not line: continue
        url_match = re.search(url_pattern, line)
        if not url_match:
            # Skip bing redirects or messy text
            continue
        full_url = url_match.group(1)
        video_id = url_match.group(2)
        start_time = None
        time_match = re.search(time_pattern, line)
        if time_match:
            t_str = time_match.group(1)
            parts = t_str.split(':')
            start_time = int(parts[0]) * 60 + int(parts[1])
        entries.append({"url": full_url, "id": video_id, "start_time": start_time, "source": "Mentor List"})
    return entries

def get_extra_songs():
    return [
        {"url": "https://www.youtube.com/watch?v=zqNTltOGh5c", "id": "jazz_so_what", "source": "Self (Jazz)", "start_time": None},
        {"url": "https://www.youtube.com/watch?v=fNFzfwLM72c", "id": "disco_stayin_alive", "source": "Self (Disco)", "start_time": None},
        {"url": "https://www.youtube.com/watch?v=CvFH_6DNRCY", "id": "debussy_clair", "source": "Self (Classical)", "start_time": None},
        {"url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ", "id": "queen_rhapsody", "source": "Self (Rock)", "start_time": None},
        {"url": "https://www.youtube.com/watch?v=4pkS7b4DQPE", "id": "mozart_k448", "source": "Self (Mozart)", "start_time": None}
    ]

def sanitize_filename(name, fallback_id):
    # Replace anything that isn't a word char, space, or hyphen with nothing, then clean up spaces.
    sanitized = re.sub(r'[^\w\s-]', '', name).strip()
    sanitized = re.sub(r'\s+', '_', sanitized)
    # If the title was empty or only special characters, fall back to a sanitized ID
    if not sanitized:
        sanitized = re.sub(r'\W+', '_', fallback_id)
    return sanitized

def download_batch(entries, output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    metadata_catalog = []
    seen_ids = set()
    print(f"🚀 Processing {len(entries)} entries...")
    
    # Initialize a YDL instance for fetching metadata (download=False)
    ydl_info_opts = {'quiet': True, 'no_warnings': True}
    
    with yt_dlp.YoutubeDL(ydl_info_opts) as ydl_info:
        for entry in entries:
            vid_id = entry['id']
            if vid_id in seen_ids: continue
            seen_ids.add(vid_id)
            
            # --- STEP 1: Get metadata (Title) without downloading ---
            title = 'Unknown'
            try:
                # Fetch metadata
                info = ydl_info.extract_info(entry['url'], download=False)
                title = info.get('title', 'Unknown')
            except Exception as e:
                print(f"❌ Error getting metadata for {vid_id}: {e}")
                continue
            
            # --- STEP 2: Determine filename based on sanitized title ---
            safe_title = sanitize_filename(title, vid_id)
            
            # The final .wav file path and template, based on the better, title-derived name
            out_template = os.path.join(output_dir, f"{safe_title}.%(ext)s")
            final_wav = os.path.join(output_dir, f"{safe_title}.wav")

            # --- STEP 3: Define download options and perform download ---
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': out_template, 
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'wav','preferredquality': '192'}],
               
                'quiet': True, 'no_warnings': True
            }
            
            # Handling timestamps and duration limits (same as before)
            args = []
            if entry['start_time']:
                args = ['-ss', str(entry['start_time']), '-t', '180']
            else:
                args = ['-t', '300'] # Max 5 mins
            ydl_opts['postprocessor_args'] = args

            try:
                # Need a new YDL instance for download to apply the specific outtmpl for this video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                    ydl_download.download([entry['url']])
                    
                # The catalog entry now uses the predictable, title-based file_path
                metadata_catalog.append({"id": vid_id, "title": title, "category": entry['source'], "file_path": final_wav})
                print(f"✅ {title}")
            except Exception as e:
                print(f"❌ Error downloading {vid_id} ('{title}'): {e}")
                
    return metadata_catalog

if __name__ == "__main__":
    mentor_data = parse_raw_list("data/raw_mentor_list.txt")
    extra_data = get_extra_songs()
    catalog = download_batch(mentor_data + extra_data)
    with open("data/verification_cohort.json", "w") as f:
        json.dump(catalog, f, indent=4)
    print("Done.")

