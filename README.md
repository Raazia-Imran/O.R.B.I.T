
````markdown
<div align="center">

<img src="./orbit_logo.svg" width="400" alt="ORBIT Logo" />

# O.R.B.I.T.
### Operational Reporting & Business Intelligence Tool

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" />
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />

<br/>

**The "Central Command" for Enterprise Data.**<br>
Transforms raw CSV logs into strategic, actionable intelligence in < 3 seconds.

[🎥 View Demo](#) · [🐛 Report Bug](#) · [🚀 Request Feature](#)

</div>

---

## 🗺️ The ORBIT Ecosystem
ORBIT is not just a dashboard; it is a **Role-Based Intelligence Hub** that routes data to the right decision-maker.

```mermaid
graph TD
    A[📂 Raw CSV Data] -->|Drag & Drop| B(🏠 Home Portal)
    B -->|Route 1| C{📈 Manager Insights}
    B -->|Route 2| D{🔬 Analyst Lab}
    B -->|Route 3| E{📜 Audit Trails}
    
    C -->|AI Agent| F[📊 Trends & Forecasts]
    C -->|AI Agent| G[⚡ Anomaly Detection]
    C -->|AI Agent| H[✉️ Auto-CEO Email]
    
    D -->|Python Engine| I[🧹 Auto-Cleaning]
    D -->|Plotly| J[📊 Correlation Matrix]
    
    C & D -->|Log Actions| K[(🗄️ Supabase DB)]
    K --> E
````

---

## 🚀 Key Modules

| Portal            | User Persona   | Key Capabilities                                                                                                                                          | Visual Vibe  |
| ----------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **01_🏠 Home**    | All Users      | • **Smart Ingestion:** Auto-samples >200MB files.<br>• **Lottie Animations:** Interactive Sci-Fi Hero.<br>• **Splash Screen:** Cinematic "Boot Sequence." | 🪐 Galactic  |
| **02_📈 Manager** | Executives     | • **3-Click AI:** Trends, Anomalies, Actions.<br>• **Voice Command:** Speak to control data.<br>• **Auto-Emailer:** Drafts professional reports.          | 💼 Strategic |
| **03_🔬 Analyst** | Data Engineers | • **One-Click Clean:** Removes duplicates/nulls.<br>• **Deep Dive:** Correlation Heatmaps.<br>• **Export:** Download cleaned datasets.                    | 🧪 Technical |
| **04_📜 Audit**   | Compliance     | • **Immutable Logs:** Tracks every AI action.<br>• **Live Stats:** Real-time user activity counter.<br>• **Search:** Filter logs by role or action.       | 🛡️ Secure   |

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

Create `.streamlit/secrets.toml` in the root directory:

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

<div align="center">

**Built for the Future of Work.**
Created with ❤️ by [Your Name]

</div>
```
