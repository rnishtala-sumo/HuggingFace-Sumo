
# HuggingFace Sumologic

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

## Client program

```
go run redact_pii.go
```

### Output

```
go run redact_pii.go
Input string:
My password is abc123
Response: [{"entity": "U-PASSWORD", "score": 0.8452024459838867, "index": 4, "word": "a", "start": 15, "end": 16}, {"entity": "U-PASSWORD", "score": 0.8681536912918091, "index": 5, "word": "##b", "start": 16, "end": 17}, {"entity": "U-PASSWORD", "score": 0.8878251314163208, "index": 6, "word": "##c", "start": 17, "end": 18}, {"entity": "U-PASSWORD", "score": 0.9736464619636536, "index": 7, "word": "##12", "start": 18, "end": 20}, {"entity": "U-PASSWORD", "score": 0.7674290537834167, "index": 8, "word": "##3", "start": 20, "end": 21}]
Detected entity: U-PASSWORD a (confidence: 0.845202)
Detected entity: U-PASSWORD ##b (confidence: 0.868154)
Detected entity: U-PASSWORD ##c (confidence: 0.887825)
Detected entity: U-PASSWORD ##12 (confidence: 0.973646)
Detected entity: U-PASSWORD ##3 (confidence: 0.767429)

Masked input string:
My password is ******
```
