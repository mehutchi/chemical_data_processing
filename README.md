# Small Tools for Processing Computational Chemistry Data

## md_framefinder_energy.py

It is not uncommon to want to optimize the geometry of every frame (or kth frame) of an n-frame (say 10,000) molecular dynamics (MD) trajectory. Due to constraints on computing availability, one would often run such a large job in m batches, where each batch contained p (ex. 100) individual optimizations.

What this code does is take a n-frame coordinate file (.xyz format) as input and create m batch directories each containing p=100 frame directories containing a single nth-frame coordinate file and a terachem input file.

This code was used to systematically organize the frames in order to bulk optimize every frame of an n-frame molecular dynamics trajectory. The program outlined just below is a companion which can easily harvest the relevant data from the file structure outlined and created with this method.

This code could be modified to take the desired Terachem input file as input and also to paste batch scripts where needed, but it was only ever a means to an end, thus it lacks some refinement.

## batch_opt_BO_collector.py 

This code extracts either coordinate or bond order (BO) data from bulk Terachem geometry optimizations. The optimization results data is obtained from the file structure outlined above which now houses Terachem optimization results inside each frame directory. 

This code saves time by automatically parsing the vast structure to extract relevant information into a single file of the same form of a MD trajectory or BO results output.

Coordinates are very structured and follow the same patterns throughout, however BO results are only printed if they exceed a threshold, and therefore are a bit more challenging to obtain due to their variable length.

The optimized BO and/or coordinate trajectories would then be used in codes such as https://github.com/mehutchi/bond_order_time_series.

## tinker_vs_openmm_FIXED.py



