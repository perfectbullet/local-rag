def rewrite_expand(selected_text, polish_requirements):
    system = """## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行扩写。
## 工作流程
第一步：在开始扩写之前，必须认真阅读并牢记扩写的要点。
第二步：使用Markdown格式，按照扩写的要求，对给你的文字进行扩写。"""
    user = f"""
原文字如下:
{selected_text}
扩写的要点如下:
{polish_requirements}"""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]

    parser = StrOutputParser()

    chain = llm | parser
    stream_res = chain.stream(messages)

    return stream_res



def expand():
    display()
    expand_requirements = st.session_state.expand_requirements
    selected_text = st.session_state.expand_target_content
    try:
        with st.chat_message("user"):
            st.session_state.messages.append(
                {"role": "user",
                 "content": f"针对\n```text\n{selected_text}\n```\n进行扩写，要求:{expand_requirements}"})
            st.write(f"针对\n```text\n{selected_text}\n```\n进行扩写，要求:{expand_requirements}")
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                st_all_columns = st.columns(3)
                for draft_id in range(3):
                    column_subheader = f"草稿{draft_id + 1}:"
                    st_all_columns[draft_id].subheader(column_subheader)

                polish_result = rewrite_expand(selected_text, expand_requirements)
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
        st.session_state.messages.append({"role": "assistant", "content": '草稿1：\n' + polish_full_text[0]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿2：\n' + polish_full_text[1]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿3：\n' + polish_full_text[2]})
    except AttributeError:
        st.error("expand run error")


def rewrite_polish(selected_text, polish_requirements):
    system = """## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行润色。
## 工作流程
第一步：在开始润色之前，必须认真阅读并牢记润色的要求。
第二步：使用Markdown格式，按照润色的要求，对给你的文字进行润色。
    """
    user = f"""
原文字如下:
{selected_text}
润色要求如下:
{polish_requirements}
    """

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]

    parser = StrOutputParser()

    chain = llm | parser
    stream_res = chain.stream(messages)
    # all_outputs.append(stream_res)
    return stream_res