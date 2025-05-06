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

# 01
from case_01.prompts import s01_staticMenuDotPrompt, s01_vanillaPrompt
from case_02.flows import s02_menuQuestionFlow
from case_02.prompts import s02_dataMenuPrompt

# 02
from case_02.tools import menu_tool

# 03
from case_03.flows import s03_multiTurnChatFlow
from case_03.prompts import s03_chatPreamblePrompt

# 04
# TODO: uncomment once implemented
# from case_04.flows import s04_indexMenuItemsFlow, s04_ragMenuQuestionFlow
# from case_04.prompts import s04_ragDataMenuPrompt
# 05
from case_05.flows import (
    s05_readMenuFlow,
    s05_textMenuQuestionFlow,
    s05_visionMenuQuestionFlow,
)
from case_05.prompts import s05_readMenuPrompt, s05_textMenuPrompt

print('All prompts and flows loaded, use the Developer UI to test them out')
