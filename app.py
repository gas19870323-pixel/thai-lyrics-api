from flask import Flask, request, jsonify
from flask_cors import CORS
from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate import romanize

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_lyrics():
    data = request.json
    text = data.get('text', '')
    
    lines = text.strip().split('\n')
    result = []
    
    for line in lines:
        if not line.strip():
            result.append([])
            continue
            
        words = word_tokenize(line.strip(), engine="newmm")
        line_data = []
        
        for w in words:
            if w.strip():
                rtgs = romanize(w, engine="royal")
                line_data.append({
                    "thai": w,
                    "roman": rtgs,
                    "chinese": "-" # 這裡留空，全部交給網頁端補上
                })
        result.append(line_data)
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
