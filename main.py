from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import logging
from typing import Optional

# Import the crew components
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Financial Document Analyzer",
    description="AI-powered financial document analysis system",
    version="1.0.0"
)

def run_crew(query: str, file_path: str = "data/sample.pdf") -> str:
    """Run the financial analysis crew
    
    Args:
        query (str): User's analysis query
        file_path (str): Path to the financial document
        
    Returns:
        str: Analysis results
    """
    try:
        # Validate inputs
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Financial document not found at: {file_path}")
        
        # Create and configure the crew
        financial_crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the analysis
        logger.info(f"Starting analysis for query: {query}")
        result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
        
        logger.info("Analysis completed successfully")
        return str(result)
        
    except Exception as e:
        logger.error(f"Error in crew execution: {str(e)}")
        raise Exception(f"Analysis failed: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "data_directory": os.path.exists("data"),
        "required_env_vars": {
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
            "SERPER_API_KEY": bool(os.getenv("SERPER_API_KEY"))
        }
    }

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(..., description="PDF financial document to analyze"),
    query: Optional[str] = Form(
        default="Analyze this financial document for investment insights",
        description="Specific analysis query or question"
    )
):
    """
    Analyze financial document and provide comprehensive investment recommendations
    
    Args:
        file: PDF file containing financial data
        query: Specific question or analysis focus
        
    Returns:
        JSON response with analysis results
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported for financial document analysis"
        )
    
    # Generate unique file ID and path
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        logger.info(f"Processing uploaded file: {file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
        
        query = query.strip()
        
        # Process the financial document
        logger.info(f"Starting financial analysis with query: {query}")
        analysis_result = run_crew(query=query, file_path=file_path)
        
        logger.info("Analysis completed successfully")
        return {
            "status": "success",
            "query": query,
            "analysis": analysis_result,
            "file_processed": file.filename,
            "file_size": len(content),
            "processing_id": file_id
        }
        
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"File processing error: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error processing financial document: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing financial document: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup file {file_path}: {cleanup_error}")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "error": True,
        "status_code": exc.status_code,
        "message": exc.detail,
        "type": "HTTP Exception"
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "error": True,
        "status_code": 500,
        "message": "Internal server error occurred",
        "type": "Server Error"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Check environment setup before starting
    required_env_vars = ["OPENAI_API_KEY", "SERPER_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set up your .env file with the required API keys:")
        for var in missing_vars:
            print(f"  {var}=your_api_key_here")
        exit(1)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    logger.info("Starting Financial Document Analyzer API...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )