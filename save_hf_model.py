#%% import required libraries
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification    
model_path = 'models/transformers/' # will be created automatically if not exists

#%% download and save the model to local directory
model_name = "ArunaSaraswathy/bert-finetuned-ner-pii"

print("----------- transformer model loaded ------------")
tokenizer = AutoTokenizer.from_pretrained("ArunaSaraswathy/bert-finetuned-ner-pii")
model = AutoModelForTokenClassification.from_pretrained("ArunaSaraswathy/bert-finetuned-ner-pii")
print("----------- transformer tokenizer loaded ------------")
classifier = pipeline('token-classification', model=model, tokenizer=tokenizer)
classifier.save_pretrained(model_path)
#%% test if it works
classifier(["good"]) 

#%% load model from local directory if it works
model = AutoModelForTokenClassification.from_pretrained(model_path, local_files_only=True)
print("-----------  model loaded from local dir ------------")
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
print("-----------  tokenizer loaded from local dir ------------")
classifier = pipeline('token-classification', model=model, tokenizer=tokenizer)

classifier(["good"]) 

# %%
