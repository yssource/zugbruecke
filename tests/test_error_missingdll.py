# -*- coding: utf-8 -*-

"""

ZUGBRUECKE
Calling routines in Windows DLLs from Python scripts running on unixlike systems
https://github.com/pleiszenburg/zugbruecke

	tests/test_error_missingdll.py: Checks for proper error handling if DLL does not exist

	Required to run on platform / side: [UNIX, WINE]

	Copyright (C) 2017-2018 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/zugbruecke/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import pytest

from sys import platform
if any([platform.startswith(os_name) for os_name in ['linux', 'darwin', 'freebsd']]):
	import zugbruecke as ctypes
elif platform.startswith('win'):
	import ctypes


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TEST(s)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def test_missingdll_cll():

	with pytest.raises(OSError):
		dll = ctypes.cdll.LoadLibrary('tests/nonexistent_dll.dll')


def test_missingdll_windll():

	with pytest.raises(OSError):
		dll = ctypes.windll.LoadLibrary('tests/nonexistent_dll.dll')


def test_missingdll_oledll():

	with pytest.raises(OSError):
		dll = ctypes.oledll.LoadLibrary('tests/nonexistent_dll.dll')


def test_missingdll_cll_attr():

	with pytest.raises(OSError):
		dll = ctypes.cdll.nonexistent_dll


def test_missingdll_windll_attr():

	with pytest.raises(OSError):
		dll = ctypes.windll.nonexistent_dll


def test_missingdll_oledll_attr():

	with pytest.raises(OSError):
		dll = ctypes.oledll.nonexistent_dll
