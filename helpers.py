import os
from dotenv import find_dotenv, load_dotenv
import openai
import json
import requests
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks import wandb_tracing_enabled

os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
os.environ["WANDB_PROJECT"] = "langchain-tracing"


openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERPER_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")


load_dotenv(find_dotenv())


SEARCH_QUERY = 6


embeddings = OpenAIEmbeddings()


def search_serp_news(query, tm):
    """
    The function `search_serp_news` uses the GoogleSerperAPIWrapper to search for news articles related
    to a given query within a specified time frame.

    Args:
      query: The `query` parameter in the `search_serp_news` function is the search query that you want
    to use to search for news articles. It is the term or phrase that you want to look up in the news
    search.
      tm: The `tm` parameter in the `search_serp_news` function likely stands for "time range" or "time
    filter". It is used to specify a specific time frame for the search results. This parameter allows
    you to filter the news articles based on when they were published or last updated. It

    Returns:
      The function `search_serp_news` is returning the JSON response from the Google Search Engine
    Results Page (SERP) for news articles related to the given query and time range.
    """
    search_n = GoogleSerperAPIWrapper(k=SEARCH_QUERY, type="news", tbs=tm)
    response_json_n = search_n.results(query)
    return response_json_n


def search_serp_general(query, tm):
    """
    The function `search_serp_general` uses the GoogleSerperAPIWrapper to retrieve search results based
    on a query and time parameter.

    Args:
      query: The `query` parameter in the `search_serp_general` function represents the search query
    that you want to perform on the search engine. It is the term or phrase that you want to look up in
    the search results.
      tm: The `tm` parameter in the `search_serp_general` function likely stands for "time range" or
    "time filter". It is used to specify a specific time range for the search results. This parameter
    allows you to filter search results based on when the content was published or last updated.

    Returns:
      The function `search_serp_general` returns the JSON response from the Google Search Engine Results
    Page (SERP) API for the given query and time range.
    """
    search = GoogleSerperAPIWrapper(k=SEARCH_QUERY, type="search", tbs=tm)
    response_json = search.results(query)
    return response_json


def pick_best_articles_urls(response_json, query):
    # turn json to string
    response_str = json.dumps(response_json)

    # create llm to choose best articles
    llm = ChatOpenAI(temperature=0.7)  # , callbacks=callbacks)
    template = """ 
      You are a world class journalist, researcher, tech, Software Engineer, Developer, newsletter writer and a online content creator
      , you are amazing at finding the most interesting and relevant, useful articles in certain topics.
      
      QUERY RESPONSE:{response_str}
      
      Above is the list of search results for the query {query}.
      
      Please choose the best 3-5 articles from the list and return ONLY an array of the urls.  
      Do not include anything else -
      return ONLY an array of the urls. 
      Also make sure the articles are recent and not too old.
      If the file, or URL is invalid, show www.google.com.
    """
    prompt_template = PromptTemplate(
        input_variables=["response_str", "query"], template=template
    )
    article_chooser_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    urls = article_chooser_chain.run(response_str=response_str, query=query)

    # Convert string to list
    url_list = json.loads(urls)
    return url_list


def extract_content_from_urls(urls):
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    docs = text_splitter.split_documents(data)
    db = FAISS.from_documents(docs, embeddings)

    return db


def summarizer(db, query, k=2):

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)  # , callbacks=callbacks)
    template = """
       {docs}
        As a world class journalist, researcher, tech, Software Engineer, Developer, newsletter writer and a online content creator, 
        you will summarize the text above in order to create a 
        newsletter around {query}.
        This newsletter will be sent as an email.  The format is going to be like
        Tim Ferriss' "5-Bullet Friday" newsletter.
        
        Please follow all of the following guidelines:
        1/ Make sure the content is engaging, informative with good data
        2/ Make sure the conent is not too long, it should be the size of a nice newsletter bullet point and summary
        3/ The content should address the {query} topic very well
        4/ The content needs to be good and informative
        5/ The content needs to be written in a way that is easy to read, digest and understand
        6/ The content needs to give the audience actinable advice & insights including resouces and links if necessary
        
        SUMMARY:
    """
    prompt_template = PromptTemplate(
        input_variables=["docs", "query"], template=template
    )

    summarizer_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    response = summarizer_chain.run(docs=docs_page_content, query=query)

    return response.replace("\n", "")  # reponse, docs


def generate_newsletter(summaries, query, tone_summary):
    """
    This Python function generates a newsletter based on provided summaries, a query, and a tone
    summary, following specific guidelines and using a language model to create engaging and informative
    content.

    Args:
      summaries: It seems like the code snippet you provided is a function called `generate_newsletter`
    that takes in three parameters: `summaries`, `query`, and `tone_summary`. The function appears to
    generate a newsletter based on the provided summaries, query, and tone summary.
      query: The `query` parameter in the `generate_newsletter` function is the topic or subject that
    the newsletter will be focused on. It serves as the central theme around which the newsletter
    content will revolve.
      tone_summary: The `tone_summary` parameter is used to specify the tone in which the newsletter
    should be written. It guides the writing style and voice of the newsletter, helping to set the
    overall mood and approach for the content. For example, the tone could be casual, professional,
    informative, humorous, or any

    Returns:
      The function `generate_newsletter` returns a generated newsletter based on the provided summaries,
    query, and tone summary. The newsletter is written in a specific format with guidelines to follow,
    including engaging and informative content related to the query topic. The function uses a language
    model to generate the newsletter text.
    """
    summaries_str = str(summaries)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)  # , callbacks=callbacks)
    template = """
    {summaries_str}
        As a world class journalist, researcher, tech, Software Engineer, Developer, newsletter writer and a online content creator,
        you'll use the text above as the context about {query}
        to write an excellent newsletter to be sent to subscribers about {query}.
        
        This newsletter will be sent as an email.  The format is going to be like
        Tim Ferriss' "5-Bullet Friday" newsletter.
        
        Make sure to write it in {tone_summary} - no "Dear" or any other formalities.  
        Start the newsletter with
        `Hi All!
          Here is your weekly dose of the Newsletter, a list of what I find interesting
          and worth and exploring.`
          
        Make sure to also write a backstory about the topic - make it personal, engaging and lighthearted before
        going into the meat of the newsletter.
        
        Please follow all of the following guidelines:
        1/ Make sure the content is engaging, informative with good data
        2/ Make sure the conent is not too long, it should be the size of a nice newsletter bullet point and summary
        3/ The content should address the {query} topic very well
        4/ The content needs to be good and informative
        5/ The content needs to be written in a way that is easy to read, digest and understand
        6/ The content needs to give the audience actinable advice & insights including resouces and links if necessary.
        
        If there are books, or products involved, make sure to add amazon links to the products or just a link placeholder.
        
        As a signoff, write a clever quote related to learning, general wisdom, living a good life.  Be creative with this one - and then,
        Sign with "-AI Generated." IN NEW LINE.
        NEWSLETTER-->:
    """
    prompt_template = PromptTemplate(
        input_variables=["summaries_str", "query", "tone_summary"], template=template
    )
    news_letter_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    news_letter = news_letter_chain.predict(
        summaries_str=summaries_str, query=query, tone_summary=tone_summary
    )

    return news_letter
