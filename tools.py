import os
import PyPDF2
from io import BytesIO
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

load_dotenv()

# Validate required environment variables
required_env_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

search_tool = SerperDevTool()

class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path='data/sample.pdf'):
        """Tool to read and extract text from PDF financial documents
        
        Args:
            path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content from the PDF
        """
        try:
            if not os.path.exists(path):
                return f"Error: File not found at path: {path}"
            
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                full_text = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text.strip():
                            full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
                    except Exception as e:
                        full_text += f"\n--- Page {page_num + 1} (Error reading) ---\n"
                
                if not full_text.strip():
                    return "Error: No readable text found in the PDF document"
                
                # Clean up the extracted text
                full_text = full_text.replace('\n\n\n', '\n\n')
                return full_text.strip()
                
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        """Analyze financial document data for investment insights"""
        if not financial_document_data or "Error" in financial_document_data:
            return "Cannot analyze investment data due to document reading error"
        
        # Basic investment analysis framework
        analysis = {
            "revenue_analysis": "Revenue trends and growth patterns",
            "profitability_metrics": "Profit margins and efficiency ratios",
            "liquidity_assessment": "Cash flow and working capital analysis",
            "debt_evaluation": "Debt levels and financial leverage",
            "market_position": "Competitive positioning and market share"
        }
        
        return f"Investment Analysis Framework Applied:\n" + \
               "\n".join([f"- {k}: {v}" for k, v in analysis.items()])

class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        """Create risk assessment based on financial document analysis"""
        if not financial_document_data or "Error" in financial_document_data:
            return "Cannot perform risk assessment due to document reading error"
        
        risk_factors = [
            "Market volatility and economic conditions",
            "Industry-specific risks and competition",
            "Financial leverage and debt service capability",
            "Regulatory and compliance risks",
            "Operational and management risks"
        ]
        
        return f"Risk Assessment Framework:\n" + \
               "\n".join([f"- {factor}" for factor in risk_factors])