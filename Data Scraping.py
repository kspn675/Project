import streamlit as st
import praw
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import time
import plotly.express as px

# Load environment variables from the .env file
load_dotenv()

# Title and description
st.title("Reddit Data Scraper 📄")
st.markdown("""
Welcome to the **Reddit Data Scraper**! 🚀  
Fetch and analyze posts from any Reddit user effortlessly.  
Fill in the details in the sidebar and start scraping!  
""")

# Sidebar inputs
st.sidebar.header("Input Options 🔒")
st.sidebar.markdown("---")

st.sidebar.markdown("### User Details 📝")
username = st.sidebar.text_input("Enter the Reddit Username:", help="The username whose posts you want to scrape.")

# Scrape button
if st.sidebar.button("Scrape Reddit Data 🚀", help="Click to start scraping data"):
    if username:
        st.write(f"Fetching posts from Reddit user: **{username}**")
        try:
            # Initialize Reddit client with provided credentials
            reddit = praw.Reddit(
                client_id="DXn4zA4ndLlPL76BWusSdQ",
                client_secret="xxfD_L4vvaa7dTiZzQlT6Ex2eZHJRQ",
                user_agent="K_ScraperApp/1.0 by Mysterious-List-186"
            )

            # Fetch user submissions
            user = reddit.redditor(username)
            submissions = user.submissions.new(limit=100)  # Fetch the latest 100 posts

            # Collect post data
            posts = []
            with st.spinner("Scraping data... Please wait!"):
                for submission in submissions:
                    posts.append({
                        "title": submission.title,
                        "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                        "score": submission.score,
                        "comments": submission.num_comments,
                        "url": submission.url
                    })
                time.sleep(2)  # Simulate loading time

            # Convert to a DataFrame
            if posts:
                df = pd.DataFrame(posts)

                # Enhanced Visualization Section
                st.subheader("Data Insights 📊")
                st.markdown("### Post Performance Overview")

                # Dot chart for Post Scores
                st.markdown("#### Post Scores")
                fig_score = px.scatter(
                    df,
                    x="title",
                    y="score",
                    title="Dot Chart of Post Scores",
                    labels={"score": "Scores", "title": "Post Titles"},
                    template="plotly_white",
                    color="score",  # Color points based on score for better visibility
                    color_continuous_scale="Viridis",
                    height=400
                )
                st.plotly_chart(fig_score, use_container_width=True)

                # Dot chart for Comments
                st.markdown("#### Post Comments")
                fig_comments = px.scatter(
                    df,
                    x="title",
                    y="comments",
                    title="Dot Chart of Post Comments",
                    labels={"comments": "Number of Comments", "title": "Post Titles"},
                    template="plotly_white",
                    color="comments",  # Color points based on comments
                    color_continuous_scale="Cividis",
                    height=400
                )
                st.plotly_chart(fig_comments, use_container_width=True)

                # Display Data in Tabs
                st.subheader("Scraped Data 📋")
                tab1, tab2 = st.tabs(["Table View", "Raw JSON"])
                with tab1:
                    st.table(df)
                with tab2:
                    st.json(df.to_dict(orient="records"))

                # Save Data as CSV
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_filename = f"{username}_reddit_data_{timestamp}.csv"
                csv_filepath = os.path.join("scraped_data", csv_filename)

                os.makedirs("scraped_data", exist_ok=True)
                df.to_csv(csv_filepath, index=False)

                # Download Button
                st.download_button(
                    label="Download Data as CSV 📥",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name=csv_filename,
                    mime="text/csv"
                )

                st.success(f"✅ Successfully scraped and saved data for user: {username}")
            else:
                st.warning("No posts were found for the specified Reddit user.")
        except Exception as e:
            st.error(f"Failed to fetch posts: {e}")
    else:
        st.warning("Please provide the Reddit Username.")

# Footer
st.markdown("""
---
Built with ❤️ by Kashish ([GitHub](https://github.com/kspn675/)).  
""")
