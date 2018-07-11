#!/usr/bin/python

import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import argparse
import numpy as np

from src.utils import io,ui

dataset_dir = BASE_DIR + '/datasets/npz/'


def read_reference_data(f):
	eV_to_kcalmol = 0.036749326/0.0015946679

	e_next, f_next, geo_next = False, False, False
	n_atoms = None
	R,z,T,TG = [],[],[],[]

	geo_idx = 0
	for line in f:
		if n_atoms:
			cols = line.split()
			if e_next:
				T.append(float(cols[5]))
				e_next = False
			elif f_next:
				a = int(cols[1])-1
				TG.append(map(float,cols[2:5]))
				if a == n_atoms-1:
					f_next = False
			elif geo_next:
				if 'atom' in cols:
					a_count += 1
					R.append(map(float,cols[1:4]))

					if geo_idx == 0:
						z.append(io._z_str_to_z_dict[cols[4]])

					if a_count == n_atoms:
						geo_next = False
						geo_idx += 1
			elif 'Energy and forces in a compact form:' in line:
					e_next = True
			elif 'Total atomic forces (unitary forces cleaned) [eV/Ang]:' in line:
					f_next = True
			elif 'Atomic structure (and velocities) as used in the preceding time step:' in line:
					geo_next = True
					a_count = 0
		elif 'The structure contains' in line and 'atoms,  and a total of' in line:
			n_atoms = int(line.split()[3])
			print '| Number atoms per geometry:      {:>7d}'.format(n_atoms)
			continue

		if geo_idx > 0 and geo_idx % 1000 == 0:
			sys.stdout.write("\r| Number geometries found so far: {:>7d}".format(geo_idx))
			sys.stdout.flush()
	sys.stdout.write("\r| Number geometries found so far: {:>7d}".format(geo_idx))
	sys.stdout.flush()
	print '\n' + ui.info_str('[INFO]') + ' Energies and forces have been converted from eV to kcal/mol(/Ang)'


	R = np.array(R).reshape(-1,n_atoms,3) 
	z = np.array(z)
	T = np.array(T) * eV_to_kcalmol
	TG = np.array(TG).reshape(-1,n_atoms,3) * eV_to_kcalmol

	f.close()
	return (R,z,T,TG)


parser = argparse.ArgumentParser(description='Creates a dataset from FHI-aims format.')
parser.add_argument('dataset', metavar = '<dataset>',\
							   type    = argparse.FileType('r'),\
							   help	   = 'path to xyz dataset file')
args = parser.parse_args()
dataset = args.dataset


R,z,T,TG = read_reference_data(dataset)
name = os.path.splitext(os.path.basename(dataset.name))[0]

# Base variables contained in every model file.
base_vars = {'R':				R,\
			 'z':				z,\
			 'T':				T[:,None],\
			 'TG':				TG,\
			 'name':			name,\
			 'theory_level':	'unknown'}

if not os.path.exists(dataset_dir):
	os.makedirs(dataset_dir)
dataset_path = dataset_dir + name + '.npz'
print 'Writing dataset to \'datasets/npz/%s.npz\'...' % name
np.savez_compressed(dataset_path, **base_vars)
print ui.pass_str('DONE')