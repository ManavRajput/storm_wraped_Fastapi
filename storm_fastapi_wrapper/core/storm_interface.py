import logging
import dspy
from utils.patch_file_writes import get_memory_file_log
from knowledge_storm.storm_wiki.modules.knowledge_curation import StormKnowledgeCurationModule
from knowledge_storm.storm_wiki.modules.outline_generation import StormOutlineGenerationModule
from knowledge_storm.storm_wiki.modules.article_generation import StormArticleGenerationModule
from knowledge_storm.storm_wiki.modules.article_polish import StormArticlePolishingModule
from knowledge_storm.storm_wiki.modules.callback import BaseCallbackHandler
from dotenv import load_dotenv
import os
from utils.mock_retriever import MockRetriever
import google.generativeai as genai  # Import Gemini

import logging
from typing import Dict, Union

logger = logging.getLogger(__name__)
import builtins

original_open = open


def block_writes(path, mode='r', *args, **kwargs):
    if 'w' in mode or 'a' in mode:
        raise RuntimeError(f"File writes are blocked: attempted to write to '{path}'")
    return original_open(path, mode, *args, **kwargs)


builtins.open = block_writes

# Load environment variables from .env file
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Make sure this matches your .env
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite-001')


# Create a DSPy LM wrapper for Gemini
class GeminiLM(dspy.LM):
    def __init__(self, model):
        super().__init__("gemini-pro")
        self.model = model

    def basic_request(self, prompt, **kwargs):
        response = self.model.generate_content(prompt)
        return response.text

    def __call__(self, prompt, **kwargs):
        return self.basic_request(prompt, **kwargs)


# Initialize the language model engine with Gemini
LLM_ENGINE = GeminiLM(gemini_model)

# Instantiate mock retriever
retriever = MockRetriever()
callback_handler = BaseCallbackHandler()

# Initialize STORM pipeline modules (rest of your code remains the same)
knowledge_curation = StormKnowledgeCurationModule(
    retriever=retriever,
    persona_generator=None,
    conv_simulator_lm=LLM_ENGINE,
    question_asker_lm=LLM_ENGINE,
    max_search_queries_per_turn=3,
    search_top_k=5,
    max_conv_turn=3,
    max_thread_num=2,
)

outline_generation = StormOutlineGenerationModule(outline_gen_lm=LLM_ENGINE)
article_generation = StormArticleGenerationModule(article_gen_lm=LLM_ENGINE)
article_polishing = StormArticlePolishingModule(
    article_gen_lm=LLM_ENGINE,
    article_polish_lm=LLM_ENGINE,
)

def run_storm_query(params: dict) -> str:
    topic = params.get("query", "").strip()
    if not topic:
        return "Error: Empty query"

    logging.info(f"[STORM] Running pipeline for topic: {topic}")

    try:
        # Step 1: Knowledge Curation
        info = knowledge_curation.research(
            topic=topic,
            ground_truth_url="",
            callback_handler=callback_handler
        )
        logging.info("Knowledge curation complete.")

        # Step 2: Outline Generation
        outline = outline_generation.generate_outline(topic, info)
        logging.info("Outline generation complete.")

        # Step 3: Article Draft
        draft = article_generation.generate_article(topic, info, outline)
        logging.info("Article draft complete.")

        # Step 4: Article Polishing
        final_article = article_polishing.polish_article(topic, draft)
        logging.info("Article polishing complete.")

        return final_article.to_string()
    except Exception as e:
        logging.exception("Error running STORM pipeline")
        return f"Pipeline Error: {str(e)}"


def run_storm_query_stream(params: dict):
    topic = params.get("query", "").strip()
    if not topic:
        yield "Error: Empty query"
        return

    logging.info(f"[STORM STREAM] Running pipeline for topic: {topic}")

    try:
        yield "🔍 Curating knowledge...\n"
        info = knowledge_curation.research(
            topic=topic,
            ground_truth_url="",
            callback_handler=callback_handler
        )

        yield "🧠 Generating outline...\n"
        outline = outline_generation.generate_outline(topic, info)

        yield "📝 Drafting article...\n"
        draft = article_generation.generate_article(topic, info, outline)

        yield "✨ Polishing article...\n"
        final_article = article_polishing.polish_article(topic, draft)

        yield "\n✅ Done!\n\n"
        yield final_article.to_string()

    except Exception as e:
        logging.exception("Streaming pipeline error")
        yield f"\n❌ Pipeline Error: {str(e)}"


def get_memory_file_log():
    return get_memory_file_log()
