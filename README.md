
# PII redaction using a transformer-based ML model

Hugging Face offers a large number of pre-trained models for a variety of Natural Language Processing (NLP) tasks such as text classification, named entity recognition (NER), sentiment analysis, translation, summarization, question answering, and more.

Hugging Face's main contributions to the Machine Learning community are their open source libraries, such as the Transformers library, the Datasets library, and the Tokenizers library. The [Hugging Face Model](https://huggingface.co/models) Hub is an open platform where trained models can be shared with the wider community

These models are based on various state-of-the-art NLP architectures including:

- BERT (Bidirectional Encoder Representations from Transformers): A transformer-based model designed to pre-train deep bidirectional representations from an unlabeled text, which can be fine-tuned for a wide range of tasks.

- GPT-2 (Generative Pretrained Transformer 2): An autoregressive language model that uses deep learning to produce human-like text.

A "transformer" is a type of model architecture in machine learning, specifically in the field of natural language processing (NLP)

Transformers consider the entire context, both from the previous and the next words in the sentence, for capturing the context and the semantic meaning of a word (Bidirectional)

The Named Entity Recognition (NER) model used in this repository is fine-tuned on BERT. It specifically focuses on the detection of personally identifiable information (PII). This model utilizes a pre-trained BERT model, fine-tuned on a NER task for detecting personal identification information. BERT, or Bidirectional Encoder Representations from Transformers, is a transformer-based machine learning technique for natural language processing.

Applying the BERT model to NER tasks, such as detecting PII, involves training the model on a labeled dataset where each token of each sentence is assigned an entity label. The model then learns to predict these entity labels, effectively identifying which parts of the text correspond to which type of entity.

The general principle applied in this case is that the model was trained to detect PII through its understanding of the dataset it was trained on. This enables the model to identify sentences and word patterns that have the potential to be PII.

## API

**Required libraries:** Flask, transformers, tensorflow. (pip or conda as you wish, I used pip) 

 - Step 1: Load and save the transformer model in a local directory using save_hf_model.py 
 - Step 2: Create a minimal flask app, in fact you can use the above one without changing anything. Just replace your model with the one in the models directory. Recommend to test your app at this level. 
 - Step 3: Containerize the app using Dockerfile:
		  `docker build --tag mlapp . `
		  `docker run -i -p 9000:5000 mlapp` *(add -d flag to run in detach mode in the background, you can change 9000 as you need)* 
		- Check if your docker is up and running 
		  `docker ps`

| CONTAINER ID |  IMAGE |  COMMAND |  CREATED |  STATUS  | PORTS | NAMES | 
|--------------|--------|----------|----------|----------|-------|-------|
| 1fbcac69069c |  mlapp |  "python app.py" |  50 seconds ago |  Up 49 seconds |  0.0.0.0:9000->5000/tcp |  crazy_pike | 

- Check if the container is responding `curl localhost:9000 -v`
- Step 4: Test your model with make_req.py. Please note that your data should be in the correct format, for example, as you tested your model in save_hf_model.py. 
- Step 5: To stop your docker container 
			`docker stop 1fbcac69069c`

Your model is now running in your container, ready to deploy anywhere.

## OpenTelemetry collector with AI powered PII redaction processor

The Otelcol distribution below uses an AI powered PII redaction processor

https://github.com/astencel-sumo/hack23/blob/main/otelcol-processor/distro/README.md

### Pipeline

```yaml
exporters:
  debug/basic:
    verbosity: basic
  sumologic:

extensions:
  sumologic:
    collector_name: pii-redaction
    installation_token: ${SUMOLOGIC_INSTALLATION_TOKEN}

processors:
  pii_redaction:

receivers:
  filelog:
    include:
    - ./input.txt
    start_at: beginning

service:
  extensions:
  - sumologic
  pipelines:
    logs:
      exporters:
      - debug/basic
      - sumologic
      processors:
      - pii_redaction
      receivers:
      - filelog
```

### Sample Output

```
Input string:

Hello, my name is John Doe. My password is abc123. I live at 123 Apple Road, New York, NY 10001, and my phone number is (123) 456-7890. I work for Tech Corp. and my email address is john.doe@techcorp.com.


Detected entity: U-PASSWORD a (confidence: 0.845202)
Detected entity: U-PASSWORD ##b (confidence: 0.868154)
Detected entity: U-PASSWORD ##c (confidence: 0.887825)
Detected entity: U-PASSWORD ##12 (confidence: 0.973646)
Detected entity: U-PASSWORD ##3 (confidence: 0.767429)

Masked input string:
Hello, my name is **** ***. My password is ******. I live ** *** ***** ***** *** ***** ** *****, and my phone number is ***** ********. I work *** **** ***** and my email address is *********************.
```

In this example, "a" is the token and is recognized as part of a "U-PASSWORD" entity. The "U-" prefix denotes that the token forms a complete entity on its own. This is a part of the Inside-Out-Beginning (IOB) tagging system.

The score is 0.85, implying that the model is quite confident (85%) that this classification is correct. The index is the position of the token in the sequence of tokens (4, meaning it's the fifth token, as it begins from 0). start and end indicate the position of this token in the original string fed into the system.

The token "##b" that follows uses Hugging Face's way of dealing with subwords. BERT uses WordPiece tokenization. In this approach, a word may be broken down into smaller parts, with "##" signifying that this piece is part of a larger word.

#### Detected Entities

Response: [{"entity": "U-PASSWORD", "score": 0.8452024459838867, "index": 4, "word": "a", "start": 15, "end": 16}, {"entity": "U-PASSWORD", "score": 0.8681536912918091, "index": 5, "word": "##b", "start": 16, "end": 17}, {"entity": "U-PASSWORD", "score": 0.8878251314163208, "index": 6, "word": "##c", "start": 17, "end": 18}, {"entity": "U-PASSWORD", "score": 0.9736464619636536, "index": 7, "word": "##12", "start": 18, "end": 20}, {"entity": "U-PASSWORD", "score": 0.7674290537834167, "index": 8, "word": "##3", "start": 20, "end": 21}]

```
Detected entity: B-PER John (confidence: 0.997769)
Detected entity: L-PER Do (confidence: 0.999665)
Detected entity: U-PER ##e (confidence: 0.999339)
Detected entity: U-O a (confidence: 0.977393)
Detected entity: U-O ##b (confidence: 0.995046)
Detected entity: U-O ##c (confidence: 0.993210)
Detected entity: U-O ##12 (confidence: 0.991082)
Detected entity: U-O ##3 (confidence: 0.988609)
Detected entity: I-LOC at (confidence: 0.568763)
Detected entity: I-LOC 123 (confidence: 0.996455)
Detected entity: I-LOC Apple (confidence: 0.999946)
Detected entity: I-LOC Road (confidence: 0.999780)
Detected entity: I-LOC , (confidence: 0.999780)
Detected entity: I-LOC New (confidence: 0.999429)
Detected entity: I-LOC York (confidence: 0.999926)
Detected entity: I-LOC , (confidence: 0.999909)
Detected entity: I-LOC NY (confidence: 0.999929)
Detected entity: L-LOC 1000 (confidence: 0.999734)
Detected entity: U-LOC ##1 (confidence: 0.996582)
Detected entity: B-O ( (confidence: 0.960983)
Detected entity: I-O 123 (confidence: 0.995478)
Detected entity: I-O ) (confidence: 0.999848)
Detected entity: I-O 45 (confidence: 0.999800)
Detected entity: I-O ##6 (confidence: 0.999726)
Detected entity: I-O - (confidence: 0.999760)
Detected entity: L-O 78 (confidence: 0.999724)
Detected entity: U-O ##90 (confidence: 0.999882)
Detected entity: B-ORG for (confidence: 0.709578)
Detected entity: B-ORG Tech (confidence: 0.997056)
Detected entity: L-ORG Corp (confidence: 0.998827)
Detected entity: U-ORG . (confidence: 0.997981)
Detected entity: U-O j (confidence: 0.998731)
Detected entity: U-O ##oh (confidence: 0.997377)
Detected entity: U-O ##n (confidence: 0.996498)
Detected entity: U-O . (confidence: 0.995999)
Detected entity: U-O do (confidence: 0.997692)
Detected entity: U-O ##e (confidence: 0.998086)
Detected entity: U-O @ (confidence: 0.985402)
Detected entity: U-O tech (confidence: 0.997423)
Detected entity: U-O ##cor (confidence: 0.999028)
Detected entity: U-O ##p (confidence: 0.999017)
Detected entity: U-O . (confidence: 0.998307)
Detected entity: U-O com (confidence: 0.996966)
```

In the detected entities list, each line represents a detected entity from the text, along with the confidence score. The entity is prefixed with one of three tags:

B: Beginning of the entity
I: Inside of the entity
L: Last token of the entity
U: A single-token entity
O: A non-entity token

Detected entity: B-PER John (confidence: 0.997769) means that 'John' is detected as the 'beginning' (B-) of a person (PER) entity with a confidence score of 0.997769.