# Streamlit Newsletter Generator

Welcome to the **Streamlit Newsletter Generator**! This application is designed to automate the creation of engaging, informative, and personalized newsletters using the power of Streamlit, LangChain, and OpenAI. Here's everything you need to know to get started and make the most out of this tool.

## Overview

The Streamlit Newsletter Generator is a user-friendly web application that allows you to:

- **Select Timeframe**: Choose how far back you want to gather content for your newsletter.
- **Specify Content Type**: Decide between news articles or general content.
- **Set the Tone**: Tailor the newsletter's tone to match your audience's expectations.
- **Input Topic**: Enter a topic of interest to focus the newsletter's content.

Once you've made your selections, the app generates a newsletter tailored to your specifications, complete with summaries, insights, and actionable advice.

## Features

### 1. **Timeframe Selection**
   - **Options**: Hour, Day, Week, Month, Year.
   - **Customization**: Users can select how many units of time to look back (e.g., 1 day, 2 weeks, etc.).

### 2. **Content Type**
   - **News**: Focuses on recent news articles related to the topic.
   - **General**: Searches for general content, which might include blogs, articles, and other online resources.

### 3. **Tone Customization**
   - **Informative/Neutral**: Straightforward, factual content.
   - **Professional/Business**: Formal language, business-oriented.
   - **Friendly/Conversational**: Warm, engaging, and personal.
   - **Educational/Instructive**: Guides, tutorials, and educational content.
   - **Inspiring/Motivational**: Uplifting and motivational messages.
   - **Humorous/Lighthearted**: Adds humor to engage readers.

### 4. **Topic Input**
   - Users can enter any topic they wish to explore in the newsletter.

### 5. **Generation Process**
   - **Search**: Utilizes GoogleSerperAPI to fetch relevant articles or content based on the selected timeframe and type.
   - **Selection**: An AI model picks the best articles from the search results.
   - **Summarization**: Extracts content from URLs, splits it into manageable chunks, and summarizes it.
   - **Newsletter Creation**: Generates a newsletter in the style of Tim Ferriss' "5-Bullet Friday", including:
     - A personal backstory to engage readers.
     - Bullet points with summaries, insights, and actionable advice.
     - Links to resources or products (with placeholders for Amazon links).
     - A clever sign-off quote related to learning or wisdom.

### 6. **User Interface**
   - **Streamlit**: Provides an intuitive UI for easy navigation and interaction.
   - **Expander Sections**: Allows users to view different stages of the newsletter generation process.

### 7. **Backend Integration**
   - **LangChain**: For orchestrating the AI chains involved in content selection, summarization, and generation.
   - **OpenAI**: Powers the language models for understanding user inputs, summarizing content, and generating the newsletter.

## How to Use

1. **Setup**: Ensure you have Streamlit, LangChain, and OpenAI libraries installed.
2. **Run the App**: Execute `streamlit run app.py` in your terminal.
3. **Configure**: Set your API keys in the environment variables or `.env` file.
4. **Interact**: Use the UI to select your preferences and generate your newsletter.

## Installation

```bash
pip install streamlit langchain openai
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key.
- `SERPER_API_KEY`: Your GoogleSerperAPI key.
- `WANDB_API_KEY`: Your Weights & Biases API key for tracking.



---
