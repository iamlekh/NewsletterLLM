import os
import streamlit as st
from helpers import *


def main():
    """
    Main function to generate a newsletter using Streamlit UI.

    This function sets up the Streamlit UI components, including input fields,
    radio buttons, and buttons for generating the newsletter based on user inputs.
    """
    st.set_page_config(page_title="Researcher...", page_icon=":parrot:", layout="wide")

    st.header("Generate a Newsletter :parrot:")
    # Define time period options
    time_period = {"hour": "h", "day": "d", "week": "w", "month": "m", "year": "y"}
    time_period_n = {"1": 1, "2": 2, "6": 6}

    # Select time period and timeframe
    time_period_r = st.radio("TIMEFRAME", time_period, horizontal=True)
    time_period_n_r = st.radio("FOR PAST", time_period_n, horizontal=True)

    # Construct the timeframe string
    tm = f"{time_period[time_period_r]}{time_period_n[time_period_n_r]}"
    tm = "qdr:" + tm

    # Select genre/type of content
    genre = st.radio("-- 🧾 TYPE --", ["NEWS", "GENERAL"], index=1, horizontal=True)

    # Define tone options
    tone_d = {
        "Informative / Neutral Tone": "Provides factual information without bias or emotion. Focuses on delivering content in a straightforward manner.",
        "Professional / Business Tone": "Conveys professionalism and credibility. Uses formal language and business terminology. Emphasizes achievements, milestones, and business-related topics.",
        "Friendly / Conversational Tone": "Engages readers with a warm and approachable style. Uses conversational language, anecdotes, and personal stories. Encourages interaction and feedback from readers.",
        "Educational / Instructive Tone": "Focuses on educating and informing readers about specific topics or skills. Provides tutorials, guides, tips, and how-to content. Uses clear explanations and step-by-step instructions.",
        "Inspiring / Motivational Tone": "Aims to inspire, motivate, and uplift readers. Shares success stories, inspirational quotes, and positive messages. Encourages personal growth, resilience, and positivity.",
        "Humorous / Lighthearted Tone": "Adds humor, wit, and light-heartedness to engage readers. Uses jokes, puns, and humorous anecdotes. Creates a friendly and entertaining atmosphere.",
    }

    # Select tone for the newsletter
    tone = st.radio("-- 🎤 TONE --", tone_d, index=0, horizontal=False)
    tone_summary = tone_d[tone]

    # Input field for topic query
    query = st.text_input("ENTER A TOPIC...")

    # Button to trigger newsletter generation
    if st.button("GENERATE", type="primary"):
        if query:
            st.write(query)
            with st.spinner(
                f"Generating newsletter for {query} for last {time_period_n_r} {time_period_r} in a {tone}"
            ):
                st.write("Generating newsletter for: ", query)

                # Fetch search results based on genre and timeframe
                if genre == "NEWS":
                    search_results = search_serp_news(query, tm)
                elif genre == "GENERAL":
                    search_results = search_serp_general(query, tm)

                # Pick best articles' URLs from search results
                urls = pick_best_articles_urls(
                    response_json=search_results, query=query
                )
                data = extract_content_from_urls(urls)
                summaries = summarizer(data, query)
                newsletter_thread = generate_newsletter(summaries, query, tone_summary)

                # Display various sections of generated content
                with st.expander("Search Results"):
                    st.info(search_results)
                with st.expander("Best URLs"):
                    st.info(urls)
                with st.expander("Data"):
                    data_raw = " ".join(
                        d.page_content for d in data.similarity_search(query, k=4)
                    )
                    st.info(data_raw)
                with st.expander("Summaries"):
                    st.info(summaries)
                with st.expander("Newsletter:"):
                    st.code(newsletter_thread, language=None)

            st.success("Done!")


if __name__ == "__main__":
    main()
