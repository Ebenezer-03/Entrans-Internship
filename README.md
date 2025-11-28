# AI News Intelligence System

> A full-stack AI-powered news analysis platform with intelligent query routing, RAG capabilities, and real-time analytics.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-7B5CFF.svg)](https://ai.google.dev/)

## 🌟 Features

- 🤖 **Intelligent Chat Agent**: Automatically routes between RAG search and conversational chat
- 📊 **Real-Time Dashboard**: Live metrics updating every 3 seconds
- 📈 **Performance Benchmarks**: Analyze 1,000 articles across 7 categories
- 📄 **Professional PDF Reports**: Generate comprehensive analytics reports with charts
- 🔍 **RAG System**: Retrieval-Augmented Generation with Gemini 2.0 Flash
- 💾 **SQLite Database**: Persistent storage for articles and query logs
- 🎨 **Modern UI**: Beautiful React interface with Tailwind CSS

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- Python (v3.10+)
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Install Backend Dependencies**
```bash
cd news_agent
pip install -r requirements.txt
cd ..
```

2. **Install Frontend Dependencies**
```bash
cd frontend
npm install
cd ..
```

3. **Configure API Key**

Create `.env` in root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Run the Application

**Terminal 1 - Backend:**
```bash
uvicorn news_agent.src.api.server:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Access:** [http://localhost:3000](http://localhost:3000)

## 📖 Documentation

For detailed setup instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  ← User Interface
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│  FastAPI Server │  ← Backend API
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬─────────┐
    │          │          │         │
┌───▼───┐  ┌──▼──┐  ┌───▼────┐  ┌─▼────┐
│ Gemini│  │ RAG │  │ SQLite │  │ PDF  │
│  API  │  │Store│  │   DB   │  │ Gen  │
└───────┘  └─────┘  └────────┘  └──────┘
```

## 💡 Key Technologies

| Layer | Technology |
|-------|-----------|
| AI Model | Google Gemini 2.0 Flash |
| Backend | FastAPI, Python 3.10 |
| Frontend | React, Tailwind CSS |
| Vector Store | FAISS (LangChain) |
| Database | SQLite |
| PDF Generation | ReportLab, Matplotlib |

## 📊 Database

- **1,000 synthetic news articles**
- **7 categories**: Technology, Business, Sports, Politics, Science, Health, Entertainment
- **Query logging**: Tracks all user interactions
- **Real-time metrics**: Article count, query count, category distribution

## 🎯 Usage Examples

### Chat Queries

**News Query (RAG Mode):**
```
User: "What's the latest on Mars?"
→ System retrieves NASA Mars articles
→ Shows clickable sources
```

**General Query (Chat Mode):**
```
User: "What is AI?"
→ Direct Gemini response
→ No sources needed
```

### Dashboard

- Live activity feed (updates every 3s)
- Real-time metrics from database
- Download professional PDF reports

### Benchmarks

- Analyze all 1,000 articles
- Category breakdown with counts
- System status indicators

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Gemini API key | Yes |

## 🛠️ Development

### Backend Structure
```
news_agent/
├── src/
│   ├── api/server.py           # FastAPI endpoints
│   ├── rag/rag_engine.py       # RAG + Gemini
│   ├── database.py             # SQLite operations
│   └── utils/
│       ├── data_loader.py      # Dataset generation
│       └── pdf_generator.py    # PDF reports
└── requirements.txt
```

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/                  # Main views
│   ├── components/             # Reusable components
│   └── api/client.js           # Backend integration
└── package.json
```

## 🐛 Troubleshooting

**Backend not starting?**
```bash
# Ensure you're in root directory
cd "c:\Artificial Intelligence and Data Science\Task - 05"
uvicorn news_agent.src.api.server:app --host 0.0.0.0 --port 8000
```

**Frontend errors?**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

**Missing dependencies?**
```bash
pip install matplotlib
```

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Google Gemini AI
- LangChain
- FastAPI
- React Community

---


