# -*- coding: utf-8 -*-

"""

ZUGBRUECKE
Calling routines in Windows DLLs from Python scripts running on unixlike systems
https://github.com/pleiszenburg/zugbruecke

	src/zugbruecke/config.py: Handles the modules configuration

	Required to run on platform / side: [UNIX]

	Copyright (C) 2017 Sebastian M. Ernst <ernst@pleiszenburg.de>

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

import os
import json

from .lib import generate_session_id


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_default_config():

	cfg = {}

	# Generate unique session id
	cfg['id'] = generate_session_id()

	# Session mode
	cfg['mode'] = 'ctypes'

	# Display messages from stdout
	cfg['stdout'] = True

	# Display messages from stderr
	cfg['stderr'] = True

	# Write log messages into file
	cfg['logwrite'] = False

	# Overall log level
	cfg['log_level'] = 0 # No logs are generated by default

	# Open server for collected logs from clients
	cfg['log_server'] = True

	# Send log messages to remove sever
	cfg['remote_log'] = False

	# Define Wine & Wine-Python architecture
	cfg['arch'] = 'win32'

	# Define Wine-Python version
	cfg['version'] = '3.5.3'

	# Default config directory
	cfg['dir'] = __get_default_config_directory__()

	return cfg


def get_module_config(override_dict = {}):

	# Get config from files as a prioritized list
	config = __locate_and_read_config_files__()

	# Add override parameters
	config.insert(0, override_dict)

	# Add defaults
	config.append(get_default_config())

	# Sort and return the config
	return __join_config_by_priority__(config)


def __get_default_config_directory__():

	return os.path.join(os.path.expanduser('~'), '.zugbruecke')


def __join_config_by_priority__(config_dict_list):

	# Gather all the keys ...
	key_set = set()
	for config_dict in config_dict_list:
		key_set = key_set | set(list(config_dict.keys()))

	# New parameter dict
	parameter_dict = {}

	# Go through list, from low priority to high
	for config_dict in reversed(config_dict_list):

		# Go through keys
		for key in key_set:

			# Change config is needed
			if key in config_dict.keys():
				parameter_dict[key] = config_dict[key]

	return parameter_dict


def __locate_and_read_config_files__():

	# List of config files' contents by priority
	config_dict_list = []

	# Look for config in the usual spots
	for file_location in [
		os.curdir,
		os.environ.get('ZUGBRUECKE'),
		__get_default_config_directory__(),
		'/etc/zugbruecke'
		]:

		# Compile path
		try:
			try_path = os.path.join(file_location, 'config.json')
		except:
			try_path = None

		# If there is a path ...
		if try_path is not None:

			# Is this a file?
			if os.path.isfile(try_path):

				# Read file
				f = open(try_path, 'r')
				cnt = f.read()
				f.close()

				# Try to parse it
				try:
					cnt_json = json.loads(cnt)
					config_dict_list.append(cnt_json)
				except:
					pass # TODO produce an error

	return config_dict_list
