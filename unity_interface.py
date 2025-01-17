import streamlit as st
from anthropic import Anthropic
import openai
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Unity Project Team Interface",
    page_icon="🌌",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def load_config():
    """Load API keys and configuration"""
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Configuration file not found. Please create config.json with your API keys.")
        return None

def setup_clients(config):
    """Initialize API clients"""
    anthropic = Anthropic(api_key=config['ANTHROPIC_API_KEY'])
    openai.api_key = config['OPENAI_API_KEY']
    return anthropic, openai

def get_claude_response(anthropic, prompt, system_prompt=""):
    """Get response from Claude"""
    try:
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content
    except Exception as e:
        return f"Error getting Claude response: {str(e)}"

def get_chatgpt_response(prompt):
    """Get response from ChatGPT"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting ChatGPT response: {str(e)}"

def save_conversation(prompt, claude_response, chatgpt_response):
    """Save conversation to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversation = {
        "timestamp": timestamp,
        "prompt": prompt,
        "claude_response": claude_response,
        "chatgpt_response": chatgpt_response
    }
    
    os.makedirs("conversations", exist_ok=True)
    filename = f"conversations/conv_{timestamp.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(conversation, f, indent=2)

def main():
    # Load configuration
    config = load_config()
    if not config:
        return
    
    anthropic, _ = setup_clients(config)
    
    # Header
    st.title("🌌 Unity Project Team Interface")
    st.markdown("---")
    
    # Input area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = st.text_area("Enter your prompt:", height=150)
        
    with col2:
        st.markdown("### Query Options")
        get_claude = st.checkbox("Get Claude's response", value=True)
        get_chatgpt = st.checkbox("Get ChatGPT's response", value=True)
        
        # Additional context options
        st.markdown("### Additional Context")
        include_equations = st.checkbox("Include Unity equations")
        include_progress = st.checkbox("Include project progress")
        
    # Submit button
    if st.button("Submit"):
        if prompt:
            # Build context-aware prompt
            full_prompt = prompt
            if include_equations:
                full_prompt = "Context: Unity Project Equations\n\n" + config['UNITY_EQUATIONS'] + "\n\n" + prompt
            if include_progress:
                full_prompt = "Context: Current Project Progress\n\n" + config['PROJECT_STATUS'] + "\n\n" + full_prompt
            
            # Get responses
            claude_response = get_claude_response(anthropic, full_prompt) if get_claude else None
            chatgpt_response = get_chatgpt_response(full_prompt) if get_chatgpt else None
            
            # Save conversation
            save_conversation(prompt, claude_response, chatgpt_response)
            
            # Display responses
            st.markdown("---")
            st.markdown("### Responses")
            
            if get_claude:
                with st.expander("Claude's Response", expanded=True):
                    st.markdown(claude_response)
            
            if get_chatgpt:
                with st.expander("ChatGPT's Response", expanded=True):
                    st.markdown(chatgpt_response)
            
            # Add to session history
            st.session_state.chat_history.append({
                "prompt": prompt,
                "claude": claude_response,
                "chatgpt": chatgpt_response
            })
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Previous Query {len(st.session_state.chat_history) - i}"):
                st.markdown("**Prompt:**")
                st.markdown(chat["prompt"])
                if chat["claude"]:
                    st.markdown("**Claude:**")
                    st.markdown(chat["claude"])
                if chat["chatgpt"]:
                    st.markdown("**ChatGPT:**")
                    st.markdown(chat["chatgpt"])

if __name__ == "__main__":
    main()