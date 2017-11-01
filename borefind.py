# This program opens the hypothetical file "boreholes.txt" which
# has two columns corresponding to the longitude and latitude
# coordinates for 150 boreholes. It then finds the number of
# boreholes in a regular 2.5 x 2.5 deg lat-lon grid in the domain
# 46.25N-23.75N and 63.75E-111.25E. This corresponds to 9 x 19 = 171
# grid cells. It writes the grid cell center lat-lon and number of
# boreholes to the file "out," which is written-out as "borehole_count.txt."
import csv
from array import *
import numpy as np
import os

def borefind():

    file_name = 'BoreNew.txt'  # input file name
    file_path = os.path.join('C://',
                             'Folder1',
                             'Folder2',
                             file_name)
    num_boreholes = 2333
    west_ext = 8101192
    north_ext = -416247.2
    box_size = 250 # pixels for UTM
    grid_x_size = 2027
    grid_y_size = 1724

    # these next 4 lines are how python reads in data:
    with open(file_path, 'r') as file:  # this is opening the file that you named earlier
                                        # the 'r' means it's Reading it (not writing it, that would be 'w')
        i = 0
        # make some empty arrays that you will stuff the data into as you read the file
        data = np.empty([num_boreholes, 3])
        # [[0 for x in range(3)] for y in range(2233)]
        for line in csv.reader(file, delimiter='\t'):  # a for loop; like saying " for every line in this file, do something"
            if "Lat" in line:
                continue        # this is basically skipping the first line
            else:
                data[i, 0] = float(line[0])    # this is storing the three parts of the line into arrays
                data[i, 1] = float(line[1])    # for lat, lon, and the borehole number
                data[i, 2] = int(line[2])
                i += 1              # add one to i each time you go through, for index
    lat = north_ext ## NEED EQUIVALENTS IN UTM
    next_lat = lat + box_size  # each box will be 25000 tall
    box = 0
    bores = dict.fromkeys(range(grid_x_size*grid_y_size))   #initializing
    data_new = np.empty([(grid_x_size*grid_y_size), 3])   # initializing the new array

    for i in range(grid_x_size):          # loop over 9 in this direction

        lon = west_ext           # Max lon UTM value
        next_lon = lon - box_size  # so each box will be 50000 wide
        for j in range(grid_y_size):     #loop over 19 in this direction
            bores[box] = data[(data[:, 0] >= lat) &
                         (data[:, 0] <= next_lat) &
                         (data[:, 1] <= lon) &
                         (data[:, 1] >= next_lon), 2] # some logical bullshit
            data_new[box, 0] = lat - (box_size/2)  # the center of the box (lat)
            data_new[box, 1] = lon + (box_size/2)  # center of the box (lon)
            data_new[box, 2] = bores[box].size # number of holes in this box
            if bores[box].size > 0:
                print(data_new[box,:])
            box += 1
            lon = next_lon
            next_lon = lon - box_size
        lat = next_lat
        next_lat = lat + box_size

    output_file_name = "boreout.txt"
    np.savetxt(output_file_name, data_new, fmt =['%-d', '%-d', '%i'])  # saving the output file
                
if __name__ == "__main__":
    borefind()
