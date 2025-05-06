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

"""Action module for defining and managing RPC-over-HTTP functions."""

from ._action import (
    Action,
    ActionRunContext,
)
from ._key import (
    create_action_key,
    parse_action_key,
)
from ._util import parse_plugin_name_from_action_name

__all__ = [
    Action.__name__,
    ActionRunContext.__name__,
    create_action_key.__name__,
    parse_action_key.__name__,
    parse_plugin_name_from_action_name.__name__,
]
