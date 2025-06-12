import fitz 
import pandas as pd 
import toc

def extract_pages(path, start_page, end_page):
    doc = fitz.open(path)
    text = ""
    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text
    
if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    # start = int(sys.argv[2])
    # end = int(sys.argv[3])
    # chunk = extract_pages(path, start, end)
    # print(chunk[:1000])

    df = get_toc("data/TEST.pdf")

