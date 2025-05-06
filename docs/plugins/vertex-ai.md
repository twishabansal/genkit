# Vertex AI plugin

The Vertex AI plugin provides interfaces to several AI services:

*   [Google generative AI models](https://cloud.google.com/vertex-ai/generative-ai/docs/):
    *   Gemini text generation
    *   Imagen2 and Imagen3 image generation
    *   Text embedding generation
    *   Multimodal embedding generation
*   A subset of evaluation metrics through the Vertex AI [Rapid Evaluation API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/evaluation):
    *   [BLEU](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#bleuinput)
    *   [ROUGE](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#rougeinput)
    *   [Fluency](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#fluencyinput)
    *   [Safety](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#safetyinput)
    *   [Groundeness](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#groundednessinput)
    *   [Summarization Quality](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#summarizationqualityinput)
    *   [Summarization Helpfulness](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#summarizationhelpfulnessinput)
    *   [Summarization Verbosity](https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/evaluateInstances#summarizationverbosityinput)
*   [Vector Search](https://cloud.google.com/vertex-ai/docs/vector-search/overview)

## Installation

```posix-terminal
npm i --save @genkit-ai/vertexai
```

If you want to locally run flows that use this plugin, you also need the [Google Cloud CLI tool](https://cloud.google.com/sdk/docs/install) installed.

## Configuration

To use this plugin, specify it when you initialize Genkit:

```ts
import { genkit } from 'genkit';
import { vertexAI } from '@genkit-ai/vertexai';

const ai = genkit({
  plugins: [
    vertexAI({ location: 'us-central1' }),
  ],
});
```

The plugin requires you to specify your Google Cloud project ID, the [region](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) to which you want to make Vertex API requests, and your Google Cloud project credentials.

*   You can specify your Google Cloud project ID either by setting `projectId` in the `vertexAI()` configuration or by setting the `GCLOUD_PROJECT` environment variable. If you're running your flow from a Google Cloud environment (Cloud Functions, Cloud Run, and so on), `GCLOUD_PROJECT` is automatically set to the project ID of the environment.
*   You can specify the API location either by setting `location` in the `vertexAI()` configuration or by setting the `GCLOUD_LOCATION` environment variable.
*   To provide API credentials, you need to set up Google Cloud Application Default Credentials.
    1. To specify your credentials:
        *   If you're running your flow from a Google Cloud environment (Cloud Functions, Cloud Run, and so on), this is set automatically.
        *   On your local dev environment, do this by running:

            ```posix-terminal
            gcloud auth application-default login --project YOUR_PROJECT_ID
            ```
            
        *   For other environments, see the [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) docs.
    1. In addition, make sure the account is granted the Vertex AI User IAM role (`roles/aiplatform.user`). See the Vertex AI [access control](https://cloud.google.com/vertex-ai/generative-ai/docs/access-control) docs.

## Usage

### Generative AI Models

This plugin statically exports references to its supported generative AI models:

```ts
import { gemini15Flash, gemini15Pro, imagen3 } from '@genkit-ai/vertexai';
```

You can use these references to specify which model `ai.generate()` uses:

```ts
const ai = genkit({
  plugins: [vertexAI({ location: 'us-central1' })],
});

const llmResponse = await ai.generate({
  model: gemini15Flash,
  prompt: 'What should I do when I visit Melbourne?',
});
```

This plugin also supports grounding Gemini text responses using [Google Search](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-gemini#web-ground-gemini) or [your own data](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-gemini#private-ground-gemini).

Important: Vertex AI charges a fee for grounding requests in addition to the cost of making LLM requests.  See the [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) page and be sure you understand grounding request pricing before you use this feature.

Example:

```ts
const ai = genkit({
  plugins: [vertexAI({ location: 'us-central1' })],
});

await ai.generate({
  model: gemini15Flash,
  prompt: '...',
  config: {
    googleSearchRetrieval: {
      disableAttribution: true,
    }
    vertexRetrieval: {
      datastore: {
        projectId: 'your-cloud-project',
        location: 'us-central1',
        collection: 'your-collection',
      },
      disableAttribution: true,
    }
  }
})
```

This plugin also statically exports a reference to the Gecko text embedding model:

```ts
import { textEmbedding004 } from '@genkit-ai/vertexai';
```

You can use this reference to specify which embedder an indexer or retriever uses. For example, if you use Chroma DB:

```ts
const ai = genkit({
  plugins: [
    chroma([
      {
        embedder: textEmbedding004,
        collectionName: 'my-collection',
      },
    ]),
  ],
});
```

Or you can generate embeddings directly:

```ts
const ai = genkit({
  plugins: [vertexAI({ location: 'us-central1' })],
});

const embeddings = await ai.embed({
  embedder: textEmbedding004,
  content: 'How many widgets do you have in stock?',
});
```

This plugin can also handle multimodal embeddings:

```ts
import { multimodalEmbedding001, vertexAI } from '@genkit-ai/vertexai';

const ai = genkit({
  plugins: [vertextAI({location: 'us-central1' })],
});

const embeddings = await ai.embed({
  embedder: multimodalEmbedding001,
  content: {
    content: [{
      "media": {
        "url": "gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
        "contentType": "video/mp4"
      }
    }]
  }
});
```

Imagen3 model allows generating images from user prompt:

```ts
import { imagen3 } from '@genkit-ai/vertexai';

const ai = genkit({
  plugins: [vertexAI({ location: 'us-central1' })],
});

const response = await ai.generate({
  model: imagen3,
  output: { format: 'media' },
  prompt: 'a banana riding a bicycle',
});

return response.media();
```

and even advanced editing of existing images:

```ts
const ai = genkit({
  plugins: [vertexAI({ location: 'us-central1' })],
});

const baseImg = fs.readFileSync('base.png', { encoding: 'base64' });
const maskImg = fs.readFileSync('mask.png', { encoding: 'base64' });

const response = await ai.generate({
  model: imagen3,
  output: { format: 'media' },
  prompt: [
    { media: { url: `data:image/png;base64,${baseImg}` }},
    {
      media: { url: `data:image/png;base64,${maskImg}` },
      metadata: { type: 'mask' },
    },
    { text: 'replace the background with foo bar baz' },
  ],
  config: {
    editConfig: {
      editMode: 'outpainting',
    },
  },
});

return response.media();
```

Refer to [Imagen model documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api#edit_images_2) for more detailed options.

#### Anthropic Claude 3 on Vertex AI Model Garden

If you have access to Claude 3 models ([haiku](https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/claude-3-haiku), [sonnet](https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/claude-3-sonnet) or [opus](https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/claude-3-opus)) in Vertex AI Model Garden you can use them with Genkit.

Here's a sample configuration for enabling Vertex AI Model Garden models:

```ts
import { genkit } from 'genkit';
import {
  claude3Haiku,
  claude3Sonnet,
  claude3Opus,
  vertexAIModelGarden,
} from '@genkit-ai/vertexai/modelgarden';

const ai = genkit({
  plugins: [
    vertexAIModelGarden({
      location: 'us-central1',
      models: [claude3Haiku, claude3Sonnet, claude3Opus],
    }),
  ],
});
```

Then use them as regular models:

```ts
const llmResponse = await ai.generate({
  model: claude3Sonnet,
  prompt: 'What should I do when I visit Melbourne?',
});
```

#### Llama 3.1 405b on Vertex AI Model Garden

First you'll need to enable [Llama 3.1 API Service](https://console.cloud.google.com/vertex-ai/publishers/meta/model-garden/llama3-405b-instruct-maas) in Vertex AI Model Garden.

Here's sample configuration for Llama 3.1 405b in Vertex AI plugin:

```ts
import { genkit } from 'genkit';
import { llama31, vertexAIModelGarden } from '@genkit-ai/vertexai/modelgarden';

const ai = genkit({
  plugins: [
    vertexAIModelGarden({
      location: 'us-central1',
      models: [llama31],
    }),
  ],
});
```

Then use it as a regular model:

```ts
const llmResponse = await ai.generate({
  model: llama31,
  prompt: 'Write a function that adds two numbers together',
});
```

#### Mistral Models on Vertex AI Model Garden

If you have access to Mistral models ([Mistral Large](https://console.cloud.google.com/vertex-ai/publishers/mistralai/model-garden/mistral-large), [Mistral Nemo](https://console.cloud.google.com/vertex-ai/publishers/mistralai/model-garden/mistral-nemo), or [Codestral](https://console.cloud.google.com/vertex-ai/publishers/mistralai/model-garden/codestral)) in Vertex AI Model Garden, you can use them with Genkit.

Here's a sample configuration for enabling Vertex AI Model Garden models:

```ts
import { genkit } from 'genkit';
import {
  mistralLarge,
  mistralNemo,
  codestral,
  vertexAIModelGarden,
} from '@genkit-ai/vertexai/modelgarden';

const ai = genkit({
  plugins: [
    vertexAIModelGarden({
      location: 'us-central1',
      models: [mistralLarge, mistralNemo, codestral],
    }),
  ],
});
```

Then use them as regular models:

```ts
const llmResponse = await ai.generate({
  model: mistralLarge,
  prompt: 'Write a function that adds two numbers together',
  config: {
    version: 'mistral-large-2411', // Optional: specify model version
    temperature: 0.7,              // Optional: control randomness (0-1)
    maxOutputTokens: 1024,         // Optional: limit response length
    topP: 0.9,                     // Optional: nucleus sampling parameter
    stopSequences: ['###'],        // Optional: stop generation at sequences
  }
});
```

The models support:
- `mistralLarge`: Latest Mistral large model with function calling capabilities
- `mistralNemo`: Optimized for efficiency and speed
- `codestral`: Specialized for code generation tasks

Each model supports streaming responses and function calling:

```ts
const response = await ai.generateStream({
  model: mistralLarge,
  prompt: 'What should I cook tonight?',
  tools: ['recipe-finder'],
  config: {
    version: 'mistral-large-2411',
    temperature: 1,
  },
});

for await (const chunk of response.stream) {
  console.log(chunk.text);
}
```

### Evaluators

To use the evaluators from Vertex AI Rapid Evaluation, add an `evaluation` block to your `vertexAI` plugin configuration.

```ts
import { genkit } from 'genkit';
import {
  vertexAIEvaluation,
  VertexAIEvaluationMetricType,
} from '@genkit-ai/vertexai/evaluation';

const ai = genkit({
  plugins: [
    vertexAIEvaluation({
      location: 'us-central1',
      metrics: [
        VertexAIEvaluationMetricType.SAFETY,
        {
          type: VertexAIEvaluationMetricType.ROUGE,
          metricSpec: {
            rougeType: 'rougeLsum',
          },
        },
      ],
    }),
  ],
});
```

The configuration above adds evaluators for the `Safety` and `ROUGE` metrics. The example shows two approaches- the `Safety` metric uses the default specification, whereas the `ROUGE` metric provides a customized specification that sets the rouge type to `rougeLsum`.

Both evaluators can be run using the `genkit eval:run` command with a compatible dataset: that is, a dataset with `output` and `reference` fields. The `Safety` evaluator can also be run using the `genkit eval:flow -e vertexai/safety` command since it only requires an `output`.

### Indexers and retrievers

The Genkit Vertex AI plugin includes indexer and retriever implementations backed by the Vertex AI Vector Search service.

(See the [Retrieval-augmented generation](../rag.md) page to learn how indexers and retrievers are used in a RAG implementation.)

The Vertex AI Vector Search service is a document index that works alongside the document store of your choice: the document store contains the content of documents, and the Vertex AI Vector Search index contains, for each document, its vector embedding and a reference to the document in the document store. After your documents are indexed by the Vertex AI Vector Search service, it can respond to search queries, producing lists of indexes into your document store.

The indexer and retriever implementations provided by the Vertex AI plugin use either Cloud Firestore or BigQuery as the document store. The plugin also includes interfaces you can implement to support other document stores.

Important: Pricing for Vector Search consists of both a charge for every gigabyte of data you ingest and an hourly charge for the VMs that host your deployed indexes. See [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing#vectorsearch). This is likely to be most cost-effective when you are serving high volumes of traffic. Be sure to understand the billing implications the service will have on your project before using it.

To use Vertex AI Vector Search:

1. Choose an embedding model. This model is responsible for creating vector embeddings from text or media. Advanced users might use an embedding model optimized for their particular data sets, but for most users, Vertex AI's `text-embedding-004` model is a good choice for English text, the `text-multilingual-embedding-002` model is good for multilingual text, and the `multimodalEmbedding001` model is good for mixed text, images, and video.
2. In the [Vector Search](https://console.cloud.google.com/vertex-ai/matching-engine/indexes) section of the Google Cloud console, create a new index. The most important settings are:
    *   **Dimensions:** Specify the dimensionality of the vectors produced by your chosen embedding model. The `text-embedding-004` and `text-multilingual-embedding-002` models produce vectors of 768 dimensions. The `multimodalEmbedding001` model can produce vectors of 128, 256, 512, or 1408 dimensions for text and image, and will produce vectors of 1408 dimensions for video.
    *   **Update method:** Select streaming updates.

    After you create the index, deploy it to a standard (public) endpoint.

3. Get a document indexer and retriever for the document store you want to use:

    **Cloud Firestore**

    ```ts
    import { getFirestoreDocumentIndexer, getFirestoreDocumentRetriever } from '@genkit-ai/vertexai/vectorsearch';

    import { initializeApp } from 'firebase-admin/app';
    import { getFirestore } from 'firebase-admin/firestore';

    initializeApp({ projectId: PROJECT_ID });
    const db = getFirestore();

    const firestoreDocumentRetriever = getFirestoreDocumentRetriever(db, FIRESTORE_COLLECTION);
    const firestoreDocumentIndexer = getFirestoreDocumentIndexer(db, FIRESTORE_COLLECTION);
    ```

    **BigQuery**

    ```ts
    import { getBigQueryDocumentIndexer, getBigQueryDocumentRetriever } from '@genkit-ai/vertexai/vectorsearch';
    import { BigQuery } from '@google-cloud/bigquery';

    const bq = new BigQuery({ projectId: PROJECT_ID });

    const bigQueryDocumentRetriever = getBigQueryDocumentRetriever(bq, BIGQUERY_TABLE, BIGQUERY_DATASET);
    const bigQueryDocumentIndexer = getBigQueryDocumentIndexer(bq, BIGQUERY_TABLE, BIGQUERY_DATASET);
    ```

    **Other**

    To support other documents stores you can provide your own implementations of `DocumentRetriever` and `DocumentIndexer`:

    ```ts
    const myDocumentRetriever = async (neighbors) => {
      // Return the documents referenced by `neighbors`.
      // ...
    }
    const myDocumentIndexer = async (documents) => {
      // Add `documents` to storage.
      // ...
    }
    ```

    For an example, see [Sample Vertex AI Plugin Retriever and Indexer with Local File](https://github.com/firebase/genkit/tree/main/js/testapps/vertexai-vector-search-custom).

4. Add a `vectorSearchOptions` block to your `vertexAI` plugin configuration:

    ```ts
    import { genkit } from 'genkit';
    import { textEmbedding004 } from '@genkit-ai/vertexai';
    import { vertexAIVectorSearch } from '@genkit-ai/vertexai/vectorsearch';

    const ai = genkit({
      plugins: [
        vertexAIVectorSearch({
          projectId: PROJECT_ID,
          location: LOCATION,
          vectorSearchOptions: [
            {
              indexId: VECTOR_SEARCH_INDEX_ID,
              indexEndpointId: VECTOR_SEARCH_INDEX_ENDPOINT_ID,
              deployedIndexId: VECTOR_SEARCH_DEPLOYED_INDEX_ID,
              publicDomainName: VECTOR_SEARCH_PUBLIC_DOMAIN_NAME,
              documentRetriever: firestoreDocumentRetriever,
              documentIndexer: firestoreDocumentIndexer,
              embedder: textEmbedding004,
            },
          ],
        }),
      ],
    });
    ```

    Provide the embedder you chose in the first step and the document indexer and retriever you created in the previous step.

    To configure the plugin to use the Vector Search index you created earlier, you need to provide several values, which you can find in the Vector Search section of the Google Cloud console:

    *   `indexId`: listed on the [Indexes](https://console.cloud.google.com/vertex-ai/matching-engine/indexes) tab
    *   `indexEndpointId`: listed on the [Index Endpoints](https://console.cloud.google.com/vertex-ai/matching-engine/index-endpoints) tab
    *   `deployedIndexId` and `publicDomainName`: listed on the "Deployed index info" page, which you can open by clicking the name of the deployed index on either of the tabs mentioned earlier
5. Now that everything is configured, you can use the indexer and retriever in your Genkit application:

    ```ts
    import {
      vertexAiIndexerRef,
      vertexAiRetrieverRef,
    } from '@genkit-ai/vertexai/vectorsearch';

    // ... inside your flow function:

    await ai.index({
      indexer: vertexAiIndexerRef({
        indexId: VECTOR_SEARCH_INDEX_ID,
      }),
      documents,
    });

    const res = await ai.retrieve({
      retriever: vertexAiRetrieverRef({
        indexId: VECTOR_SEARCH_INDEX_ID,
      }),
      query: queryDocument,
    });
    ```

See the code samples for:

*   [Vertex Vector Search + BigQuery](https://github.com/firebase/genkit/tree/main/js/testapps/vertexai-vector-search-bigquery)
*   [Vertex Vector Search + Firestore](https://github.com/firebase/genkit/tree/main/js/testapps/vertexai-vector-search-firestore)
*   [Vertex Vector Search + a custom DB](https://github.com/firebase/genkit/tree/main/js/testapps/vertexai-vector-search-custom)

## Context Caching

The Vertex AI Genkit plugin supports **Context Caching**, which allows models to reuse previously cached content to optimize token usage when dealing with large pieces of content. This feature is especially useful for conversational flows or scenarios where the model references a large piece of content consistently across multiple requests.

### How to Use Context Caching

To enable context caching, ensure your model supports it. For example, `gemini15Flash` and `gemini15Pro` are models that support context caching, and you will have to specify version number `001`.

You can define a caching mechanism in your application like this:

```ts
const ai = genkit({
  plugins: [googleAI()],
});

const llmResponse = await ai.generate({
  messages: [
    {
      role: 'user',
      content: [{ text: 'Here is the relevant text from War and Peace.' }],
    },
    {
      role: 'model',
      content: [
        {
          text: 'Based on War and Peace, here is some analysis of Pierre Bezukhov’s character.',
        },
      ],
      metadata: {
        cache: {
          ttlSeconds: 300, // Cache this message for 5 minutes
        },
      },
    },
  ],
  model: gemini15Flash,
  prompt: 'Describe Pierre’s transformation throughout the novel.',
});
```

In this setup:
- **`messages`**: Allows you to pass conversation history.
- **`metadata.cache.ttlSeconds`**: Specifies the time-to-live (TTL) for caching a specific response.

### Example: Leveraging Large Texts with Context

For applications referencing long documents, such as *War and Peace* or *Lord of the Rings*, you can structure your queries to reuse cached contexts:

```ts

const textContent = await fs.readFile('path/to/war_and_peace.txt', 'utf-8');

const llmResponse = await ai.generate({
  messages: [
    {
      role: 'user',
      content: [{ text: textContent }], // Include the large text as context
    },
    {
      role: 'model',
      content: [
        {
          text: 'This analysis is based on the provided text from War and Peace.',
        },
      ],
      metadata: {
        cache: {
          ttlSeconds: 300, // Cache the response to avoid reloading the full text
        },
      },
    },
  ],
  model: gemini15Flash,
  prompt: 'Analyze the relationship between Pierre and Natasha.',
});
```

### Benefits of Context Caching
1. **Improved Performance**: Reduces the need for repeated processing of large inputs.
2. **Cost Efficiency**: Decreases API usage for redundant data, optimizing token consumption.
3. **Better Latency**: Speeds up response times for repeated or related queries.

### Supported Models for Context Caching

Only specific models, such as `gemini15Flash` and `gemini15Pro`, support context caching, and currently only on version numbers `001`. If an unsupported model is used, an error will be raised, indicating that caching cannot be applied.

### Further Reading

See more information regarding context caching on Vertex AI in their [documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview).
