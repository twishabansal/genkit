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

"""Module containing various core constants."""

# The version of Genkit sent over HTTP in the headers.
DEFAULT_GENKIT_VERSION = '0.3.2'

# TODO: make this dynamic
GENKIT_VERSION = DEFAULT_GENKIT_VERSION

GENKIT_CLIENT_HEADER = f'genkit-python/{DEFAULT_GENKIT_VERSION}'
