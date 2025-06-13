import fitz
import pandas as pd 
import re

def get_toc(path):
    doc = fitz.open(path)
    toc = doc.get_toc()
    doc.close()

    if not toc:
        toc = manual_toc(path)
    
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

def extract_toc1(path, start):
    import fitz, re

    doc = fitz.open(path)
    total_pages = len(doc)

    toc_text = ""
    empty_pages = False
    page = start

    while page < total_pages and not empty_pages:
        page_text = doc.load_page(page).get_text()
        lines = page_text.splitlines()

        lines = [line for line in lines if not re.fullmatch(r'\s*\d+\s*', line)]
        last_lines = lines[-2:] if len(lines) >= 2 else lines

        if not any(re.search(r'(?:\.{2,}|(?:\s*\.\s*){2,}|\s{4,})\s*\d+$', line.strip()) for line in last_lines):
            empty_pages = True

        toc_text += "\n" + page_text
        page += 1

    doc.close()
    return toc_text

def extract_toc(path, start):
    doc = fitz.open(path)
    total_pages = len(doc)

    toc_text = ""
    page = start

    # Same-line TOC patterns
    patterns = [
        re.compile(r'(?:\.{2,}|(?:\s*\.\s*){2,}|\s{4,})\s*\d+$'),
        re.compile(r'^(.*?)\s+(\d+)$')
    ]

    while page < total_pages:
        page_text = doc.load_page(page).get_text()
        lines = page_text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]

        match_count = 0

        # Try same-line TOC match
        for line in lines:
            print("hi")
            for pattern in patterns:
                print("hello")
                if pattern.match(line):
                    print("bongo")
                    match_count += 1
                    break

        # Try 3-line TOC match
        for i in range(len(lines) - 2):
            print("yolo")
            if (re.fullmatch(r'\d+(\.\d+)*', lines[i]) and
                lines[i + 1] and
                re.fullmatch(r'\d+', lines[i + 2])):
                match_count += 1

        if not match_count:
            break

        toc_text += "\n" + page_text
        print(page_text)
        page += 1

    doc.close()
    return toc_text



def parse_toc(toc_text):
    
    lines = toc_text.splitlines()
    entries = []
    buffer = ""
    last_page = -1
    print("gyatt")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        buffer += " " + line
        print(repr(line))
        # match = re.match(r'^(.*?)\s*(?:\.{2,}|(?:\s*\.\s*){2,}|\s{4,})\s*(\d+)$', buffer.strip())
        # if match:
        #     print("OMG PERFECT MATCH")
        #     title = match.group(1).strip()
        #     page = int(match.group(2))

        #     if page >= last_page:
        #         section = re.match(r'^(\d+(\.\d+)*)(\s+|:)', title)
        #         level = section.group(1).count('.') + 1 if section else 1

        #         entries.append([level, title, page])
        #         last_page = page 

        #     buffer = ""
    print("rizz")
    # return entries
    return []
           

def manual_toc(path):
    start = find_toc_start(path)
    text = extract_toc(path, start)
    return parse_toc(text)
