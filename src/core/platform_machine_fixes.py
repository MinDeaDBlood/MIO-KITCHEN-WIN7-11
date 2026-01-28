# Copyright (C) 2022-2025 The MIO-KITCHEN-SOURCE Project
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Platform machine() fix for Windows 7 compatibility.

On Windows 7 with 32-bit Python running on 64-bit system, platform.machine()
incorrectly returns 'AMD64' instead of 'x86'. This causes the application to
look for binaries in bin/Windows/AMD64/ instead of bin/Windows/x86/.

This module patches platform.machine() to return the correct architecture
based on the Python interpreter bitness, not the OS architecture.
"""

import platform

# Save the original platform.machine() value
_original_machine = platform.machine()

# Check if we're running 32-bit Python on a system that reports AMD64
if platform.architecture()[0] == '32bit' and _original_machine == 'AMD64':
    # Override platform.machine() to return 'x86' for 32-bit Python
    platform.machine = lambda: 'x86'
    print(f"[Platform Fix] Corrected platform.machine() from '{_original_machine}' to 'x86' for 32-bit Python")
