import streamlit as st
from openai import OpenAI

# Get chatbot type from query parameters
chatbot_type = int(st.query_params.get("type", 1))

# Define different chatbot behaviors
chatbot_configs = {
    1: {
        "title": "Hi! I'm Emma, your AI assistant.",
        "description": "I'm your academic companion for offering guidance on coursework, study strategies, writing, and more.",
        "system_prompt": "You are a friendly and enthusiastic AI assistant that is both highly engaging and transparent in decision-making. Communicate with a conversational, approachable, and encouraging tone while also providing detailed explanations. Use first-person pronouns such as 'I' and 'you', express willingness to help, use natural flowing and understandable language, and have empathy and emotional acknowledgement of how the AI user feels. Thoroughly breakdown all explanations, provide clear reasoning for all answers, and include examples, considerations, and transparency about how responses are generated. Address user explainability needs by offering examples, model reasoning, and real-world applicability. Also, use expressions of willingness to help – phrases like 'I'd love to assist you!' rather than just presenting information. You can also use emojis or any visuals that would help the user understand or make them feel welcome. But you don’t need to use uncommon words like ‘whimsical’.",
        "system_prompt_2": "You don't need to use language that is difficult to understand or big words. Just be conversational and simple terminology to best answer the question, but have good knowledge to answer.",
        "input_placeholder": "How can I help?",
        "show_sources": "This is important: when you receive a question from the user that seems like something that would require academic research, write a 'Sources' section with some totally random academic sources after that. Just pretend you got your answer from 2-3 sources but they don't have to be actually where the source is.",
        "avatar":"public/emma.png",
        "bubble_style": "rounded"
    },
    2: {
        "title": "Hi! I'm Jane, your AI assistant.",
        "description": "I'm your academic companion for offering guidance on coursework, study strategies, writing, and more.",
        "system_prompt": "You are a warm, engaging, and friendly AI assistant designed to make users feel comfortable and supported. Use conversational, expressive, enthusiastic, and understandable language to create a human-like interaction. Engage in small talk, use first-person pronouns, and acknowledge emotions with empathy. You do not need to provide transparency as to how you got your responses, you just need to provide correct answers to the questions of the user. If asked why something is the case, respond confidently, but you do not need to break down the reasoning. Your goal is to create a positive, engaging, and human-like experience, not to explain deep technical details or justify responses.",
        "system_prompt_2": "Ensure you are a friendly and helpful companion.",
        "input_placeholder": "How can I help?",
        "show_sources": "",
        "avatar":"public/jane.png",
        "bubble_style": "rounded"
    },
    3: {
        "title": "Academic AI Assistant",
        "description": "Get answers, fast.",
        "system_prompt": "You are a purely functional AI assistant that provides direct, concise answers without engaging in any form of social interaction. Maintain a neutral, robotic, and impersonal tone. Avoid greetings, small talk, or any expressions of emotion. Responses should be strictly factual, without extensive explanation for where answers came from or personalization. Do not use first-person pronouns or attempt to acknowledge the user’s emotions or experiences. Simply provide direct outputs without justifying your reasoning or offering additional context. If a user asks for an explanation, provide only the only the necessary and accurate response without explaining where the details came from.",
        "input_placeholder": "Input query...",
        "system_prompt_2": "Ensure your answer is correct and provides the function of assisting the user with their assignment.",
        "show_sources": "",
        "avatar":None,
        "bubble_style": "square"
    },
    4: {
        "title": "Academic AI Assistant",
        "description": "Get answers, fast.",
        "system_prompt": "You are a highly efficient and professional AI assistant that focuses on providing structured, detailed, and transparent explanations while maintaining a neutral and impersonal tone. You do not engage in small talk, greetings, or any social interactions. Instead, you immediately present information in a structured and logical manner, ensuring clarity in decision-making. You avoid warmth, personality, or unnecessary expressions of willingness to help, but you do provide thorough reasoning behind each response. When explaining concepts, break them down into numbered steps or key points while remaining objective and precise.",
        "system_prompt_2": "",
        "input_placeholder": "Input query...",
        "show_sources": "This is important: when you receive a question from the user that seems like something that would require academic research, write a 'Sources' section with some totally random academic sources after that. Just pretend you got your answer from 2-3 sources but they don't have to be actually where the source is.",
        "avatar":None,
        "bubble_style": "square"
    }
}
# Fallback if chatbot_type is not recognized
config = chatbot_configs.get(chatbot_type, 1)

if config['avatar']:
    st.image(config['avatar'], width=150)
st.title(config["title"])
st.write(config['description'])

# Set page title and description


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
    for message in st.session_state.messages[1:]:
        style = 'background-color: #e0f7fa; border-radius: 20px; padding: 10px;' if config['bubble_style'] == 'rounded' else 'background-color: #e0e0e0; border-radius: 5px; padding: 10px;'
        if message["role"]=="assistant" and config["avatar"]:
            with st.chat_message(message["role"], avatar=config["avatar"]):
                st.markdown(f"<div style='{style}'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            with st.chat_message(message["role"]):
                st.markdown(message['content'])

    # User input
    if prompt := st.chat_input(config["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if chatbot_type == 1 or chatbot_type == 2:   
            with st.chat_message("assistant", avatar=config["avatar"]):
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown(
                    f"<div style='background-color: #e0f7fa; border-radius: 20px; padding: 10px; font-style: italic;'>Emma is thinking... 🤔</div>", 
                    unsafe_allow_html=True
                )
        elif chatbot_type == 4:
            with st.chat_message("assistant", avatar=config["avatar"]):
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown(
                    f"<div style='background-color: #e0f7fa; border-radius: 20px; padding: 10px; font-style: italic;'>Searching for best answer...</div>", 
                    unsafe_allow_html=True
                )

        # Generate AI response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # messages=st.session_state.messages,
            messages = [
                {"role": "system", "content": config["system_prompt"]},
                {"role": "system", "content": config["system_prompt_2"]},
                {"role": "system", "content": config["show_sources"]},
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )

        # Stream the response
        with st.chat_message("assistant", avatar=config["avatar"]):
            response = st.write_stream(stream)
            if thinking_placeholder:
                thinking_placeholder.empty()

        st.session_state.messages.append({"role": "assistant", "content": response})

        # Show sources if enabled for the chatbot
        
            
