
<div align="center">

<img src="./orbit_logo.svg" width="400" alt="ORBIT Logo" />

# O.R.B.I.T.
### Operational Reporting & Business Intelligence Tool

<img src="[https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)" />
<img src="[https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)" />
<img src="[https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)" />
<img src="[https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)" />
<img src="[https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)" />

<br/>

**The "Central Command" for Enterprise Data.**<br>
Transforms raw CSV logs into strategic, actionable intelligence in < 3 seconds.

[🎥 View Demo](#) · 

</div>

---

## 🗺️ The ORBIT Ecosystem
ORBIT is not just a dashboard; it is a **Role-Based Intelligence Hub** that routes data to the right decision-maker.

* **Managers** get high-level trends and AI summaries.
* **Analysts** get cleaning tools and deep-dive statistics.
* **Auditors** get immutable logs of every action.

---

## 🚀 Key Modules

| Portal | User Persona | Key Capabilities | Visual Vibe |
| :--- | :--- | :--- | :--- |
| **01_🏠 Home** | All Users | • **Smart Ingestion:** Auto-samples >200MB files.<br>• **Lottie Animations:** Interactive Sci-Fi Hero.<br>• **Splash Screen:** Cinematic "Boot Sequence." | 🪐 Galactic |
| **02_📈 Manager** | Executives | • **3-Click AI:** Trends, Anomalies, Actions.<br>• **Voice Command:** Speak to control data.<br>• **Auto-Emailer:** Drafts professional reports. | 💼 Strategic |
| **03_🔬 Analyst** | Data Engineers | • **One-Click Clean:** Removes duplicates/nulls.<br>• **Deep Dive:** Correlation Heatmaps.<br>• **Export:** Download cleaned datasets. | 🧪 Technical |
| **04_📜 Audit** | Compliance | • **Immutable Logs:** Tracks every AI action.<br>• **Live Stats:** Real-time user activity counter.<br>• **Search:** Filter logs by role or action. | 🛡️ Secure |

---

## 🛠️ Installation & Setup

### 1. Clone & Environment
```bash
git clone https://github.com/yourusername/ORBIT.git
cd ORBIT
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Configure Secrets

Create a `.streamlit/secrets.toml` file in the root directory:

```toml
[general]
HF_API_TOKEN = "your_huggingface_token_here"
SUPABASE_URL = "your_supabase_url_here"
SUPABASE_KEY = "your_supabase_key_here"

```

### 4. Launch ORBIT 🚀

```bash
streamlit run 01_🏠_Home.py

```

---

## 🧠 Technical Architecture

### **Frontend Engine (Streamlit)**

* **Custom Design System:** Uses `utils/ui.py` to inject "Glassmorphism" cards, a neon-gradient sidebar, and the **Orbitron** sci-fi font.
* **Skeleton Loaders:** Replaces static spinners with shimmering "pulse" animations for a premium feel.
* **Splash Screen:** A custom SVG-based boot animation that runs on every session load.

### **Intelligence Engine (Hugging Face)**

* **Tiered Fallback System:**
1. *Primary:* **Phi-3 Mini** (Ultra-fast inference).
2. *Secondary:* **Gemma-2B** (Google's lightweight backup).
3. *Tertiary:* **Llama-3-8B** (Heavy-duty backup).


* **Safety:** Prompts include strict ethical guardrails against biased advice.

### **Data Engine (Pandas + Plotly)**

* **State Management:** Uses `st.session_state` to pass data between pages without reloading.
* **Visualization:** Interactive Plotly charts that support zooming and panning.

---

## 📂 Project Structure

```text
ORBIT/
├── 01_🏠_Home.py               # Landing Page & Routing
├── orbit_logo.svg              # Main Vector Logo
├── favicon.svg                 # Browser Tab Icon
├── pages/
│   ├── 02_📈_Manager_Insights.py # Executive Dashboard
│   ├── 03_🔬_Analyst_Lab.py      # Data Engineering Tools
│   └── 04_📜_Audit_Trails.py     # Database Logs
├── utils/
│   ├── ai_helper.py            # LLM API & Fallback Logic
│   ├── ui.py                   # CSS, Animations & Components
│   └── math_utils.py           # Statistical Calculations
├── modules/
│   ├── database.py             # Supabase Connection
│   └── cleaning.py             # Data Hygiene Scripts
└── requirements.txt            # Dependencies

```

---

<div align="center">

**Built for the Future of Work.**

Created with ❤️ by Raazia Imran Reshamwala, Aiza Samad, Waheeba Khan

</div>

```

```
