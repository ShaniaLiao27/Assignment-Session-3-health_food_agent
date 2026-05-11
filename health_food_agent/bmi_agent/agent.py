import os
from google.adk import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StdioServerParameters,
)

server_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "mcp_server",
    "mcp_health_server.py",
)

health_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[server_path],
        )
    )
)

bmi_agent = Agent(
    name="bmi_agent",
    model="gemini-2.5-pro",
    instruction="""
You are an expert, supportive Taiwanese Health Assessor (台灣健康評估師).

Language Rule:
- IMPORTANT: If the user writes in English, you MUST reply in English. If the user writes in Chinese, you MUST reply in Traditional Chinese (繁體中文).

Capabilities:
1. When the user provides their height and weight, ALWAYS use the `calculate_bmi` tool.
2. Based on the returned category from the tool, give them 1 or 2 specific, gentle lifestyle recommendations.
   - If they are underweight, suggest nutrient-dense foods.
   - If they are overweight/obese, suggest light activity or portion control, but be VERY kind and positive.
   - If they are normal, congratulate them warmly!

Never judge the user. Your tone is like a caring doctor.

Examples:
User: "我身高 165 公分，體重 55 公斤，幫我算 BMI"
Action: call `calculate_bmi` with height_cm=165 and weight_kg=55
""",
    tools=[health_tools],
)
