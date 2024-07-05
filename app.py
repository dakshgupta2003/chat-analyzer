import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

# we are working in a virtual environment so this is not a predefined library

st.sidebar.title("Whatsapp Chat Analyzer")  # will create a sidebar

# now we need to write a code to upload files
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # the file we get is in byte_stream we need to convert it into string
    data = bytes_data.decode('utf-8')
    # st.text(data)# will display the info stored in data
    df = preprocessor.preprocess(data)

    st.dataframe(df)  # will display the dataframe in streamlit app

    # now we have our dataframe and we will start our analysis

    #  get unique users for dropdown
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # if it is overall then we show group analysis otherwise we show individually
    selected_user = st.sidebar.selectbox("Show Analysis wrt", options=user_list, index=0)
    # if no. of users are more the list will open upward due to lack of space
    # remove grp notification as user and sort in ascending order

    if st.sidebar.button("Show Analysis"):

        # STATS
        col1, col2, col3, col4 = st.columns(4)
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        # if someone clicks the button then only the analysis will begin
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # BUSY USER ANALYSIS (group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, percentage = helper.most_busy_users(df)
            name = x.index
            count = x.values
            fig, ax = plt.subplots()
            # fig defines the figure
            # ax defines the axes
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(name, count, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(percentage)

        # Timeline Analysis
        st.title('Timeline Analysis')
        timeline = helper.timeline_analysis(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # WORDCLOUD
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        # imshow is used to display the image
        st.pyplot(fig)

        # BAR GRAPH FOR GAALI's

        # if selected_user == 'Overall':
        #     st.title('Abusive Words')
        #     new_df = helper.abusive(df)
        #     fig, ax = plt.subplots()
        #     name = new_df['user']
        #     count = new_df['count']
        #     ax.bar(name, count, color='red')
        #     plt.xticks(rotation='vertical')
        #     st.pyplot(fig)
        #
        # if selected_user != 'Overall':
        #     st.title('Abusive Words')
        #
        #     new_df = helper.individual_abusive(selected_user, df)
        #     new_df['count'] = new_df['count'].astype(int)
        #     fig, ax = plt.subplots()
        #     word = new_df['word']
        #     count = new_df['count']
        #     ax.barh(word, count, color='red')
        #     plt.xticks(rotation='vertical')
        #     st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        # ax.barh(most_common_df[0], most_common_df[1]) # this will create a horizontal bar graph
        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        # Emoji Analysis

        df_emoji = helper.emoji_analysis(selected_user, df)
        st.title('Total Emojis Used')
        st.header(df_emoji.shape[0])

        if not df_emoji.empty:

            # st.dataframe(df_emoji)
            st.title('Emoji Analysis')
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(df_emoji)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(df_emoji[1].head(5), labels=df_emoji[0].head(5), autopct="%0.2f")
                st.pyplot(fig)


        # Word Search
        # st.title('Word Search')
        # word = st.text_input(label='', placeholder="Enter a Word")
        # # st.write(word)
        # search_df = helper.word_search(word,df)
        # fig,ax = plt.subplots()
        #
        # ax.bar(search_df['user'],search_df['count'],color='red')
        # plt.xticks(rotation = 'vertical')
        # st.pyplot(fig)
