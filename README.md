# How to

For the test purpose, the node with nvidia-A100 GPU is necessary. Here is the list of nodes with nvidia GPUs,

- CERN lxplus8-gpu (single A100 GPU). Should request afs work area and EOS area.
- SNU gamsa, with 2 RTX3090 GPUs. Good and fast for testing purpose, but as gaming GPUs do not support double precision, the results won’t be reliable.

You can find the installation instruction here:

[cudacpp-instruction](https://github.com/madgraph5/madgraph4gpu/wiki/Working-with-cudacpp-v1.00.00-(October-2024))

Currently for the testing purpose, many issue might occur, strongly suggest install in development mode.

To integrate into CMS workflow, madgraph4gpu should be contracted as a tarball. 

```bash
export WORKDIR=`pwd` # or set different path
mkdir -p $WORKDIR/tmp $WORKDIR/tarballs
cd $WORKDIR/tmp

# Download madgraph4gpu
git clone --recurse-submodules git@github.com:madgraph5/madgraph4gpu.git
cd madgraph4gpu
git checkout cudacpp_for3.6.0_v1.00.00
git submodule update

# remove unecessary file to reduce the file size
rm -rf epoch0 epoch1 epoch2 test tools misc setup* && cd cudacpp
rm -rf alpaka fortran gridpack kokkos sycl && cd cudacpp
rm -rf *.mad *.sa && cd $WORKDIR/tmp

# make a tarball
export DATE=$(date +%Y-%m-%d)
tar -c madgraph4gpu | pigz -p 8 > mg4gpu_${DATE}.tar.gz
mv mg4gpu_${DATE}.tar.gz $WORKDIR/tarballs
```

Download genproduction repo. You can see general instruction for producing CMS gridpacks here:

[how to produce MG5 gridpacks](https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO)

We should modify ``gridpack_generation.sh``` to point the mg4gpu tarball.
```bash
# Download genproduction
cd $WORKDIR
git clone --depth=1 -b mg4gpu git@github.com:choij1589/genproductions.git
cd genproductions/bin/MadGraph5_aMCatNLO

# modify MGSOURCE in gridpack_generation.sh script
# Always check the $MG and $MGSOURCE variables point to.
# e.g. MG=mg4gpu_$DATE.$EXT
#      MGSOURCE = $DIRECTORY_PATH_TO_MG/$MG

# Test: DY2j_LO_5f_FORTRAN
# cards in cards/13p6TeV/mg4gpu/epoch1/DY2j_LO_5f_FORTRAN
time ./gridpack_generation.sh DY2j_LO_5f_FORTRAN cards/13p6TeV/mg4gpu/epoch1/DY2j_LO_5f_FORTRAN
```
