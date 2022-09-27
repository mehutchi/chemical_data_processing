#!/usr/bin/env python

'''
Code to iterate over each batch#### folder and also each frame_#### folder contained within.
Next, access the scr and copy the relevant the BO (or coordinate) info into a single combined file.
'''

import os
import argparse

def main():
    # determine whether to collect and combine bond_order.list ('bo') or optim.xyz ('coord') information
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filetype", choices=['bo', 'coord'], help='file type to be processed')
    args = parser.parse_args()
        
    start_dir = os.getcwd() + '/'
    # create a sorted list containing all the batch directories inside the current directory
    batch_directories = [b for b in os.listdir(start_dir) if os.path.isdir(b) and 'batch' in b]
    batch_directories.sort()
    # create a new file to contain all the bond_order.list files
    if args.filetype == 'bo':
        new_file_name = 'combined_opt_bond_order.list'
    elif args.filetype == 'coord':
        new_file_name = 'combined_opt_coordinates.xyz'
    with open(os.path.join(start_dir, new_file_name), 'w') as whole_list:
        # iterate over each batch directory
        for k in batch_directories:
            # create a sorted list containing all the frame directories inside the current batch directory
            frame_directories = [f for f in os.listdir(os.path.join(start_dir, k)) if os.path.isdir(os.path.join(start_dir, k, f)) and 'frame' in f]
            frame_directories.sort()
            # iterate over each frame directory
            for i in frame_directories:
                # open and read each bond_order.list
                if args.filetype == 'bo':
                    with open(os.path.join(start_dir, k, i, 'scr/bond_order.list')) as data:
                        data_file = data.readlines()
                # or, open and read each optim.xyz list
                elif args.filetype == 'coord':
                    with open(os.path.join(start_dir, k, i, 'scr/optim.xyz')) as data:
                        data_file = data.readlines()                    
                # write the results into the combined file
                endpoint = False
                while endpoint == False:
                    frame_list = []
                    for j in reversed(data_file):
                        # in reverse order, copy each line of the frame's bond_order.list (or optim.xyz)
                        # until a line is reached with length = 1. (that is the line containing
                        # the number of lines in the frame of the bond_order.list [or optim.xyz] that we want to end on)
                        new_j = j.split()
                        # record each line not equal to len=1
                        if len(new_j) != 1:
                            frame_list.append(j)
                        # once the 'number of lines' line is reached (len=1), exit the while loop
                        elif len(new_j) == 1:
                            frame_list.append(j)
                            endpoint = True
                            break
                line_counter = 0
                # now reverse the order again, and write the information into the whole_list file
                for x in reversed(frame_list):
                    # write a description in the comment (2nd) line, instead of writing from the frame_list
                    if line_counter == 1:
                        # comment line for bond_order.list
                        if args.filetype == 'bo':
                            whole_list.write('optimized MD%s bond order list\n'%i)
                        # comment line for coordinates.xyz
                        elif args.filetype == 'coord':
                            whole_list.write('optimized MD%s coordinate list\n'%i)
                    # otherwise, simply write onto the whole_list
                    elif line_counter != 1:
                        whole_list.write(x)
                    line_counter += 1
            print("%s data processed"%k)

if __name__ == '__main__':
    main()
