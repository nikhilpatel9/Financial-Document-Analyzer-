import os
from crewai import Agent
from tools import search_tool, FinancialDocumentTool

# Validate environment setup
def validate_environment():
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

validate_environment()

financial_analyst = Agent(
    role='Senior Financial Analyst',
    goal='Provide comprehensive and accurate financial analysis of documents with actionable investment insights',
    backstory="""You are a seasoned financial analyst with over 15 years of experience in 
    investment banking and equity research. You specialize in analyzing corporate financial 
    statements, identifying key financial metrics, and providing data-driven investment 
    recommendations. You have a track record of successful stock picks and risk assessments.""",
    
    verbose=True,
    allow_delegation=False,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    
    # Enhanced capabilities
    max_iter=3,
    memory=True
)

verifier = Agent(
    role='Financial Document Verifier',
    goal='Verify the authenticity and completeness of financial documents and validate analysis quality',
    backstory="""You are a meticulous financial auditor with expertise in document 
    verification and quality assurance. You ensure all financial analyses are based on 
    accurate data and follow industry standards.""",
    
    verbose=True,
    allow_delegation=False,
    tools=[FinancialDocumentTool.read_data_tool]
)