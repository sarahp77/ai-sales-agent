# 🤖 Nova: Enterprise Autonomous AI Sales Agent

An intelligent, production-ready AI Sales Consultant built with **LangGraph**, **LangChain**, and **OpenAI (GPT-4o-mini)**, featuring dynamic tool invocation, business domain guardrails, and a modern **Streamlit** web interface.

---

## 🌟 Key Features

- **Cyclic Agentic Workflow:** Built using a dynamic state graph via `LangGraph`, managing multi-turn context and routing between reasoning and tool execution.
- **Dynamic Tool Calling:** Inspects and retrieves real-time catalog data, inventory status, and USD pricing from external JSON storage.
- **Domain Guardrails & Policy Enforcement:** Strictly scoped to platform offerings; gracefully deflects off-topic queries (trivia, creative writing) while preserving high conversion rates.
- **Interactive UI:** Responsive, session-aware chat interface built with Streamlit.

---

## 🏗️ Architecture Overview
```text
+-----------------+
|   User Prompt   |
+--------+--------+
|
v
+-----------------+
|   Agent Node    | <---------------+
|  (GPT-4o-mini)  |                 |
+--------+--------+                 |
|                          |
[Tool Call Needed?]                |
/           \                    |
(Yes)          (No)                 |
/               \                  |
v                 v                 |
+--------------+    +----------+           |
| Action: Tool |    | Respond  |           |
| (JSON Read)  |    | to User  |           |
+------+-------+    +----+-----+           |
|                 |                 |
+-----------------+-----------------+
|
v
[Finished]

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- An OpenAI API Key

### 2. Installation
Clone this repository and create a virtual environment:

bash
git clone https://github.com/your-username/ai-sales-agent.git
cd ai-sales-agent
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies:
bash
pip install langchain langchain-openai langgraph streamlit python-dotenv

### 3. Environment Configuration
Create a `.env` file in the root directory:
env
OPENAI_API_KEY=your_actual_openai_api_key_here

### 4. Run the Application
Launch the Streamlit app:
bash
streamlit run app.py

---

## 📁 Project Structure

text
├── core/
│   ├── __init__.py
│   └── agent.py          # LangGraph state machine, nodes, and sales prompt
├── data/
│   └── products.json     # Dynamic catalog & inventory database
├── .env.example          # Sample environment variables
├── .gitignore            # Excludes secrets and environments
├── app.py                # Streamlit chat interface
└── README.md             # Project documentation

---

## 📄 License
This project is open-source under the MIT License.


---

