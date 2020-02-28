
'''
Script to process a single LVIS flight line into a DEM
'''

##########################################

# import necessary packages
from osgeo import gdal             # package for handling geotiff data
from osgeo import osr              # package for handling projection information
from gdal import Warp
import numpy as np
import argparse
import os

#import other classes
from handleTiff import tiffHandle

##########################################
# define a command line reader

def getCmdArgs():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Command line parser to provide input and output filenames and resolution"))
    p.add_argument("--input", dest ="inName", type=str, default="/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/ILVIS1B_AQ2015_1017_R1605_067952.h5", help=("Input file \nDefault = 10/17/2015 067952"))
    p.add_argument("--output", dest ="outName", type=str, default="data.tif", help=("Input file \nDefault = data.tif"))
    p.add_argument("--res", dest = "res", type=int, default=10, help=("Resolution of data processing \nDefault=10m"))
    p.add_argument("--bounds", dest = "bounds", type=str, default = "No", help=("Set to 'Yes' to process the data using specified bounds. Default = 'No', which processes the full spatial extent"))
    p.add_argument("--subset", dest = "subset", type=int, default = 0, help=("Value sets a fraction of the data to subset \nDefault= 0 (i.e. no subsetting)"))
    cmdargs = p.parse_args()
    return cmdargs


##########################################
# main
if __name__ == '__main__':
  # read the command line
  cmdargs=getCmdArgs()

  #sets filename as the input from the command line parser
  inName=cmdargs.inName
  res = cmdargs.res
  outName = cmdargs.outName
  bounds = cmdargs.bounds
  subset = cmdargs.subset

  # if using bounds
  if bounds == "Yes":
      #initialise class
      b=tiffHandle(inName,onlyBounds=True)

      # set some bounds
      x0=b.bounds[0]
      y0=b.bounds[1]
      x1=(b.bounds[2]-b.bounds[0])/subset+b.bounds[0]
      y1=(b.bounds[3]-b.bounds[1])/subset+b.bounds[1]

      #initialise class, reading in specified bounds
      lvis=tiffHandle(inName,minX=x0,minY=y0,maxX=x1,maxY=y1)

  else:
      #initialise class, using no bounds
      lvis = tiffHandle(inName)


  # set elevation
  lvis.setElevations()
  # find the ground
  lvis.estimateGround()
  #reproject lat and long coords
  lvis.reproject(4326,3031)
  #write tiff for bounds
  lvis.writeTiff(lvis.zG,res,outName)
