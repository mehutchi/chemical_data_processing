#!/usr/bin/env python
import os

'''
This code looks at a MD trajectory coordinate file (coors.xyz) and creates
an optimization directory (all_opt_frames) at that level. Inside the
optimization directory, batch directories are created for every 100
MD frames. Inside each batch directory, a frame directory is created with
a coordinate file from the appropriate MD step along with a run.in file.

This code does not create the appropriate batch.script file, so those need
to be added to each batch separately. Also, this can be made more general by
requiring an input file to save a batch.script into each batch directory and
a run.in file to copy into each Frame directory.
'''

# example batch.script:
'''
#!/bin/bash -l
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 2
#SBATCH --gres=gpu:1
#SBATCH --mem=8000
#SBATCH -J tera

#SBATCH --no-requeue

# Record job info
echo -e "$SLURM_JOB_ID  $HOSTNAME  $(pwd)" >> ~/.myslurmhistory

module load intel cuda14
export TeraChem=/home/leeping/opt/terachem/current
export PATH=$TeraChem/bin:$PATH
export LD_LIBRARY_PATH=$TeraChem/lib:$LD_LIBRARY_PATH

for d in frame*/
do
cd $d
terachem  run.in &> run.out
cd ..
done
'''

current_dir = os.getcwd() + '/'
# read in coors.xyz file
#file_name = 'coors.xyz'
file_name = input('Enter name of the coordinate file: ')
lines = open(file_name, 'r').readlines()

num_atoms = int(lines[0])
frame_size = num_atoms + 2
frame_list = []
# create an optimization directory and batch directories within it
toppath = 'all_opt_frames'
os.mkdir(toppath)
for i in range(len(lines) / frame_size / 100):
    os.mkdir(os.path.join(toppath, 'batch%04d'%i))
current_batch = 0
# create a directory for each MD frame that includes starting coordinates from that frame and a run.in
for line in lines:
    if 'frame ' in line:
        ls = line.split()
        frame_no = int(ls[1])
        
        pathname = os.path.join(current_dir, 'all_opt_frames', 'batch%04d'%current_batch, 'frame%04d'%frame_no)
        os.mkdir(pathname)
        
        xyz_name = os.path.join(pathname, 'start.xyz')
        with open(xyz_name, 'w') as xyz_file:
            xyz_file.write('%s\n'%num_atoms) 
            xyz_file.write('MD Frame %04d\n'%frame_no)
            
            line_position = lines.index(line)
            
            for i in range(line_position + 1, line_position + frame_size - 1):
                    fields = lines[i].split()
            
                    xyz_file.write(fields[0] + ' ' + fields[1] + ' ' + fields[2] + ' ' + fields[3] + '\n')
        
        in_name = os.path.join(pathname, 'run.in')
        with open(in_name, 'w') as in_file:
            in_file.write('# General Options\n')
            in_file.write('run energy\n')
            in_file.write('coordinates start.xyz\n')
            in_file.write('method rb3lyp\n')
            in_file.write('basis 3-21g')
            in_file.write('charge 1\n')
            in_file.write('spinmult 1\n\n')
            in_file.write('# Output options\n')
            in_file.write('bond_order_list yes\n')
            in_file.write('bond_order_thresh 0.1\n\n')
            in_file.write('# SCF options\n')
            in_file.write('scf diis+a\n')
            in_file.write('maxit 100\n')
            in_file.write('convthre 1e-4\n')
            in_file.write('purify no\n')
            in_file.write('mixguess 0.0\n\n')
            in_file.write('# Technical options\n')
            in_file.write('precision mixed\n')
            in_file.write('threspdp 1e-4\n')
            in_file.write('dftgrid 1')
        if frame_no != 0:
            if frame_no % 100 == 0:
                current_batch += 1
    
