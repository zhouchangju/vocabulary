import fitz
import pytesseract
from PIL import Image
import numpy as np
import re
import os

# 获取当前脚本所在目录的父目录，以正确定位 data 文件夹
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_v6(pdf_path, output_file, start_page=10, end_page=None):
    doc = fitz.open(pdf_path)
    if end_page is None: end_page = len(doc)
    
    all_words = []
    mat = fitz.Matrix(3.0, 3.0) 
    
    print("Starting Final High-Precision Extraction (V6 Precise)...")
    
    for page_num in range(start_page, end_page):
        try:
            page = doc.load_page(page_num)
            clip_rect = fitz.Rect(0, 0, 280, 841)
            pix = page.get_pixmap(matrix=mat, clip=clip_rect)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            arr = np.array(img)
            mask = (arr[:,:,0] < 125) & (arr[:,:,1] < 125) & (arr[:,:,2] < 125)
            clean = np.ones_like(arr) * 255
            clean[mask] = 0
            clean_img = Image.fromarray(clean)
            
            data = pytesseract.image_to_data(clean_img, output_type=pytesseract.Output.DATAFRAME)
            data = data[data.text.notna()]
            data['text'] = data['text'].astype(str).str.strip()
            data['clean'] = data['text'].apply(lambda x: re.sub(r'[^a-zA-Z-]', '', x))
            
            if data.empty: continue
            
            candidates = data[(data.left >= 200) & (data.height >= 30)]
            if candidates.empty: continue
            
            candidates = candidates.sort_values(['top', 'left'])
            
            page_words = []
            if not candidates.empty:
                current_word = ""
                last_top = -100
                
                for _, row in candidates.iterrows():
                    if abs(row['top'] - last_top) < 20:
                        current_word += row['clean']
                    else:
                        if len(current_word) >= 3:
                            page_words.append(current_word.lower())
                        current_word = row['clean']
                    last_top = row['top']
                
                if len(current_word) >= 3:
                    page_words.append(current_word.lower())

            seen_page = set()
            for w in page_words:
                if w not in seen_page:
                    all_words.append(w)
                    seen_page.add(w)
                    if len(seen_page) >= 6: break
            
            if (page_num + 1) % 50 == 0:
                print("Progress: {}/{} | Extracted: {}".format(page_num+1, end_page, len(all_words)))
                
        except Exception:
            pass

    doc.close()
    
    unique = []
    seen = set()
    for w in all_words:
        if w not in seen and len(w) >= 3 and re.search(r'[aeiouy]', w):
            unique.append(w)
            seen.add(w)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in unique:
            f.write(word + "
")
            
    return unique

if __name__ == "__main__":
    pdf_path = os.path.join(BASE_DIR, "data/vocabulary/学而思国际托福改革后一站式精品词书.pdf")
    output_file = os.path.join(BASE_DIR, "data/vocabulary/TOEFL_V6_FINAL.txt")
    
    if os.path.exists(pdf_path):
        words = extract_v6(pdf_path, output_file)
        print("Success! {} words saved to {}.".format(len(words), output_file))
    else:
        print("PDF not found at: " + pdf_path)
