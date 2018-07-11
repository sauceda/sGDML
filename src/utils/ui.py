import os

#import os, sys
#BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
#sys.path.append(BASE_DIR)

import argparse

import numpy as np
import scipy.io


def yes_or_no(question):
	reply = str(raw_input(question+' (y/n): ')).lower().strip()
	if not reply or reply[0] != 'y':
		return False
	else:
		return True


# COLORS

def info_str(str):
	return '\x1b[1;37m' + str + '\x1b[0m'

def pass_str(str):
	return '\x1b[1;32m' + str + '\x1b[0m'

def warn_str(str):
	return '\x1b[1;33m' + str + '\x1b[0m'

def fail_str(str):
	return '\x1b[1;31m' + str + '\x1b[0m'


# USER INPUT VALIDATION

def is_valid_np_file(parser, arg):
	try:
		return arg, np.load(arg)
	except:
		parser.error("Reading '%s' failed." % arg)

def is_valid_mat_file(parser, arg):
	try:
		return arg, scipy.io.loadmat(arg)
	except:
		parser.error("Reading '%s' failed." % arg)

def is_dir(arg):
	if not os.path.isdir(arg):
		raise argparse.ArgumentTypeError("{0} is not a directory".format(arg))
	else:
		return arg

def is_strict_pos_int(arg):
	x = int(arg)
	if x <= 0:
		raise argparse.ArgumentTypeError('Parameter must be >0.')
	return x