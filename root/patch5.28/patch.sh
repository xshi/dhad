#!/bin/bash

#----------------------------------------------------------------------
# Patch the SQRT scale 
#----------------------------------------------------------------------

rootdir=$HOME/local/share/root/5.28

echo "Patching ROOT 5.28 in $rootdir ..."

ln -sf `pwd`/TCreatePrimitives.cxx $rootdir/graf2d/gpad/src/
ln -sf `pwd`/TGraph.cxx $rootdir/hist/hist/src/
ln -sf `pwd`/TGraphPainter.cxx $rootdir/hist/histpainter/src/
ln -sf `pwd`/TGraph2DPainter.cxx $rootdir/hist/histpainter/src/
ln -sf `pwd`/THistPainter.cxx $rootdir/hist/histpainter/src/
ln -sf `pwd`/TPad.cxx $rootdir/graf2d/gpad/src/


#----------------------------------------------------------------------
# Patch the RooDLineShape Model 
#----------------------------------------------------------------------
ln -sf `pwd`/LinkDef1.h $rootdir/roofit/roofit/inc/

ln -sf `pwd`/RooDLineShape.h $rootdir/roofit/roofit/inc/
ln -sf `pwd`/RooDLineShape.cxx $rootdir/roofit/roofit/src/
ln -sf `pwd`/RooDLineShapeImp.h $rootdir/roofit/roofit/inc/
ln -sf `pwd`/RooDLineShapeImp.cxx $rootdir/roofit/roofit/src/
ln -sf `pwd`/RooDEnergyImp.h $rootdir/roofit/roofit/inc/
ln -sf `pwd`/RooDEnergyImp.cxx $rootdir/roofit/roofit/src/
ln -sf `pwd`/RooParmFcn.h $rootdir/roofit/roofit/inc/
ln -sf `pwd`/RooParmFcn.cxx $rootdir/roofit/roofit/src/

#----------------------------------------------------------------------
# Compiling code
#----------------------------------------------------------------------

cd $rootdir
./configure --enable-roofit
gmake
cd - 




