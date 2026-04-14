 Developer Tools Research Agent

A command-line based Developer Tools Research Agent that helps you discover, analyze, and compare developer tools and companies based on your query.

It fetches structured insights like pricing, tech stack, integrations, API availability, and more — making it easier to evaluate tools for your projects.

🚀 Features
🔍 Query developer tools using natural language
🏢 Get detailed company/tool information:
Website
Pricing model
Open-source status
Tech stack
Supported languages
API availability
Integrations
📊 Structured output for easy comparison
🧠 Intelligent recommendations based on your query
🔐 Environment-based configuration using .env
📁 Project Structure
.
├── src/
│   └── workflow.py        # Core logic for processing queries
├── .env                   # Environment variables
├── main.py                # Entry point (your script)
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/Pranshu-cyber/Development-Tools-Scraper.git
cd dev-tools-research-agent
2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
3. Install dependencies
pip install -r requirements.txt
🔐 Environment Setup

Create a .env file in the root directory:

# Example variables (update based on your workflow implementation)
API_KEY=your_api_key_here
MODEL_NAME=gpt-4

⚠️ Make sure .env is added to .gitignore

▶️ Usage

Run the application:

python main.py
Example interaction:
Developer Tools Research Agent

🔍 Developer Tools Query: CI/CD tools

📊 Results for: CI/CD tools
============================================================

1. 🏢 Company Name
   🌐 Website: https://example.com
   💰 Pricing: Freemium
   📖 Open Source: No
   🛠️ Tech Stack: Docker, Kubernetes, AWS
   💻 Language Support: Python, JavaScript
   🔌 API: ✅ Available
   🔗 Integrations: GitHub, GitLab
   📝 Description: A powerful CI/CD platform

Developer Recommendations:
----------------------------------------
Best suited for scalable deployments...
🧠 How It Works
User enters a query
Workflow processes the query
Relevant companies/tools are retrieved and analyzed
Structured results + recommendations are displayed
🛑 Exit Commands

You can exit the program by typing:

exit
quit
clear
(empty input)
🧩 Customization

You can extend the project by:

Adding more data sources (APIs, scraping, etc.)
Enhancing ranking/analysis logic
Exporting results (CSV, JSON, etc.)
Building a web UI (React + FastAPI)
🐞 Troubleshooting
Module not found error
Ensure you're running from the root directory
Check your virtual environment
Environment variables not loading
Confirm .env exists and load_dotenv() is called
📌 Future Improvements
🌐 Web dashboard
📈 Tool comparison charts
🤖 AI-powered ranking/scoring
📤 Export/share reports