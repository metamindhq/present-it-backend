def get_dynamic_slide_gen_system_message(
        topic: str,
        genre: str,
        theme: str,
        summary: str,
        offset: int,
        total_slides: int
):
    print(topic)
    return f"""
You are a bot that creates presentation slides. Follow the instructions exactly as given. 

- **Focus strictly on the specified topic. Do not include irrelevant or historical information unless explicitly asked.**
- **Each slide must cover a different specific topic directly related to the main subject.**

Genre: {genre}

Previous Slides Content:

{summary}

**Respond with content for slide:** {offset} of {total_slides}

Follow the below provided JSON format for the slide content:
{{
  "title": "string",  # strictly 2-5 words, specific to the team or topic
  "subtitle": "string",  # 4-7 words, relevant to the slide's focus
  "content": "string",  # 30-40 words, detailed and specific to the team's involvement in F1
  "bullet_points": [
    "string",  # 2-3 points, 10-20 words each, directly related to the team or topic
  ],
  "speaker_note": "string",  # Brief, relevant note that strictly explains the slide content
  "summary": "string",  # 30-40 words, summarizes the team’s role in F1, no unrelated history
  "image_generation_prompt": "string"  # 80-100 words, describing a visual theme relevant to the team, based on {theme}
}}

User Prompt: {topic}
"""
