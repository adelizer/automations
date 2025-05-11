import os
import streamlit as st

import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool
from cofounder.custom_agents.cofounder_agent import cofounder_agent


async def main():

    st.title("Cofounder Agent")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            result = Runner.run_streamed(
                cofounder_agent,
                input=st.session_state.messages,
            )
            async for event in result.stream_events():
                # We'll ignore the raw responses event deltas
                if event.type == "raw_response_event":
                    continue
                # When the agent updates, print that
                elif event.type == "agent_updated_stream_event":
                    info_message = f"--Agent updated: {event.new_agent.name}"
                    print(info_message)
                    st.write(info_message)
                    continue
                # When items are generated, print them
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        info_message = f"--Tool call: {event.item.raw_item.name}"
                        print(info_message)
                        st.write(info_message)
                    elif event.item.type == "tool_call_output_item":
                        info_message = f"--Tool call output: {event.item.output}"
                        print(info_message)
                        st.write(info_message)
                    elif event.item.type == "message_output_item":
                        info_message = f"{ItemHelpers.text_message_output(event.item)}"
                        print(info_message)
                        st.write(info_message)
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": ItemHelpers.text_message_output(event.item),
                            }
                        )
                    else:
                        pass  # Ignore other event types


if __name__ == "__main__":
    asyncio.run(main())
