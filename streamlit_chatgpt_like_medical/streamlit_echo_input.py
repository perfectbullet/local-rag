import streamlit as st


st.title('观想医疗')

# init chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# display history
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'], unsafe_allow_html=True)


# react to user input
if prompt := st.chat_input('输入你的问题'):
    # display user message
    with st.chat_message('user'):
        st.markdown(prompt, unsafe_allow_html=True)
    # add message to history
    st.session_state['messages'].append({'role':'user', 'content':prompt})

    response = f'Echo {prompt}'
    # display assistant response
    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)
    st.session_state['messages'].append({'role':'assistant', 'content':response})
