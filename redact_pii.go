package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

type Entity struct {
	Entity string  `json:"entity"`
	Score  float64 `json:"score"`
	Index  int     `json:"index"`
	Word   string  `json:"word"`
	Start  int     `json:"start"`
	End    int     `json:"end"`
}

func main() {
	// inputString := `Hello, my name is John Doe. My password is abc123. I live at 123 Apple Road, New York, NY 10001, and my phone number is (123) 456-7890. I work for Tech Corp. and my email address is john.doe@techcorp.com.`
	inputString := `My password is abc123`
	fmt.Println("Input string:\n" + inputString)

	jsonValue, _ := json.Marshal(inputString)

	resp, err := http.Post("http://localhost:9000", "application/json", bytes.NewBuffer(jsonValue))

	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	// Print the body for debugging
	fmt.Println("Response: " + string(body))
	var entities []Entity
	err = json.Unmarshal(body, &entities)
	if err != nil {
		fmt.Println("Error parsing JSON response")
		panic(err)
	}

	for _, entity := range entities {
		fmt.Printf("Detected entity: %s %s (confidence: %f)\n", entity.Entity, entity.Word, entity.Score)
		mask := strings.Repeat("*", len(inputString[entity.Start:entity.End]))
		inputString = inputString[:entity.Start] + mask + inputString[entity.End:]
	}

	fmt.Println("\nMasked input string:")
	fmt.Println(inputString)
}
