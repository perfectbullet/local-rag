

def polish():
    display()
    polish_requirements = st.session_state.polish_requirements
    selected_text = st.session_state.polish_target_content
    try:
        with st.chat_message("user"):
            st.session_state.messages.append(
                {"role": "user",
                 "content": f"针对\n```text\n{selected_text}\n```\n进行润色，要求:{polish_requirements}"})
            st.write(f"针对\n```text\n{selected_text}\n```\n进行润色，要求:{polish_requirements}")
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                st_all_columns = st.columns(3)
                for draft_id in range(3):
                    column_subheader = f"草稿{draft_id + 1}:"
                    st_all_columns[draft_id].subheader(column_subheader)

                polish_result = rewrite_polish(selected_text, polish_requirements)
                polish_placeholder = [st_all_columns[0].empty(), st_all_columns[1].empty(), st_all_columns[2].empty()]
                polish_full_text = ['', '', '']
                choice_index = 0
                for chunk in polish_result:
                    chunk = chunk.choices
                    if chunk and chunk[0].delta.content is not None:
                        polish_full_text[choice_index % 3] += chunk[0].delta.content
                        polish_placeholder[0].markdown(polish_full_text[0], unsafe_allow_html=True)
                        polish_placeholder[1].markdown(polish_full_text[1], unsafe_allow_html=True)
                        polish_placeholder[2].markdown(polish_full_text[2], unsafe_allow_html=True)
                    choice_index += 1
        # message = {"role": "assistant", "content": polish_full_text[0]}
        st.session_state.messages.append({"role": "assistant", "content": '草稿1：\n' + polish_full_text[0]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿2：\n' + polish_full_text[1]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿3：\n' + polish_full_text[2]})
    except AttributeError:
        st.error("polish run error")