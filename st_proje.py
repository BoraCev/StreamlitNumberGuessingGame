import streamlit as st
import requests
import string
import uuid

# Function to display chat history
def display_chat_history():
    for item in st.session_state.chat_history:
        st.chat_message(item['sender']).write(item['message'])

if 'guessed_correctly' not in st.session_state:
    st.session_state.guess = 0
    st.session_state.guessed_correctly = False
    st.session_state.guess_count = 0
    st.session_state.lower_bound = 1
    st.session_state.upper_bound = 100

# Session State variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({'sender': 'assistant', 'message': 'You need to think of a number between 1 and 100 and I will try to guess which number you thought of.'})
    st.session_state.guess = (st.session_state.lower_bound + st.session_state.upper_bound) // 2
    st.session_state.chat_history.append({'sender': 'assistant', 'message': f'My guess is: {st.session_state.guess}. Is it correct?'})

# print historical chat
display_chat_history()

if prompt := st.chat_input("Higher, Lower, or Yes, No, Save"):
    st.chat_message('user').write(prompt)
    st.session_state.chat_history.append({'sender': 'user', 'message': prompt})
 
    if prompt.lower() == "yes":
        st.chat_message('assistant').write('Ha Ha Ha!')
        st.session_state.chat_history.append({'sender': 'assistant', 'message': 'Ha Ha Ha!'})
    
    elif prompt.lower() == "no":
        st.chat_message('assistant').write('Is it higher or lower then the number I guessed?')
        st.session_state.chat_history.append({'sender': 'assistant', 'message': "Is it higher or lower then the number I guessed?"})
    
    else:
        if prompt == "higher":
            if st.session_state.guess + 1 > st.session_state.upper_bound:
                st.chat_message('assistant').write('You are a cheater! Ha Ha Ha.')
                st.session_state.chat_history.append({'sender': 'assistant', 'message': 'You are a cheater! Ha Ha Ha.'})
            else:
                st.session_state.lower_bound = st.session_state.guess + 1
                st.session_state.guess = (st.session_state.lower_bound + st.session_state.upper_bound) // 2
                st.session_state.chat_history.append({'sender': 'assistant', 'message': f'My guess is: {st.session_state.guess}. Is it correct?'})
                st.rerun()
        elif prompt == "lower":
            if st.session_state.guess - 1 < st.session_state.lower_bound:
                st.chat_message('assistant').write('You are a cheater! Ha Ha Ha.')
                st.session_state.chat_history.append({'sender': 'assistant', 'message': 'You are a cheater! Ha Ha Ha.'})
            else:
                st.session_state.upper_bound = st.session_state.guess - 1
                st.session_state.guess = (st.session_state.lower_bound + st.session_state.upper_bound) // 2
                st.session_state.chat_history.append({'sender': 'assistant', 'message': f'My guess is: {st.session_state.guess}. Is it correct?'})
                st.rerun()
        elif prompt == "save":
            chat_history_filename = f"chat_history_{uuid.uuid4()}.txt"
            with open(chat_history_filename, 'w') as file:
                for chat in st.session_state.chat_history:
                    file.write(f"{chat['sender']}: {chat['message']}\n")
            st.chat_message('assistant').write('Chat history saved successfully.')
            st.session_state.chat_history.append({'sender': 'assistant', 'message': 'Chat history saved successfully.'})
        else:
            st.chat_message('assistant').write('Please use Higher, Lower, or Yes, No, to navigate me!')
            st.session_state.chat_history.append({'sender': 'assistant', 'message': 'Please use Higher, Lower, or Yes, No, to navigate me!' })