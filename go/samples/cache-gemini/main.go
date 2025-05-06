// Copyright 2025 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"context"
	"errors"
	"log"
	"os"

	"github.com/firebase/genkit/go/ai"
	"github.com/firebase/genkit/go/genkit"
	"github.com/firebase/genkit/go/plugins/googlegenai"
)

// duneQuestionInput is a question about Dune.
type duneQuestionInput struct {
	Question string `json:"question"`
	FilePath string `json:"path"`
}

func main() {
	ctx := context.Background()
	g, err := genkit.Init(ctx,
		genkit.WithDefaultModel("googleai/gemini-1.5-flash"),
		genkit.WithPlugins(&googlegenai.GoogleAI{}),
	)
	if err != nil {
		log.Fatal(err)
	}

	genkit.DefineFlow(g, "duneFlowGeminiAI", func(ctx context.Context, input *duneQuestionInput) (string, error) {
		prompt := "What is the text I provided you with?"
		if input == nil {
			return "", errors.New("empty flow input, provide at least a source file to read")
		}
		if len(input.Question) > 0 {
			prompt = input.Question
		}

		textContent, err := os.ReadFile(input.FilePath)
		if err != nil {
			return "", err
		}

		// generate a request with a large text content to be cached
		resp, err := genkit.Generate(ctx, g, ai.WithConfig(&googlegenai.GeminiConfig{
			Temperature: 0.7,
			Version:     "gemini-1.5-flash-001",
		}),
			ai.WithMessages(
				ai.NewUserTextMessage(string(textContent)).WithCacheTTL(360),
			),
			ai.WithPrompt(prompt),
		)
		if err != nil {
			return "", nil
		}

		// use previous messages to keep the conversation going and keep
		// asking questions related to the large content that was cached
		resp, err = genkit.Generate(ctx, g, ai.WithConfig(&googlegenai.GeminiConfig{
			Temperature: 0.7,
			Version:     "gemini-1.5-flash-001",
		}),
			ai.WithMessages(resp.History()...),
			ai.WithPrompt("now rewrite the previous summary and make it look like a pirate wrote it"),
		)
		if err != nil {
			return "", nil
		}

		text := resp.Text()
		return text, nil
	})

	<-ctx.Done()
}
