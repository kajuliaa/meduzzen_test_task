
from uuid import uuid4
import json
import random
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.utils import SITES_DIR, LOG_FILE

from app.prompts import SECTION_PROMPT, TITLE_PROMPT,META_PROMPT
import os 

env = Environment(loader=FileSystemLoader("app/templates"))



hf_pipe = pipeline(
    "text-generation",
    model='gpt2-xl',
    
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)

llm = HuggingFacePipeline(pipeline=hf_pipe)





section_prompt = PromptTemplate(
    input_variables=["topic", "section_name", "style"],
    template=SECTION_PROMPT
)
section_chain = LLMChain(llm=llm, prompt=section_prompt)

title_prompt = PromptTemplate(
    input_variables=["topic", "style"],
    template=TITLE_PROMPT
)
title_chain = LLMChain(llm=llm, prompt=title_prompt)

meta_prompt = PromptTemplate(
    input_variables=["topic", "style", "summary"],
    template=META_PROMPT
)
meta_chain = LLMChain(llm=llm, prompt=meta_prompt)


def generate_section_content(topic: str, section_name: str, style: str) -> str:
    return section_chain.run(topic=topic, section_name=section_name, style=style).strip()


def generate_unique_title(topic: str, style: str) -> str:
    result = title_chain.run(topic=topic, style=style)
    return result.strip(' "\'')


def generate_meta_description(topic: str, style: str, sections_content: dict) -> str:
    content_summary = " ".join(sections_content.values())[:600]
    return meta_chain.run(topic=topic, style=style, summary=content_summary).strip(' "\'')


def generate_website_html(title: str, meta_desc: str, sections: dict) -> str:
    style_variant = random.choice(["light", "dark", "modern", "playful"])
    template = env.get_template(f"{style_variant}.html")
    return template.render(title=title, meta_desc=meta_desc, sections=sections)


def generate_and_store_website(title, meta_desc, sections, topic) -> dict:
    site_id = str(uuid4())
    filename = f"site_{site_id}.html"
    filepath = SITES_DIR / filename

    html = generate_website_html(title, meta_desc, sections)
    filepath.write_text(html, encoding="utf-8")

    metadata = {
        "site_id": site_id,
        "title": title,
        "meta_desc": meta_desc,
        "topic": topic,
        "sections": list(sections.keys()),
        "file_path": str(filepath),
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(LOG_FILE, "a", encoding="utf-8") as log_f:
        log_f.write(json.dumps(metadata) + "\n")

    return metadata
