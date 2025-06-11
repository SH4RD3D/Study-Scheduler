import fitz 
import pandas as pd 

def extract_pages(path, start_page, end_page):
    doc = fitz.open(path)
    text = ""
    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def get_toc(path):
    doc = fitz.open(path)
    toc = doc.get_toc()
    doc.close()

    if not toc:
        print("[!] No Table of Contents :(")
        return None
    
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


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    # start = int(sys.argv[2])
    # end = int(sys.argv[3])
    # chunk = extract_pages(path, start, end)
    # print(chunk[:1000])

    df = get_toc("data/TEST.pdf")

