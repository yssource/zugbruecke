# -*- coding: utf-8 -*-

"""

PYCROSSCALL
Calling routines in Windows DLLs from Python scripts running on unixlike systems
https://github.com/s-m-e/pycrosscall

	pycrosscall/core.py: Core classes for managing pycrosscall sessions

	Required to run on platform / side: [UNIX]

	Copyright (C) 2017 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/s-m-e/pycrosscall/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import atexit
import os
from pprint import pprint as pp
import signal

from .config import get_module_config
from .dll import dll_session_class
from .interpreter import interpreter_session_class
from .lib import setup_wine_python
from .log import log_class
from .wineserver import wineserver_session_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PYCROSSCALL SESSION CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class session_class():


	def __init__(self, parameter = {}):

		# Fill empty parameters with default values
		self.p = get_module_config(parameter)

		# Get and set session id
		self.id = self.p['id']

		# Start session logging
		self.log = log_class(self.id, self.p)

		# Extract server port from log module
		self.p['port_server_log'] = self.log.server_port

		# Log status
		self.log.out('[core] STARTING ...')
		self.log.out('[core] Configured Wine-Python version is %s for %s.' % (self.p['version'], self.p['arch']))
		self.log.out('[core] Log server is listening on port %d.' % self.p['port_server_log'])

		# Store current working directory
		self.dir_cwd = os.getcwd()

		# Install wine-python
		setup_wine_python(
			self.p['arch'],
			self.p['version'],
			self.p['dir']
			)

		# Initialize Wine session
		self.wineserver_session = wineserver_session_class(self.id, self.p, self.log)

		# Initialize interpreter session
		self.interpreter_session = interpreter_session_class(self.id, self.p, self.log, self.wineserver_session)

		# Set up a dict for loaded dlls
		self.dll_dict = {}

		# Mark session as up
		self.up = True

		# Register session destructur
		atexit.register(self.terminate)
		signal.signal(signal.SIGINT, self.terminate)
		signal.signal(signal.SIGTERM, self.terminate)

		# Log status
		self.log.out('[core] STARTED.')


	def LoadLibrary(self, dll_name, dll_type = 'windll'):

		# Get full path of dll
		full_path_dll = os.path.join(self.dir_cwd, dll_name)

		# Log status
		self.log.out('[core] Trying to access DLL "%s" ...' % full_path_dll)

		# Check if dll file exists
		if not os.path.isfile(full_path_dll):

			# Log status
			self.log.out('[core] ... does NOT exist!')

			raise # TODO

		# Log status
		self.log.out('[core] ... exists ...')

		# Simplyfy full path
		full_path_dll = os.path.abspath(full_path_dll)

		# Check whether dll has yet not been touched
		if full_path_dll not in self.dll_dict.keys():

			# Log status
			self.log.out('[core] ... not yet touched ...')

			# Fire up new dll object
			self.dll_dict[full_path_dll] = dll_session_class(
				full_path_dll, dll_name, dll_type, self
				)

			# Log status
			self.log.out('[core] ... touched and added to list.')

		else:

			# Log status
			self.log.out('[core] ... already touched and in list.')

		# Return reference on existing dll object
		return self.dll_dict[full_path_dll]


	def terminate(self):

		# Run only if session is still up
		if self.up:

			# Log status
			self.log.out('[core] TERMINATING ...')

			# Destruct interpreter session
			self.interpreter_session.terminate()

			# Destruct Wine session, quit wine processes
			self.wineserver_session.terminate()

			# Log status
			self.log.out('[core] TERMINATED.')

			# Terminate log
			self.log.terminate()

			# Session down
			self.up = False


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WINDLL CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class windll_class(): # Mimic ctypes.windll


	def __init__(self):

		# Session not yet up
		self.up = False


	def start_session(self, parameter = {}):

		# Session not yet up?
		if not self.up:

			# Fire up a new session
			self.__session__ = session_class(parameter)

			# Mark session as up
			self.up = True


	def LoadLibrary(self, name):

		# Session not yet up?
		if not self.up:

			# Fire up session
			self.start_session()

		# Return a DLL instance object from within the session
		return self.__session__.LoadLibrary(dll_name = name, dll_type = 'windll')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# STAND-ALONE PYTHON INTERPRETER
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class python_interpreter():


	def __init__(self, cmd_line_args):

		cfg = get_module_config()

		setup_wine_python(
			cfg['arch'],
			cfg['version'],
			cfg['dir']
			)

		print('!!!')


	def start_session(self, parameter = {}):

		pass


	def run(self):

		pass
