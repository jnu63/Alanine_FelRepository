'''
Created on November 12, 2020
@author: Ruhar 
'''
#Performing Minimization and Production run for 10 frames 
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64:/usr/local/cuda-8.0/lib
source /usr/local/amber16/amber.sh
mkdir energy
mkdir md
mkdir traj
mkdir pdb
mkdir dihed
for ((i=0; i<36; i++))
do
    for ((j=0; j<36; j++))
    do
        mv $i.$j.pdb temp.pdb
        tleap -f run1.sh
        pmemd.cuda -O -i min.in -o ./energy/$i.$j.out -p temp.parm7 -c temp.rst7 -r temp.rst -ref temp.rst7 -inf temp.mdinfo
	pmemd.cuda -O -i md.in -o ./md/$i.$j.out -p temp.parm7 -c temp.rst -r md.rst -x temp.nc -inf md.mdinfo -ref temp.rst
	#Calculating dihedral angle
	cpptraj -p temp.parm7 <dihedral.in
	#Extracting the first frame of pdb file
        cpptraj -p temp.parm7 <trajin
	mv temp.nc /traj/$i.$j.nc
	mv test.pdb ./pdb/$i.$j.pdb
        mv phi.dat ./dihed/$i.$j.phi.dat
        mv psi.dat ./dihed/$i.$j.psi.dat
	rm md.rst md.mdinfo
        rm temp.parm7 temp.rst7 temp.rst temp.mdinfo test.pdb
        mv temp.pdb $i.$j.pdb
    done
done
