import streamlit as st
import preprocessor
import helper

import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Segoe UI Emoji' 
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
 # or 'Noto Color Emoji'


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media", num_media)
        col4.metric("Links", num_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity maps
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Busy Day")
            day_activity = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(day_activity.index, day_activity.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            month_activity = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_activity.index, month_activity.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heatmap
        st.title("Weekly Activity Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        if not heatmap.empty:
            fig, ax = plt.subplots()
            sns.heatmap(heatmap, ax=ax)
            st.pyplot(fig)
        else:
            st.write("Not enough data for heatmap.")

        # Busiest users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("WordCloud")
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Words")
        common_words = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_words['word'], common_words['count'])
        plt.xticks(rotation='horizontal')
        st.pyplot(fig)

        # Emoji analysis
        st.title("Emoji Analysis")
        emojis = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emojis)
        with col2:
            if not emojis.empty:
                fig, ax = plt.subplots()
                ax.pie(emojis['count'].head(), labels=emojis['emoji'].head(), autopct="%0.2f")
                st.pyplot(fig)
            else:
                st.write("No emojis found.")
