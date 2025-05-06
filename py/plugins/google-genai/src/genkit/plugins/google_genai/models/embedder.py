# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Google-Genai embedder model."""

import enum
import sys  # noqa

if sys.version_info < (3, 11):  # noqa
    from strenum import StrEnum  # noqa
else:  # noqa
    from enum import StrEnum  # noqa

from google import genai

from genkit.plugins.google_genai.models.utils import PartConverter
from genkit.types import Embedding, EmbedRequest, EmbedResponse


class VertexEmbeddingModels(StrEnum):
    """Embedding models supported by Google-Genai vertex."""

    GECKO_003_ENG = 'textembedding-gecko@003'
    TEXT_EMBEDDING_004_ENG = 'text-embedding-004'
    TEXT_EMBEDDING_005_ENG = 'text-embedding-005'
    GECKO_MULTILINGUAL = 'textembedding-gecko-multilingual@001'
    TEXT_EMBEDDING_002_MULTILINGUAL = 'text-multilingual-embedding-002'


class GeminiEmbeddingModels(StrEnum):
    """Embedding models supported by Google-Genai gemini."""

    GEMINI_EMBEDDING_EXP_03_07 = 'gemini-embedding-exp-03-07'
    TEXT_EMBEDDING_004 = 'text-embedding-004'
    EMBEDDING_001 = 'embedding-001'


class EmbeddingTaskType(StrEnum):
    """Embedding task types supported by Google-Genai."""

    RETRIEVAL_QUERY = 'RETRIEVAL_QUERY'
    RETRIEVAL_DOCUMENT = 'RETRIEVAL_DOCUMENT'
    SEMANTIC_SIMILARITY = 'SEMANTIC_SIMILARITY'
    CLASSIFICATION = 'CLASSIFICATION'
    CLUSTERING = 'CLUSTERING'
    QUESTION_ANSWERING = 'QUESTION_ANSWERING'
    FACT_VERIFICATION = 'FACT_VERIFICATION'


class Embedder:
    """Embedder for Google-Genai."""

    def __init__(
        self,
        version: VertexEmbeddingModels | GeminiEmbeddingModels | str,
        client: genai.Client,
    ):
        """Initialize the embedder.

        Args:
            version: Embedding model version.
            client: Google-Genai client.
        """
        self._client = client
        self._version = version

    async def generate(self, request: EmbedRequest) -> EmbedResponse:
        """Generate embeddings for a given request.

        Args:
            request: Genkit embed request.

        Returns:
            EmbedResponse
        """
        contents = self._build_contents(request)
        config = self._genkit_to_googleai_cfg(request)
        response = await self._client.aio.models.embed_content(model=self._version, contents=contents, config=config)

        embeddings = [Embedding(embedding=em.values) for em in response.embeddings]
        return EmbedResponse(embeddings=embeddings)

    def _build_contents(self, request: EmbedRequest) -> list[genai.types.Content]:
        """Build google-genai request contents from Genkit request.

        Args:
            request: Genkit request.

        Returns:
            list of google-genai contents.
        """
        request_contents: list[genai.types.Content] = []
        for doc in request.input:
            content_parts: list[genai.types.Part] = []
            for p in doc.content:
                content_parts.append(PartConverter.to_gemini(p))
            request_contents.append(genai.types.Content(parts=content_parts))

        return request_contents

    def _genkit_to_googleai_cfg(self, request: EmbedRequest) -> genai.types.EmbedContentConfig | None:
        """Translate EmbedRequest options to Google Ai GenerateContentConfig.

        Args:
            request: Genkit embed request.

        Returns:
            Google Ai embed config or None.
        """
        cfg = None
        if request.options:
            cfg = genai.types.EmbedContentConfig(
                task_type=request.options.get('task_type'),
                title=request.options.get('title'),
                output_dimensionality=request.options.get('output_dimensionality'),
            )

        return cfg
