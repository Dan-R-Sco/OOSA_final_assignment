
'''
A class to handle geotiffs
'''

#######################################################
# import necessary packages
from pyproj import Proj, transform # package for reprojecting data
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np

#import other classes
from processLVIS import lvisGround

#######################################################

class tiffHandlePlus():
  '''
  Class to handle geotiff files
  '''
#######################################################

  def readTiff(self,filename,epsg=3031):
    '''
    Read a geotiff in to RAM
    '''

    # open a dataset object
    ds=gdal.Open(filename)

    # read data from geotiff object
    self.nX=ds.RasterXSize             # number of pixels in x direction
    self.nY=ds.RasterYSize             # number of pixels in y direction

    # geolocation tiepoint
    transform_ds = ds.GetGeoTransform()# extract geolocation information
    self.xOrigin=transform_ds[0]       # coordinate of x corner
    self.yOrigin=transform_ds[3]       # coordinate of y corner
    self.pixelWidth=transform_ds[1]    # resolution in x direction
    self.pixelHeight=transform_ds[5]   # resolution in y direction

    # read data. Returns as a 2D numpy array
    self.data=ds.GetRasterBand(1).ReadAsArray(0,0,self.nX,self.nY)

 ########################################

  def writeTiff(self,data,res,filename,epsg=3031):
    '''
    Write a geotiff from a raster layer
    '''

    #copy self.array data into new array for gap fill
    imageArr = np.copy(self.array)

    # set geolocation information using raster dimensions
    geotransform = (self.xOrigin, self.pixelWidth, 0, self.yOrigin, 0, self.pixelHeight)

    # load data in to geotiff object
    dst_ds = gdal.GetDriverByName('GTiff').Create(filename, self.nX, self.nY, 1, gdal.GDT_Float32)
    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(epsg)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(imageArr)  # write image to the raster
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)  # set no data value
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

    print("Image written to",filename)
    return

#######################################################
