import streamlit as st,preprocessor,helper

st.sidebar.title("Whatsapp Chat Analyzer")
upload_file=st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    #fetch unique user
    user_list = df['user'].unique().tolist()

    #user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "overall")
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)
    if st.sidebar.button("show analysis"):
        num_messages,words,num_media_messages=helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)

