SECTION_TEMPLATES = [
    "Introduction",
    "Use Cases",
    "Technical Details",
    "Tools or Libraries",
    "Summary",
    "Call to Action",
]

SECTION_PROMPT = """
<s>[INST] 
You are writing a professional blog post in a {style} tone.

Write a section titled: "{section_name}"  
Topic: "{topic}"

Requirements:
- Write 7–10 informative, logically connected sentences.
- Be clear, concise, and avoid repetition or rhetorical questions.
- End the section with a strong concluding sentence.
[/INST]


"""

TITLE_PROMPT = """
<s>[INST] 
Generate a catchy website title in a {style} tone.

Topic: "{topic}"

Requirements:
- Keep the title between 3 and 7 words.
- Make it original, engaging, and clearly related to the topic.
[/INST]

"""

META_PROMPT = """
<s>[INST] 
Write an SEO-friendly meta description (max 155 characters) in a {style} tone.

Topic: "{topic}"  
Content Summary: {summary}

Requirements:
- Clearly summarize the content.
- Include the main keyword: "{topic}".
- Make it attention-grabbing and useful for search engines.
- Stay within 155 characters.
[/INST]


"""
