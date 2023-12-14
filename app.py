from flask import Flask, request, jsonify
import numpy as np
import json
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

app = Flask(__name__)

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

@app.route('/', methods=['GET', 'POST'])
def makecalc():
    if request.method=="POST":
        print("request received")
        data = request.get_json()
        print("data ---- > ", data)
        # prediction = np.array2string(model.predict(data))
        results = classifier(data)
        return json.dumps(results, cls=Encoder)
    return "Not a proper equest method or data"


if __name__ == '__main__':

    model_path = './models/transformers/' 
    model = AutoModelForTokenClassification.from_pretrained(model_path, local_files_only=True)
    print("----------- transformer model loaded ------------")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    print("----------- transformer tokenizer loaded ------------")
    classifier = pipeline('token-classification', model=model, tokenizer=tokenizer)
    print(classifier)

    app.run(debug=False, host='0.0.0.0')

