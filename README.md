# Financial Document Analyzer - Complete Solution

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.3-green.svg)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.130.0-orange.svg)](https://crewai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive financial document analysis system powered by AI that processes corporate reports, financial statements, and investment documents to provide professional investment insights and risk assessments.

## 🚀 Features

- **AI-Powered Analysis**: Uses CrewAI framework with specialized financial analyst agents
- **PDF Document Processing**: Extracts and analyzes text from financial PDFs
- **Investment Recommendations**: Provides detailed buy/sell/hold recommendations
- **Risk Assessment**: Comprehensive risk analysis and mitigation strategies
- **RESTful API**: Easy-to-use FastAPI endpoints for document upload and analysis
- **Professional Output**: Structured, institutional-quality financial reports
- **Real-time Processing**: Instant analysis with progress tracking

## 🔧 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   CrewAI Agents  │    │   Analysis      │
│   Web Server    │────│   Financial      │────│   Reports       │
│                 │    │   Analyst        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        │                       │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Upload    │    │   Document       │    │   Investment    │
│   & Processing  │────│   Processing     │────│   Insights      │
│                 │    │   Tools          │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🐛 Bugs Found and Fixed

### Critical Issues Resolved:

#### 1. **Missing Core Components**
- **Problem**: `agents.py` file was missing but referenced in imports
- **Fix**: Created comprehensive agents with proper CrewAI configuration
- **Impact**: System couldn't start without agent definitions

#### 2. **Broken PDF Processing**
- **Problem**: `tools.py` referenced undefined `Pdf` class
- **Fix**: Implemented proper PDF text extraction using PyPDF2
- **Impact**: Core functionality was completely broken

#### 3. **Async/Sync Mismatch**
- **Problem**: Tools defined as `async` but called synchronously
- **Fix**: Converted to synchronous methods with proper error handling
- **Impact**: Runtime errors during task execution

#### 4. **Terrible Task Prompts**
- **Problem**: Tasks encouraged hallucination and contradictory responses
- **Original**: "Maybe solve the user's query or something else that seems interesting"
- **Fixed**: Professional, structured prompts with clear deliverables
- **Impact**: Unreliable, unprofessional analysis results

#### 5. **Missing Environment Setup**
- **Problem**: No validation for required API keys
- **Fix**: Added environment validation and proper error messages
- **Impact**: Silent failures and confusing errors

#### 6. **Poor Error Handling**
- **Problem**: Generic exception handling without logging
- **Fix**: Comprehensive error handling with detailed logging
- **Impact**: Difficult to debug issues in production

#### 7. **File Management Issues**
- **Problem**: No file validation, poor cleanup, no size checks
- **Fix**: Proper file validation, secure cleanup, and size monitoring
- **Impact**: Security vulnerabilities and resource leaks

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Serper API key (for web search)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/financial-document-analyzer.git
cd financial-document-analyzer
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here

# Optional Configuration
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

### Step 5: Create Data Directory
```bash
mkdir data
```

### Step 6: Add Sample Document (Optional)
Download Tesla's Q2 2025 financial update from:
https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf

Save it as `data/sample.pdf` for testing.

## 🚀 Usage

### Starting the Server
```bash
python main.py
```

The API will be available at:
- **Main URL**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### API Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "Financial Document Analyzer API is running",
  "status": "healthy",
  "version": "1.0.0"
}
```

#### 2. Detailed Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "data_directory": true,
  "required_env_vars": {
    "OPENAI_API_KEY": true,
    "SERPER_API_KEY": true
  }
}
```

#### 3. Document Analysis
```http
POST /analyze
```
**Parameters:**
- `file` (UploadFile): PDF financial document
- `query` (str, optional): Specific analysis question

**Example Response:**
```json
{
  "status": "success",
  "query": "Analyze Tesla's financial performance and investment potential",
  "analysis": "# Financial Analysis Report\n\n## Executive Summary\n...",
  "file_processed": "TSLA-Q2-2025-Update.pdf",
  "file_size": 2048576,
  "processing_id": "uuid-string"
}
```

### Usage Examples

#### cURL
```bash
# Basic analysis
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@path/to/financial-document.pdf"

# With specific query
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@path/to/financial-document.pdf" \
  -F "query=What are the key investment risks and opportunities?"
```

#### Python Client
```python
import requests

def analyze_document(file_path, query=None):
    url = "http://localhost:8000/analyze"
    
    files = {"file": open(file_path, "rb")}
    data = {"query": query} if query else {}
    
    response = requests.post(url, files=files, data=data)
    return response.json()

# Example usage
result = analyze_document(
    "financial-report.pdf", 
    "Analyze the company's debt levels and liquidity position"
)
print(result["analysis"])
```

#### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function analyzeDocument(filePath, query) {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    if (query) form.append('query', query);
    
    const response = await axios.post('http://localhost:8000/analyze', form, {
        headers: form.getHeaders()
    });
    
    return response.data;
}

// Example usage
analyzeDocument('./financial-report.pdf', 'Investment recommendation')
    .then(result => console.log(result.analysis));
```

## 📊 Analysis Output Structure

The system provides structured, professional financial analysis reports:

### Executive Summary
- Overall investment recommendation (Buy/Hold/Sell)
- Key findings and highlights
- Risk rating and confidence level

### Financial Performance Analysis
- Revenue trends and growth analysis
- Profitability metrics and margins
- Cash flow assessment
- Balance sheet evaluation

### Investment Analysis
- Valuation metrics and fair value estimation
- Growth prospects and competitive advantages
- Dividend policy and shareholder returns
- Portfolio allocation recommendations

### Risk Assessment
- Financial risks (leverage, liquidity, credit)
- Operational and market risks
- ESG considerations
- Risk mitigation strategies

### Market Context
- Industry comparison and positioning
- Economic factors and market conditions
- Regulatory environment impact

## 🛠️ Development

### Project Structure
```
financial-document-analyzer/
├── main.py                 # FastAPI application and endpoints
├── agents.py               # CrewAI agent definitions
├── task.py                 # Analysis tasks and prompts
├── tools.py                # PDF processing and analysis tools
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── README.md              # This file
├── data/                  # Upload directory
├── logs/                  # Application logs
└── tests/                 # Test files
```

### Adding New Features

#### Custom Analysis Agents
```python
# In agents.py
new_analyst = Agent(
    role='Sector Specialist',
    goal='Provide industry-specific analysis',
    backstory='Expert in specific financial sectors...',
    tools=[custom_tool],
    verbose=True
)
```

#### Custom Analysis Tasks
```python
# In task.py
custom_task = Task(
    description="Perform specialized analysis...",
    expected_output="Structured report with...",
    agent=new_analyst,
    tools=[analysis_tools]
)
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Code Quality
```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .
```

## 🔧 Configuration

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for language model |
| `SERPER_API_KEY` | Yes | Serper API key for web search |
| `LOG_LEVEL` | No | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_FILE_SIZE` | No | Maximum upload file size in bytes |

### Customizing Analysis
Edit `task.py` to modify analysis focus:
- Financial metrics emphasis
- Risk assessment criteria
- Investment recommendation parameters
- Output format and structure

## 📈 Performance and Scaling

### Current Limitations
- Synchronous processing (single request at a time)
- In-memory file processing
- No persistent storage of results

### Scaling Solutions

#### 1. Queue Worker Model (Bonus Implementation)
```python
# requirements.txt additions
redis==4.5.4
celery==5.2.7

# Implementation
from celery import Celery

celery_app = Celery(
    'financial_analyzer',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379'
)

@celery_app.task
def analyze_document_async(file_path, query):
    return run_crew(query, file_path)

# Usage in FastAPI
@app.post("/analyze-async")
async def analyze_async(file: UploadFile, query: str = None):
    # Save file and queue task
    task = analyze_document_async.delay(file_path, query)
    return {"task_id": task.id, "status": "processing"}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = analyze_document_async.AsyncResult(task_id)
    return {"status": task.status, "result": task.result}
```

#### 2. Database Integration (Bonus Implementation)
```python
# requirements.txt additions
sqlalchemy==2.0.12
alembic==1.10.3
psycopg2-binary==2.9.6

# Database models
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    query = Column(Text)
    analysis = Column(Text, nullable=False)
    processing_time = Column(Integer)  # seconds
    file_size = Column(Integer)  # bytes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True)
    analysis_count = Column(Integer, default=0)
    total_processing_time = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/financial_analyzer"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Usage in endpoints
@app.post("/analyze")
async def analyze_with_storage(file: UploadFile, query: str = None):
    # Process document
    result = run_crew(query, file_path)
    
    # Save to database
    db = SessionLocal()
    analysis_record = AnalysisResult(
        filename=file.filename,
        query=query,
        analysis=result,
        file_size=len(content),
        processing_time=processing_time
    )
    db.add(analysis_record)
    db.commit()
    
    return {"id": analysis_record.id, "analysis": result}

@app.get("/history")
async def get_analysis_history():
    db = SessionLocal()
    results = db.query(AnalysisResult).order_by(AnalysisResult.created_at.desc()).limit(10).all()
    return results
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
Error: ModuleNotFoundError: No module named 'crewai'
```
**Solution:** Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

#### 2. API Key Issues
```bash
Error: Missing required environment variables: OPENAI_API_KEY
```
**Solution:** Check your `.env` file and ensure API keys are set correctly

#### 3. PDF Processing Errors
```bash
Error: No readable text found in the PDF document
```
**Solution:** 
- Ensure PDF is not password protected
- Check if PDF contains actual text (not just images)
- Try OCR preprocessing for image-based PDFs

#### 4. Memory Issues with Large Files
```bash
Error: File too large for processing
```
**Solution:** Implement file size limits and chunked processing:
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
if len(content) > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")
```

### Debug Mode
Enable detailed logging:
```python
# In main.py
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
LOG_LEVEL=DEBUG
```

### Performance Monitoring
Add timing and monitoring:
```python
import time

start_time = time.time()
result = run_crew(query, file_path)
processing_time = time.time() - start_time

logger.info(f"Analysis completed in {processing_time:.2f} seconds")
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure code quality (`black`, `flake8`, `mypy`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style
- Use Black for formatting
- Follow PEP 8 guidelines
- Add type hints for all functions
- Document all public methods
- Write comprehensive tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) for the multi-agent framework
- [FastAPI](https://fastapi.tiangolo.com) for the web framework
- [OpenAI](https://openai.com) for language model capabilities
- [Serper](https://serper.dev) for web search functionality



---

**Made with ❤️ for the financial analysis community**
