import fitz
import pandas as pd 
import re

def get_toc(path):
    doc = fitz.open(path)
    toc = doc.get_toc()
    doc.close()

    if not toc:
        manual_toc(path)
    
    toc_data = []
    for level, title, page in toc:
        toc_data.append({
            "level": level,
            "title": title.strip(),
            "page": page
        })
    
    df = pd.DataFrame(toc_data)
    df.to_csv("output/toc_table.csv", index=False)
    return df


def find_toc_start(path, max_pages=20, fallback_pages=20):
    doc = fitz.open(path)
    total_pages = len(doc)

    # Initial search
    for i in range(min(max_pages, total_pages)):
        text = doc.load_page(i).get_text()
        if "contents" in text.lower():
            doc.close()
            return i
    
    # Extended search
    for i in range(max_pages, min(max_pages + fallback_pages, total_pages)):
        text = doc.load_page(i).get_text()
        if "contents" in text.lower():
            doc.close()
            return i
    doc.close()
    return None

def extract_toc(path, start):
    doc = fitz.open(path)
    total_pages = len(doc)

    toc_text = ""
    consecutives = 0

    page = start
    while (consecutives < 2 and page < total_pages):
        page_text = doc.load_page(page).get_text()
        lines = page_text.splitlines()

        if not any(re.search(r'\d+$', line.strip()) for line in lines):
            consecutives += 1
        else:
            consecutives = 0
        toc_text += "\n" + page_text
        page += 1
    return toc_text
           

def manual_toc(path):
    start = find_toc_start(path)

