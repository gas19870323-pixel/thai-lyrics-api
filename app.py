from flask import Flask, request, jsonify
from flask_cors import CORS
from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate import romanize
from deep_translator import GoogleTranslator

app = Flask(__name__)
# 允許跨網域請求，這樣 Google Apps Script 才能順利呼叫你的 API
CORS(app) 

# 建立一個名為 /process 的接收端點 (Endpoint)
@app.route('/process', methods=['POST'])
def process_lyrics():
    data = request.json
    text = data.get('text', '')
    
    # 準備 Google 翻譯器
    translator = GoogleTranslator(source='th', target='zh-TW')
    lines = text.strip().split('\n')
    result = []
    
    for line in lines:
        if not line.strip():
            result.append([])
            continue
            
        # 使用 pythainlp 進行精準斷詞
        words = word_tokenize(line.strip(), engine="newmm")
        line_data = []
        
        for w in words:
            if w.strip():
                # 轉寫為 RTGS 羅馬拼音
                rtgs = romanize(w, engine="royal")
                # 取得中文翻譯
                try:
                    zh = translator.translate(w)
                except:
                    zh = "-"
                    
                line_data.append({
                    "thai": w,
                    "roman": rtgs,
                    "chinese": zh
                })
        result.append(line_data)
        
    # 將處理完的陣列轉換為 JSON 格式回傳
    return jsonify(result)

if __name__ == '__main__':
    # 啟動伺服器
    app.run(host='0.0.0.0', port=5000)