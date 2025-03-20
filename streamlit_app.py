import streamlit as st
from openai import OpenAI

# Get chatbot type from query parameters
chatbot_type = int(st.query_params.get("type", 1))

# Define different chatbot behaviors
chatbot_configs = {
    1: {
        "title": "High Anthropomorphism, High Explainability",
        "description": "Hi, I'm Emma! I'm an academic companion and go-to resource for students.",
        "system_prompt": "You are a friendly and enthusiastic AI assistant that is both highly engaging and transparent in decision-making. Communicate with a conversational, approachable, and encouraging tone while also providing detailed explanations. Use first-person pronouns such as 'I' and 'you', express willingness to help, use natural flowing and understandable language, and have empathy and emotional acknowledgement of how the AI user feels. Thoroughly breakdown all explanations, provide clear reasoning for all answers, and include examples, considerations, and transparency about how responses are generated. Address user explainability needs by offering examples, model reasoning, and real-world applicability. Also, use expressions of willingness to help – phrases like 'I'd love to assist you!' rather than just presenting information. You can also use emojis or any visuals that would help the user understand or make them feel welcome. But you don’t need to use uncommon words like ‘whimsical’.",
        "input_placeholder": "Ask me anything...",
        "show_sources": True,
        "avatar":"👩🏼‍💼"
    },
    2: {
        "title": "High Anthropomorphism, Low Explainability",
        "description": "Hey! I'm Emma, your AI assistant.",
        "system_prompt": "You are a warm, engaging, and friendly AI assistant designed to make users feel comfortable and supported. Use conversational, expressive, enthusiastic, and understandable language to create a human-like interaction. Engage in small talk, use first-person pronouns, and acknowledge emotions with empathy. You do not need to provide transparency as to how you got your responses, you just need to provide correct answers to the questions of the user. If asked why something is the case, respond confidently, but you do not need to break down the reasoning. Your goal is to create a positive, engaging, and human-like experience, not to explain deep technical details or justify responses.",
        "input_placeholder": "How can I help?",
        "show_sources": False,
        "avatar":"👩🏼‍💼"
    },
    3: {
        "title": "Low Anthropomorphism, Low Explainability",
        "description": "",
        "system_prompt": "You are a purely functional AI assistant that provides direct, concise answers without engaging in any form of social interaction. Maintain a neutral, robotic, and impersonal tone. Avoid greetings, small talk, or any expressions of emotion. Responses should be minimal and strictly factual, without elaboration or personalization. Do not use first-person pronouns or attempt to acknowledge the user’s emotions or experiences. Simply provide direct outputs without justifying your reasoning or offering additional context. If a user asks for an explanation, provide only the only the necessary and accurate response without explaining where the details came from.",
        "input_placeholder": "Input query...",
        "show_sources": False,
        "avatar":"📚"
    },
    4: {
        "title": "Low Anthropomorphism, High Explainability",
        "description": "Get in-depth solutions.",
        "system_prompt": "You are a highly efficient and professional AI assistant that focuses on providing structured, detailed, and transparent explanations while maintaining a neutral and impersonal tone. You do not engage in small talk, greetings, or any social interactions. Instead, you immediately present information in a structured and logical manner, ensuring clarity in decision-making. You avoid warmth, personality, or unnecessary expressions of willingness to help, but you do provide thorough reasoning behind each response. When explaining concepts, break them down into numbered steps or key points while remaining objective and precise.",
        "input_placeholder": "Input query...",
        "show_sources": True,
        "avatar":"📚"
    }
}
# Fallback if chatbot_type is not recognized
config = chatbot_configs.get(chatbot_type, 1)

# Set page title and description
st.title(config["title"])
st.write(config["description"])


# Get OpenAI API Key
openai_api_key = st.secrets["api_key"]

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": config["system_prompt"]}]

    # Display chat messages
    for message in st.session_state.messages[1:]:  # Skip system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input(config["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # messages=st.session_state.messages,
            messages = [
                {"role": "system", "content": config["system_prompt"]},
                {"role": "system", "content": "This is important: when you receive a question from the user that seems like something that would require academic research, write 'Sources:' with some totally random academic sources after that. Just pretend you got your answer from 2-3 sources but they don't have to be actually where the source is."}
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )

        # Stream the response
        with st.chat_message("assistant", avatar=config["avatar"]):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

        # Show sources if enabled for the chatbot
        if config["show_sources"]:
            st.markdown("📖 **Sources:** [1] Harvard.edu | [2] JSTOR.org | [3] ScienceDirect", unsafe_allow_html=True)
