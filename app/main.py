from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from datetime import datetime
from typing import List
import json
from app.utils import LOG_FILE
from app.models import GenerateRequest, SiteMetadata
from app.generator import (
    generate_unique_title,
    generate_section_content,
    generate_meta_description,
    generate_and_store_website,
)
from app.prompts import SECTION_TEMPLATES
from app.utils import SITES_DIR

app = FastAPI()

generation_logs = []


@app.post("/generate", response_model=List[SiteMetadata])
async def generate_sites(req: GenerateRequest):
    results = []
    for _ in range(req.pages_count):
        title = generate_unique_title(req.topic, req.style)

        num_sections = min(len(SECTION_TEMPLATES), max(3, 5))  
        chosen_sections = list(sorted(SECTION_TEMPLATES))  
        # To keep randomness:
        import random
        num_sections = random.randint(3, 5)
        chosen_sections = random.sample(SECTION_TEMPLATES, num_sections)

        sections_content = {
            sec: generate_section_content(req.topic, sec, req.style)
            for sec in chosen_sections
        }

        meta_desc = generate_meta_description(req.topic, req.style, sections_content)

        metadata = generate_and_store_website(title, meta_desc, sections_content, req.topic)

        results.append(SiteMetadata(site_id=metadata["site_id"], title=title, filepath=metadata["file_path"]))

    generation_logs.append({
        "topic": req.topic,
        "pages_count": req.pages_count,
        "style": req.style,
        "timestamp": datetime.utcnow().isoformat()
    })

    return results


@app.get("/site/{site_id}", response_class=HTMLResponse)
async def get_site(site_id: str):
    filename = SITES_DIR / f"site_{site_id}.html"
    if not filename.exists():
        raise HTTPException(status_code=404, detail="Site not found")
    return filename.read_text(encoding="utf-8")


@app.get("/logs")
async def get_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = [json.loads(line) for line in f if line.strip()]
        return logs
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Log file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing log file")

