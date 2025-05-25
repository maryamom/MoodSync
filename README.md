
# **MoodSync** 🌟  
**AI-Powered Therapeutic Environment System**  
*Winner of "Jury’s Favorite" @ Dauphine Tunis Hackathon (Dec 2024)*  
> **MoodSync** enhances therapy sessions by analyzing patient speech in real time and adapting the environment (music + lighting) to support emotional well-being. Built in **48 hours** for the *Generative AI for Good* hackathon.  
![1735137495785](https://github.com/user-attachments/assets/5306f9d5-9aae-42a8-8320-0f4577ed258c)

---

## **✨ Key Features**  
- **Real-Time Emotion Analysis**:  
  - 🎤 **Audio Agent**: OpenAI Whisper transcribes speech → GPT-4 detects emotions (e.g., sadness, anxiety) and intensity.  
  - 📝 **Session Summaries**: GPT-4 generates structured reports with emotional trends and therapeutic insights.  
- **Adaptive Environment**:  
  - 🎵 **Music Agent**: GPT-3.5 + Spotify API curates playlists based on detected emotions (e.g., calming music for anxiety).  
  - 💡 **Visual Agent**: Philips Hue SDK adjusts lighting (warm for calm, blue for melancholy) via local network.  
- **Therapist Dashboard**:  
  - 📊 Built with **Streamlit** for real-time monitoring of transcripts, emotional trends, and session history.  

---

### **Core Architecture**  

#### **1. Audio Processing Pipeline**  
- **Speech-to-Text**:  
  - Uses *OpenAI Whisper* to transcribe patient speech in real time.  
- **Emotion Analysis**:  
  - *GPT-4* processes transcribed text to detect emotions (e.g., anxiety, calm) and their intensity.  
- **Session Storage**:  
  - Structured summaries (emotional trends, key insights) are saved to *PostgreSQL* for therapist review.  

#### **2. Music Agent**  
- **Dynamic Playlists**:  
  - *GPT-3.5* converts emotion labels (e.g., "anxiety) into Spotify search queries.  
  - *Spotipy* fetches and plays matched playlists via authenticated user sessions.  

#### **3. Visual Agent**  
- **Smart Lighting**:  
  - *Philips Hue SDK* adjusts room lighting (color, brightness) based on real-time emotions:  
    - 🔵 *Blue* for melancholy, 🔶 *Warm* for calm, etc.  
  - Requires local network access to Hue Bridge.  

#### **4. Therapist Dashboard**  
- **Real-Time Monitoring**:  
  - *Streamlit* interface shows live transcripts, emotion timelines, and session history.  

---

### **Prerequisites**  
- Python 3.8+  
- OpenAI API key, Spotify Developer account, Philips Hue Bridge.  
- Libraries: `openai`, `spotipy`, `phue`, `streamlit`.  

### **Installation**  
```bash
git clone https://github.com/maryamom/MoodSync.git  
cd MoodSync  
pip install -r requirements.txt  
```  

### **Configuration**  
1. Rename `.env.example` to `.env` and add:  
   ```plaintext
   OPENAI_API_KEY="your_key"  
   SPOTIFY_CLIENT_ID="your_id"  
   SPOTIFY_CLIENT_SECRET="your_secret"  
   HUE_BRIDGE_IP="192.168.x.x"  # Local Hue Bridge IP  
   ```  

### **Run the System**  
```bash
streamlit run therapist_dashboard.py  # Launch dashboard  
python audio_agent.py                # Start real-time analysis  
```  
## **📂 Repository Structure**  
```plaintext
MoodSync/  
├── audio_agent.py          # Speech → Emotion analysis (Whisper + GPT-4)  
├── music_agent.py          # Spotify playlist generation  
├── visual_agent.py         # Philips Hue lighting control  
├── therapist_dashboard/    # Streamlit UI  
 


```
## **🎉 Acknowledgments**
 **Team**:
  
-  Fatma Gamha
- Rami Lazghab
- Ghada Dhaoui
- Molka Essid
- Aziz Dachraoui
 ```

