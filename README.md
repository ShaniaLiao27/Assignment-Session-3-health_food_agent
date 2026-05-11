# Health Food Agent 🍎💪

This is a customized Multi-Agent AI system built with Google ADK (Agent Development Kit). It acts as a **Taiwanese Health & Fitness Coach**, featuring bilingual support, personalized nutrition advice, and calorie tracking.

## Features ✨

This system uses a Multi-Agent architecture orchestrated by a root agent (`health_root_agent`). The root agent routes user queries to 4 specialized sub-agents:

1. **`calorie_agent` (Nutritionist)**
   - Queries the *Open Food Facts API* to estimate food calories.
   - Logs daily meals and tracks total caloric intake.
2. **`recipe_agent` (Culinary Coach)**
   - Suggests recipes using *TheMealDB API*.
   - Provides healthy ingredient pairing advice.
   - Generates YouTube search links for cooking tutorials.
3. **`step_agent` (Fitness Coach)**
   - Tracks daily steps.
   - Calculates estimated calories burned and provides relatable "food equivalents" (e.g., "You burned off a bubble tea!").
4. **`bmi_agent` (Health Assessor)**
   - Calculates BMI based on height and weight.
   - Provides gentle, category-specific lifestyle recommendations.

## Tech Stack 🛠️

- **Framework**: [Google Agent Development Kit (ADK)](https://github.com/google/adk)
- **Model**: `gemini-2.5-pro` (via Google Generative AI)
- **Integration**: Model Context Protocol (MCP) for tool execution

## Setup & Installation 🚀

1. Clone this repository.
2. Install dependencies (e.g., `google-adk`, `mcp`, `requests`).
3. Set up your `.env` file in the `health_food_agent` directory:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=0
   GOOGLE_API_KEY=your_api_key_here
   ```
   *(Note: The `.env` file is excluded from git for security).*
4. Run the ADK web interface:
   ```bash
   adk web
   ```
5. Open `http://127.0.0.1:8000` to interact with the agent!

## Demo Prompts 💬
Try asking the agent:
- *"我剛吃了一顆蘋果，幫我記錄"* (Logs an apple into your daily meals)
- *"What can I cook with salmon?"* (Fetches recipes and YouTube links)
- *"I walked 10000 steps today!"* (Calculates calories burned)
- *"我身高 165 公分，體重 55 公斤，幫我算 BMI"* (Calculates BMI)
<img width="2176" height="1370" alt="health agent calorie" src="https://github.com/user-attachments/assets/8ed661a5-0038-46a2-a563-68f3c3835bcd" />
<img width="2176" height="1368" alt="health agent adk web test 1 - BMI" src="https://github.com/user-attachments/assets/da0f0f24-0597-4353-8fcb-2b562f80bd59" />
<img width="2176" height="1374" alt="health agent - recipe" src="https://github.com/user-attachments/assets/b72a6dc5-d138-44d5-8401-4b74b2f5341d" />
