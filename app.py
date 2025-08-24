"""
Streamlit web interface for the Diet Bot
"""
import streamlit as st
from bot import DietBot

def initialize_bot():
    """Initialize the Diet Bot with sample knowledge"""
    bot = DietBot()
    
    # Add sample nutrition knowledge
    # In a real application, you would load this from a database or files
    sample_knowledge = [
        "A balanced diet should include proteins, carbohydrates, and healthy fats.",
        "Proteins are essential for muscle building and repair. Good sources include lean meats, fish, eggs, and legumes.",
        "Complex carbohydrates provide sustained energy. Sources include whole grains, vegetables, and fruits.",
        "Healthy fats are important for brain function and hormone production. Sources include avocados, nuts, and olive oil.",
        "Portion control is key to maintaining a healthy weight. Use smaller plates and listen to your body's hunger signals.",
        "Hydration is crucial for overall health. Aim to drink 8 glasses of water daily.",
        "Fiber helps with digestion and feeling full. Good sources include whole grains, vegetables, and fruits.",
        "Vitamins and minerals are essential for various bodily functions. Eat a variety of colorful fruits and vegetables."
    ]
    
    bot.initialize_knowledge_base(sample_knowledge)
    return bot

def main():
    st.title("Diet Bot - Your Nutrition Assistant")
    st.write("Ask me anything about diet and nutrition!")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize bot
    if "bot" not in st.session_state:
        st.session_state.bot = initialize_bot()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What's your question about diet and nutrition?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            response = st.session_state.bot.chat(prompt)
            st.markdown(response)
            
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
