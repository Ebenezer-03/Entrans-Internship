# AI News Intelligence System - Setup Guide

## 🚀 Quick Start Guide

This guide will help you set up and run the **AI News Intelligence System** from scratch.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.10 or higher) - [Download here](https://www.python.org/)
- **Git** - [Download here](https://git-scm.com/)
- **Google Gemini API Key** - [Get it here](https://makersuite.google.com/app/apikey)

---

## 📦 Installation Steps

### Step 1: Clone/Navigate to Project Directory

```bash
cd "c:\Artificial Intelligence and Data Science\Task - 05"
```

### Step 2: Set Up Backend (Python/FastAPI)

#### 2.1 Navigate to backend directory
```bash
cd news_agent
```

#### 2.2 Install Python dependencies
```bash
pip install -r requirements.txt
```

**Required packages include:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `langchain-google-genai` - Gemini integration
- `langchain-community` - Vector stores
- `reportlab` & `matplotlib` - PDF generation
- `python-dotenv` - Environment variables
- `pandas` - Data handling

#### 2.3 Return to root directory
```bash
cd ..
```

### Step 3: Set Up Frontend (React)

#### 3.1 Navigate to frontend directory
```bash
cd frontend
```

#### 3.2 Install Node dependencies
```bash
npm install
```

#### 3.3 Return to root directory
```bash
cd ..
```

---

## 🔑 Configuration

### Step 1: Create Environment File

Create a file named `.env` in the **root directory** (`Task - 05/.env`):

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

**Replace** `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key.

### Step 2: Verify Configuration

The system will automatically:
- ✅ Create SQLite database (`news_agent.db`)
- ✅ Load 1,000 synthetic news articles
- ✅ Initialize Gemini 2.0 Flash
- ✅ Set up RAG vector store

---

## ▶️ Running the Application

### Option 1: Start Both Servers (Recommended)

Open **TWO separate terminal windows**:

#### Terminal 1: Backend Server
```bash
cd "c:\Artificial Intelligence and Data Science\Task - 05"
uvicorn news_agent.src.api.server:app --host 0.0.0.0 --port 8000
```

#### Terminal 2: Frontend Server
```bash
cd "c:\Artificial Intelligence and Data Science\Task - 05\frontend"
npm start
```

### Option 2: PowerShell Script (Single Command)

Create a file `start.ps1` with:
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$pwd'; uvicorn news_agent.src.api.server:app --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$pwd\frontend'; npm start"
```

Then run:
```bash
.\start.ps1
```

---

## 🌐 Accessing the Application

Once both servers are running:

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📱 Features & Usage

### 1. **Chat Agent** 🤖
- Navigate to "Chat Agent" in sidebar
- Ask questions like:
  - "What's the latest on Mars?" → RAG Search (shows sources)
  - "What is AI?" → General Chat (no sources)
- System automatically routes between RAG and Chat modes

### 2. **Dashboard** 📊
- Real-time metrics from database
- Live activity feed (updates every 3 seconds)
- Shows total articles, queries, and Gemini status
- **Download Report** button generates professional PDF

### 3. **Benchmark** 📈
- Click "Run Benchmark" to analyze database
- Shows article count and category distribution
- Displays Gemini status

### 4. **Settings** ⚙️
- Update Gemini API key
- Changes saved to both `.env` and database

---

## 🗄️ Database Information

The system uses **SQLite** (`news_agent.db`) with:

- **1,000 articles** across 7 categories:
  - Technology (142 articles)
  - Business (144 articles)
  - Sports (143 articles)
  - Politics (142 articles)
  - Science (143 articles)
  - Health (144 articles)
  - Entertainment (142 articles)

- **Query logs**: Tracks all user interactions
- **Settings**: Stores API key securely

---

## 🔧 Troubleshooting

### Issue: "Could not connect to AI agent"
**Solution**: 
1. Check if backend is running on port 8000
2. Verify API key in `.env` file
3. Restart backend server

### Issue: "No module named 'src'"
**Solution**: 
```bash
# Run backend from root directory, not from news_agent/
cd "c:\Artificial Intelligence and Data Science\Task - 05"
uvicorn news_agent.src.api.server:app --host 0.0.0.0 --port 8000
```

### Issue: Frontend won't start
**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue: "ModuleNotFoundError: matplotlib"
**Solution**:
```bash
pip install matplotlib
```

---

## 📁 Project Structure

```
Task - 05/
├── .env                          # API key configuration
├── news_agent.db                 # SQLite database
├── news_agent/                   # Backend
│   ├── src/
│   │   ├── api/
│   │   │   └── server.py        # FastAPI server
│   │   ├── rag/
│   │   │   └── rag_engine.py     # RAG + Gemini integration
│   │   ├── database.py           # SQLite functions
│   │   └── utils/
│   │       ├── data_loader.py    # Dataset generation
│   │       └── pdf_generator.py  # PDF reports
│   ├── data/
│   │   └── mdpi_news.csv         # 1,000 articles
│   └── requirements.txt
└── frontend/                     # React app
    ├── src/
    │   ├── pages/
    │   │   ├── Chat.jsx          # Chat interface
    │   │   ├── Dashboard.jsx     # Real-time dashboard
    │   │   ├── Benchmark.jsx     # Performance metrics
    │   │   └── Settings.jsx      # Configuration
    │   ├── components/
    │   │   ├── ChatWindow.jsx
    │   │   ├── RAGResults.jsx    # Clickable sources
    │   │   └── Sidebar.jsx
    │   └── api/
    │       └── client.js         # API integration
    └── package.json
```

---

## 🎯 Key Technologies

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Python 3.10 |
| **AI Model** | Google Gemini 2.0 Flash |
| **Vector Store** | FAISS (LangChain) |
| **Database** | SQLite |
| **Frontend** | React, Tailwind CSS |
| **Charts** | Matplotlib (PDF), Lucide Icons (UI) |

---

## 🚀 Production Deployment

For production deployment:

1. **Update CORS settings** in `server.py`
2. **Use environment variables** for secrets
3. **Set up reverse proxy** (nginx)
4. **Enable HTTPS**
5. **Use production database** (PostgreSQL)
6. **Add authentication**

---

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review terminal logs for errors
- Verify all dependencies are installed

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Database created (`news_agent.db` exists)
- [ ] Gemini API key configured
- [ ] Can ask questions in Chat
- [ ] Dashboard shows metrics
- [ ] Benchmark works
- [ ] PDF download works

---

**🎉 You're all set! Enjoy using the AI News Intelligence System!**

*Generated: 2025-11-27*
