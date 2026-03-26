# ✈️ VoyageAI – Agentic Trip Planner

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-purple)
![FastMCP](https://img.shields.io/badge/FastMCP-Server-orange)
![Groq](https://img.shields.io/badge/Groq-LLM-black)
![Tavily](https://img.shields.io/badge/Tavily-Search-green)

VoyageAI is an **Agentic AI travel planning system** built using **FastMCP, LangGraph, Groq LLM, and Streamlit**.
It uses multiple tools (weather, web research, attractions, budgeting) to generate a **complete travel itinerary automatically**.

---

# 🌍 Features

* 🤖 **Agentic AI Planner** using LangGraph ReAct agent
* 🔧 **MCP Tool Server** for modular tool execution
* 🌐 **Web Research** using Tavily API
* ☁️ **Weather Data** using OpenWeatherMap
* 🗺 **Tourist Attractions Discovery** using OpenTripMap
* 💰 **Trip Budget Estimation**
* 💱 **Currency Converter**
* 🖥 **Streamlit UI**

---

# 🏗 Project Architecture

```
User
 │
 ▼
Streamlit UI
 │
 ▼
LangGraph Agent
 │
 ▼
MCP Client
 │
 ▼
FastMCP Server
 │
 ├── web_research
 ├── discover_places
 ├── get_city_weather
 ├── estimate_expenses
 ├── convert_money
 └── create_itinerary
```

---

# 📂 Project Structure

```
VoyageAI/
│
├── agent/
│   └── agentic_workflow.py
│
├── trip_mcp/
│   └── mcp_server.py
│
├── prompt_library/
│   └── trip_planner_prompt.py
│
├── utils/
│   ├── helpers.py
│   ├── config_loader.py
│   └── model_loader.py
│
├── logger/
│   └── logging.py
│
├── streamlit_app.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# ⚙️ Prerequisites

Install the following:

* **Python 3.11+**
* **uv package manager**
* API keys for:

```
Groq
Tavily
OpenWeatherMap
OpenTripMap
ExchangeRate API
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
OPENWEATHER_API_KEY=your_openweather_key
OPENTRIPMAP_API_KEY=your_opentripmap_key
EXCHANGERATE_API_KEY=your_exchange_rate_key
```

---

# 📦 Install Dependencies

Install dependencies using **uv**:

```bash
uv sync
```

This installs all packages from `pyproject.toml`.

---

# 🚀 Running the Project

The system has **3 components**:

1️⃣ MCP Server
2️⃣ Agent (LangGraph)
3️⃣ Streamlit UI

---

# 1️⃣ Start MCP Server

Run the MCP server which exposes the travel tools.

```bash
uv run python -m trip_mcp.mcp_server
```

You should see:

```
Starting Trip Planner MCP Server
```

---

# 2️⃣ Start Agent Development Mode (Optional)

For debugging the agent:

```bash
uv run fastmcp dev inspector trip_mcp/mcp_server.py
```

This allows inspection of the MCP tools.

---

# 3️⃣ Run the Streamlit App

Start the UI:

```bash
uv run streamlit run streamlit_app.py
```

The app will open at:

```
http://localhost:8501
```

---

# 🧠 Example Query

```
Plan a 5-day trip to Tokyo for 2 people with a moderate budget in June.
```

The agent will automatically:

1️⃣ Research the destination
2️⃣ Discover attractions
3️⃣ Fetch weather information
4️⃣ Estimate expenses
5️⃣ Generate a full itinerary

---

# 📊 Example Output

```
Destination Summary
Weather
Top Attractions
Daily Itinerary
Budget Estimate
```

---

# 🧰 MCP Tools

| Tool              | Description                 |
| ----------------- | --------------------------- |
| web_research      | Research travel information |
| discover_places   | Find tourist attractions    |
| get_city_weather  | Fetch weather forecast      |
| estimate_expenses | Estimate travel budget      |
| convert_money     | Currency conversion         |
| create_itinerary  | Generate final itinerary    |

---

# 🛠 Tech Stack

* **FastMCP**
* **LangGraph**
* **Groq LLM**
* **Tavily Search**
* **OpenWeatherMap API**
* **OpenTripMap API**
* **Streamlit**

---

# 📸 UI Preview

VoyageAI provides an interactive interface where users can:

* Select destination
* Choose trip duration
* Set budget level
* Generate a full AI travel plan

---

# 🚧 Future Improvements

* Map integration
* Hotel recommendations
* Flight search
* Export itinerary to PDF
* Multi-city trip planning

---

# 👨‍💻 Author

**Kaustav Roy Chowdhury**

AI / Data Science Enthusiast
Interested in **LLM Engineering, Agentic AI, and Applied Machine Learning**
