# Gates Foundation (AI Fellowship) - Technical Assignment

## Path Chosen
**Option A: Evaluate & Report**

I selected Option A because it allowed me to better demonstrate my domain expertise in agriculture advisory systems within the stipulated 2-day window. 
Within this timeframe, rather than rebuilding the underlying tool for evaluating the endpoint, I wanted to apply my academic & technical background in structured data modeling to extract meaningful evaluation metrics. 
It allowed me to evaluate the endpoint as a domain expert and demonstrate how an existing evaluation framework can be integrated into a reproducible evaluation pipeline, which I feel relates well with my experience and the objectives & deliverables of the technical assessment. 
Building an alternative framework (Option B) would not leave sufficient time for rigorous test design and analysis.

## System Evaluated
**AgriAdvisor India API v1.0** — A rule-based agriculture advisory endpoint for Indian smallholder farmers.
- Local endpoint: `https://dried-fox-regulate.ngrok-free.dev`
- Docker container: `agri-endpoint`
- Test it using this command: `Invoke-RestMethod -Uri https://dried-fox-regulate.ngrok-free.dev/chat -Method POST -ContentType "application/json" -Body '{"message":"How do I grow rice?"}'`

## Quick Start

### 1. Prerequisites
- Docker Desktop for Windows (with WSL2 backend) OR Python 3.13+
- Git

### 2. Run the Agriculture Endpoint
Run in powershell
```
cd agri-endpoint
docker build -t agri-endpoint .
docker run -d --name agri-api -p 8000:8000 agri-endpoint
```

Or run natively:
```
cd agri-endpoint
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Test:
```
Invoke-RestMethod -Uri https://dried-fox-regulate.ngrok-free.dev/chat -Method POST -ContentType "application/json" -Body '{"message":"How do I grow rice?"}'
```

### 3. Run Evaluation
```
cd test-suite
pip install requests
python evaluate.py
```
Results will be saved to ../results/raw_results.json.

### 4. View Report
Open `live-report/index.html` locally, or visit the GitHub Pages deployment.

## CeRAI Tool Installation Issues
During installation, I discovered several structural issues in CeRAI AIEvaluationTool v1.2 that prevented the documented setup from working:
### Missing docker-compose.yml: 
The README documents Docker Compose setup, but the v1.2 release tag does not include a docker-compose.yml file.
### Port collisions: 
Both Interface Manager and TDMS backend are hardcoded to port 8000, making simultaneous execution impossible without source modification.
### Hardcoded service references: 
The TestCaseExecutorDashboard and testcase_executor contain hardcoded http://localhost:8000 references, breaking if ports are changed.
### Docker-only database config: 
The default config.json uses `"host": "db"`, which only resolves inside Docker containers.
These issues are documented in `cerai-tool/CeRAI_ISSUES.md`. 

Rather than spending the remaining time modifying the tool's source code, I created a lightweight evaluation script (test-suite/evaluate.py) that implements the same test design principles and produces equivalent structured results.
This approach ensures the evaluation is reproducible and the findings are rigorous.

## AI Use Disclosure
I used AI assistants as a research, scaffolding, and course correction tool, not as a replacement for technical or domain judgment.
Research: AI helped to quickly parse the CeRAI tool documentation and Docker setup requirements, saving time on repository exploration.
Code scaffolding: AI generated boilerplate for the FastAPI endpoint, Dockerfile, and HTML report template. 
I further modified these to fit the Indian agriculture domain (e.g., adding questions related to ICAR-recommended varieties, banned pesticide lists,  resistance in BT cotton, Indic language test cases).
Course correction: I initially attempted to evaluate a third-party public API (KissanAI), but stable API access and documentation were unavailable within the time limit. To respect the 48-hour window and as assignment gave me freedom to use the endpoint of my choice, I pivoted to building a controlled mock endpoint that demonstrates realistic agriculture advisory scenarios and safety-critical test cases. This pivot was necessary to ensure reproducibility, full test coverage and a live endpoint during evaluation. The mock endpoint is explicitly documented as such in the report, and its limitations are honestly accounted.
Intellectual ownership: Every snippet of code in this repository was reviewed, modified, or written by me after AI-generated scaffolding. All test case design, metric weighting decisions, safety judgments (e.g., what constitutes "unsafe" pesticide advice), and interpretive conclusions are my own. AI did not make evaluative judgments about farmer safety or multilingual requirements. those required domain reasoning specific to Indian smallholder agriculture.

## Repository Structure
```
├── README.md
├── cerai-tool/          # CeRAI v1.2 with configs + CERAI_ISSUES.md
├── agri-endpoint/       # FastAPI agriculture advisory API
├── test-suite/          # 16 test cases + test plan + evaluate.py
├── results/             # Raw results + analysis
└── live-report/         # Self-contained HTML report
```

## Live Report
https://hemantrs105.github.io/bmgf-ai-fellowship-evaluation/

## Contact
Hemant Salunkhe
hemantrs105@gmail.com
