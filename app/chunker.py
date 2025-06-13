import fitz 
import pandas as pd 
from toc import get_toc, find_toc_start, extract_toc

def extract_pages(path, start_page, end_page):
    doc = fitz.open(path)
    text = ""
    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text
    
if __name__ == "__main__":
    import sys
    import os 
    os.makedirs("output", exist_ok=True)
    # path = sys.argv[1]
    # start = int(sys.argv[2])
    # end = int(sys.argv[3])
    # chunk = extract_pages(path, start, end)
    # print(chunk[:1000])

    # df = get_toc("data/test3.pdf")
    # df.to_csv("output/toc.csv", index=False)
    # print("[+] TOC saved to output/toc.csv")
    
    path = "data/test6.pdf"
    start = find_toc_start(path)
    print(start)
    text = extract_toc(path, start)
    print(text)

