# excel_insights/nodes/agent.py
from agents import Agent
from excel_insights.nodes import plan_plots, generate_code, edit_code
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    name="Excel Insights Agent",
    model="gpt-5",
    tools=[plan_plots, generate_code, edit_code],
)
