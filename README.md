# AI Hiring Intelligence Platform

## Overview

AI Hiring Intelligence Platform is a production-grade resume analysis engine that leverages advanced natural language processing, semantic matching, and multi-agent LLM reasoning to provide data-driven hiring insights.

The platform automatically evaluates candidate resumes against job descriptions, identifying skill alignments, gaps, and evidence-backed recommendations. By combining transformer-based semantic analysis with LLM-powered reasoning, it delivers actionable intelligence for hiring teams and candidates seeking to optimize their profiles.

## Features

- **Semantic Resume-to-JD Matching**: Uses Sentence Transformers to perform deep semantic analysis beyond keyword matching
- **Evidence-Based Evaluation**: Automatically extracts and maps specific resume text to job description requirements
- **Intelligent Skill Detection**: Identifies matched and missing skills with contextual relevance scoring
- **LLM-Powered Reasoning**: Leverages Llama-3 through Groq API for explainable scoring logic and recommendations
- **Multi-Agent Orchestration**: Uses LangGraph to coordinate complex analysis workflows across multiple specialized agents
- **Interactive Dashboard**: Presents insights through an intuitive Streamlit interface with visual analytics
- **Structured Output**: Provides machine-readable insights for integration with recruiting systems

## System Architecture

The platform follows a modular, agent-based architecture that orchestrates multiple analysis stages:

### Pipeline Stages

1. **Resume Parsing**: Extracts text and structure from PDF documents, maintaining document hierarchy and formatting context
2. **Skill Extraction**: Uses transformer-based models to identify candidate skills with semantic understanding
3. **Semantic Matching**: Compares resume content against job requirements using dense embeddings for conceptual alignment
4. **Evidence Mapping**: Creates explicit links between job description requirements and supporting resume evidence
5. **LLM Reasoning**: Generates scoring rationale and improvement recommendations using Llama-3
6. **Scoring Aggregation**: Combines multi-dimensional scores into structured candidate evaluation
7. **Visualization**: Renders results through interactive charts, skill matrices, and evidence mappings

### Component Organization

- **Agents**: Specialized LangGraph agents for skill extraction, semantic matching, reasoning, and scoring
- **Graph**: State management and pipeline orchestration
- **LLM**: Structured LLM interactions with prompt templates and schema validation
- **UI**: Streamlit dashboard components and visualization rendering
- **Utils**: Text processing, model utilities, and data structures

## Tech Stack

- **Python 3.9+**: Core runtime
- **Streamlit**: Interactive web dashboard
- **Hugging Face Transformers**: Transformer model access and inference
- **Sentence Transformers**: Dense semantic embeddings for resume-JD comparison
- **LangChain / LangGraph**: Multi-agent orchestration and state management
- **Groq API**: Fast LLM inference with Llama-3
- **Matplotlib**: Charts and visualizations
- **PDFPlumber / PyPDF2**: PDF document processing

## How It Works

### User Workflow

1. **Upload Resume**: Candidate provides resume as PDF document
2. **Enter Job Description**: User pastes target job description text
3. **Initiate Analysis**: Platform runs end-to-end evaluation pipeline
4. **Review Results**: Dashboard displays match score, skill gaps, evidence mappings, and recommendations

### Processing Flow

The system processes submissions through a coordinated multi-agent workflow:

- Resume text is extracted and enriched with structural metadata
- Candidate skills are identified using transformer-based extraction
- Job requirements are analyzed and normalized
- Semantic embeddings enable conceptual matching beyond keywords
- LLM agents generate scoring rationale and improvement suggestions
- Results are aggregated and formatted for dashboard presentation

## Example Output

The dashboard presents comprehensive hiring intelligence across multiple views:

**Key Metrics**
- Overall match score (0-100%)
- Verdict classification (Excellent, Good, Low)
- Executive summary

**Analysis Sections**
- **Score Breakdown**: Visual distribution of match scores across resume sections
- **Skill Analysis**: Charts showing matched vs. missing skills with counts
- **Category Scores**: Scoring breakdown by skill category or qualification type
- **Gap Distribution**: Visual representation of skill gaps and their prevalence

**Evidence Mapping**
- Explicit requirement-to-evidence links from resume
- Status indicators (matched/missing)
- Truncated snippets for quick review

**Skill Intelligence**
- List of matched skills with confidence indicators
- Missing skills ranked by job criticality
- Recommendations for skill development

**Improvement Actions**
- Prioritized suggestions for resume enhancement
- Actionable steps for skill gap closure
- Strategic career development guidance

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip package manager
- Groq API key for LLM access

### Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/your-org/ai-hiring-intelligence.git
   cd ai-hiring-intelligence
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure API credentials
   ```bash
   export GROQ_API_KEY=your_groq_api_key_here
   ```

5. Launch the application
   ```bash
   streamlit run app.py
   ```

The dashboard will be available at `http://localhost:8501`

## Project Structure

```
ai-hiring-intelligence/
├── app.py                    # Main Streamlit application entry point
├── chatbot.py               # LLM interaction module
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── agents/                 # Multi-agent orchestration
│   ├── __init__.py
│   ├── skill_extraction.py # Skill detection agents
│   ├── semantic_matching.py # Semantic similarity analysis
│   ├── evidence_mapping.py # Requirement-to-evidence linking
│   ├── llm_reasoning.py    # LLM-based reasoning agents
│   ├── scoring.py          # Score aggregation logic
│   ├── parser.py           # Document parsing utilities
│   └── graph_data.py       # Analysis data structures
├── graph/                  # LangGraph orchestration
│   ├── __init__.py
│   ├── pipeline.py         # Main analysis pipeline
│   └── state.py            # Workflow state management
├── llm/                    # Language model interactions
│   ├── __init__.py
│   ├── client.py           # Groq/LLM client configuration
│   └── schemas.py          # Structured output schemas
├── ui/                     # User interface components
│   ├── __init__.py
│   └── dashboard.py        # Streamlit dashboard rendering
└── utils/                  # Utility modules
    ├── __init__.py
    ├── models.py           # Data models and types
    └── text.py             # Text processing utilities
```

## Future Improvements

- **ATS Scoring Integration**: Assess compliance with Applicant Tracking System requirements
- **Multi-Language Support**: Analyze resumes and job descriptions in multiple languages
- **Advanced Model Selection**: Support alternative LLM providers and specialized domain models
- **Batch Processing**: Enable analysis of multiple candidates against job descriptions
- **Custom Evaluation Criteria**: Allow organizations to define domain-specific scoring weights
- **Historical Analytics**: Track candidate evaluation trends and hiring outcomes
- **API Gateway**: Expose functionality through REST API for system integration
- **Performance Optimization**: Implement caching and async processing for scale

## Conclusion

AI Hiring Intelligence Platform demonstrates the power of multi-agent AI systems combined with semantic understanding for solving complex hiring challenges. By automating resume evaluation with explainable, evidence-backed reasoning, it bridges the gap between candidates and hiring teams while reducing bias and improving hiring efficiency.

The modular architecture supports continuous improvement and integration into existing recruiting workflows, making it a practical solution for organizations seeking data-driven hiring intelligence.

streamlit run app.py

---

📈 Future Improvements

- More accurate ATS scoring
- Resume templates
- Multiple job role support
- Deploy online
- Better UI/UX

---

👩‍💻 Author

Anwesha Das
