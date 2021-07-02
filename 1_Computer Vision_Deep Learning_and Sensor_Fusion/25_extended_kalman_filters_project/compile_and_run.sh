# remove the build directory
rm -rf build

# make a new build directory and navigate into it
mkdir build && cd build

# compile the cpp code
cmake .. && make

# run
./ExtendedKF