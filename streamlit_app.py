import streamlit as st
import asyncio
from datetime import datetime

from agent.agentic_workflow import graph
from langchain_core.messages import HumanMessage

# direct converter
from utils.helpers import convert_currency

st.set_page_config(page_title="VoyageAI", page_icon="✈️", layout="wide")

st.title("✈️ VoyageAI")
st.markdown("**Intelligent Agentic Trip Planner** powered by FastMCP + LangGraph + Groq")

# ---------------- SESSION STATE ----------------
if "trip_plan" not in st.session_state:
    st.session_state.trip_plan = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Plan Your Trip")

    destination = st.text_input("Destination (City or Country)", value="Tokyo")
    days = st.slider("Number of Days", 1, 15, value=5)
    travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=2)
    budget_level = st.selectbox("Budget Level", ["budget", "moderate", "luxury"], index=1)
    travel_date = st.date_input("Travel Date", datetime.now().date())

    generate_button = st.button(
        "🚀 Generate Complete Trip Plan",
        type="primary",
        use_container_width=True
    )

# ---------------- GENERATE TRIP ----------------
if generate_button and destination:

    with st.spinner(f"Planning your trip to **{destination}**... (This may take 20-40 seconds)"):

        user_query = (
            f"Plan a {days}-day {budget_level} budget trip to {destination} "
            f"for {travelers} people in {travel_date.strftime('%B %Y')}"
        )

        try:
            config = {
                "configurable": {
                    "thread_id": f"st_{int(datetime.now().timestamp())}"
                }
            }

            async def run_agent():
                inputs = {"messages": [HumanMessage(content=user_query)]}
                final_response = None

                async for event in graph.astream(
                    inputs,
                    config=config,
                    stream_mode="values"
                ):
                    last_msg = event["messages"][-1]

                    if last_msg.content and len(last_msg.content) > 100:
                        final_response = last_msg.content

                return final_response

            final_response = asyncio.run(run_agent())

            if final_response:
                st.session_state.trip_plan = final_response

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info(
                "💡 Make sure your MCP Server is running\n\n"
                "`uv run python -m trip_mcp.mcp_server`"
            )

# ---------------- SHOW TRIP PLAN ----------------
if st.session_state.trip_plan:

    st.success(f"✅ Trip plan ready for **{destination}**!")

    st.markdown("## 📋 Your Complete Trip Plan")
    st.markdown(st.session_state.trip_plan)

    # ---------------- CURRENCY CONVERTER ----------------
    st.markdown("---")
    st.subheader("💱 Quick Currency Converter")

    col1, col2 = st.columns([3, 2])

    with col1:
        amount = st.number_input(
            "Amount",
            value=50000.0,
            step=100.0,
            format="%.2f"
        )

        from_curr = st.text_input(
            "From Currency",
            value="JPY",
            max_chars=3
        ).upper()

    col_a, col_b = st.columns(2)

    # -------- USD --------
    with col_a:

        if st.button("Convert to USD", use_container_width=True):

            if amount > 0 and from_curr:

                with st.spinner("Converting to USD..."):

                    try:
                        converted = convert_currency(amount, from_curr, "USD")

                        st.success(
                            f"{amount:,.2f} {from_curr} = {converted:,.2f} USD"
                        )

                    except Exception as e:
                        st.error(f"Conversion failed: {e}")

    # -------- INR --------
    with col_b:

        if st.button("Convert to INR", use_container_width=True):

            if amount > 0 and from_curr:

                with st.spinner("Converting to INR..."):

                    try:
                        converted = convert_currency(amount, from_curr, "INR")

                        st.success(
                            f"{amount:,.2f} {from_curr} = {converted:,.2f} INR"
                        )

                    except Exception as e:
                        st.error(f"Conversion failed: {e}")

else:
    st.info(
        "👈 Fill the sidebar and click **Generate Complete Trip Plan** "
        "to see the full itinerary."
    )

st.caption(
    "Powered by FastMCP • LangGraph • Groq • Tavily • OpenWeatherMap"
)
