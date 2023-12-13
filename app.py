from flask import Flask, request, jsonify
import numpy as np
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def makecalc():
    if request.method=="POST":
        print("request received")
        data = request.get_json()
        print("data ---- > ", data)
        # prediction = np.array2string(model.predict(data))
        results = classifier(data)
        return str(results)
    return "Not a proper request method or data"


if __name__ == '__main__':

    model_path = './models/transformers/' 
    model = AutoModelForTokenClassification.from_pretrained(model_path, local_files_only=True)
    print("----------- transformer model loaded ------------")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    print("----------- transformer tokenizer loaded ------------")
    classifier = pipeline('token-classification', model=model, tokenizer=tokenizer)
    print(classifier)

    app.run(debug=False, host='0.0.0.0')

