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


from menu_ai import ai
from menu_schemas import AnswerOutputSchema, MenuQuestionInputSchema

from .prompts import s02_dataMenuPrompt


@ai.flow(name='s02_menuQuestion')
async def s02_menuQuestionFlow(
    my_input: MenuQuestionInputSchema,
) -> AnswerOutputSchema:
    text = await s02_dataMenuPrompt({'question': my_input.question})
    return AnswerOutputSchema(
        answer=text,
    )
