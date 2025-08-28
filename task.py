from crewai import Task
from agents import financial_analyst, verifier
from tools import search_tool, FinancialDocumentTool, InvestmentTool, RiskTool

analyze_financial_document = Task(
    description="""Conduct a comprehensive analysis of the financial document provided.
    
    User Query: {query}
    
    Your analysis should include:
    1. Document overview and key highlights
    2. Financial performance metrics (revenue, profitability, cash flow)
    3. Balance sheet analysis (assets, liabilities, equity)
    4. Key financial ratios and trends
    5. Market position and competitive analysis
    6. Investment thesis and recommendations
    7. Risk factors and concerns
    
    Use the financial document reading tool to extract data and provide evidence-based insights.
    Search for recent market information if needed to contextualize the analysis.""",

    expected_output="""A comprehensive financial analysis report including:
    
    ## Executive Summary
    - Key findings and investment recommendation
    
    ## Financial Performance Analysis
    - Revenue and growth trends
    - Profitability metrics
    - Cash flow analysis
    
    ## Balance Sheet Assessment
    - Asset quality and composition
    - Debt levels and capital structure
    
    ## Investment Recommendation
    - Clear buy/hold/sell recommendation with reasoning
    - Target price or valuation range
    - Time horizon for the recommendation
    
    ## Risk Assessment
    - Key risk factors
    - Risk mitigation strategies
    
    All analysis should be based on concrete data from the financial document.""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="""Provide detailed investment analysis and recommendations based on the financial document.
    
    Focus on:
    1. Investment attractiveness and valuation
    2. Growth prospects and competitive advantages
    3. Dividend policy and shareholder returns
    4. Comparison with industry peers
    5. Specific investment strategies (long-term vs short-term)
    
    User Query: {query}""",

    expected_output="""Investment Analysis Report:
    
    ## Investment Rating
    - Overall recommendation (Strong Buy/Buy/Hold/Sell/Strong Sell)
    - Confidence level and rationale
    
    ## Valuation Analysis
    - Current valuation metrics
    - Fair value estimation
    - Price targets
    
    ## Growth Prospects
    - Revenue growth projections
    - Market expansion opportunities
    - Competitive advantages
    
    ## Shareholder Value
    - Dividend policy analysis
    - Share buyback programs
    - Capital allocation strategy
    
    ## Portfolio Fit
    - Suitable investor profiles
    - Portfolio allocation recommendations""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, InvestmentTool.analyze_investment_tool],
    async_execution=False,
)

risk_assessment = Task(
    description="""Conduct thorough risk assessment of the investment opportunity.
    
    Analyze:
    1. Financial risks (leverage, liquidity, credit)
    2. Operational risks (business model, management)
    3. Market risks (volatility, competition, regulation)
    4. ESG risks (environmental, social, governance)
    5. Macroeconomic risks
    
    User Query: {query}""",

    expected_output="""Risk Assessment Report:
    
    ## Risk Rating
    - Overall risk level (Low/Medium/High)
    - Risk-adjusted return potential
    
    ## Financial Risks
    - Debt and leverage analysis
    - Liquidity and cash flow risks
    
    ## Business Risks
    - Operational and competitive risks
    - Management and governance risks
    
    ## Market Risks
    - Industry and regulatory risks
    - Economic sensitivity analysis
    
    ## Risk Mitigation
    - Diversification strategies
    - Hedging opportunities
    - Position sizing recommendations""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, RiskTool.create_risk_assessment_tool],
    async_execution=False,
)

verification = Task(
    description="""Verify the financial document and validate the quality of analysis.
    
    Check:
    1. Document authenticity and completeness
    2. Data consistency and accuracy
    3. Analysis quality and methodology
    4. Compliance with financial reporting standards""",

    expected_output="""Document Verification Report:
    
    ## Document Status
    - File type and format validation
    - Content completeness assessment
    
    ## Data Quality
    - Numerical consistency checks
    - Missing information identification
    
    ## Analysis Validation
    - Methodology appropriateness
    - Conclusion reasonableness
    
    ## Recommendations
    - Additional analysis needed
    - Data verification suggestions""",

    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)