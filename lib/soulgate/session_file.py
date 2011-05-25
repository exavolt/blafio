#!/usr/bin/env python

"""Python pickle file session storage backend

This backend stores the session data in files encoded with Python's pickle 
module.
"""

from datetime import datetime
import pickle

from session_stub import *

