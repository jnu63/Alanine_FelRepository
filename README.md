Developing Protocol for exhaustive Sampling and Free Energy Surface Calculation of Alanine Dipeptide
Free energy surface of Alanine Peptide

Dependencies
VMD
AMBER and AmberTools
cpptraj
gmx sham
Python 

Open VMD, load ala.pdb and run on tk console : source vmd.tcl.
sh run2.sh
mkdir Dihedral
mv phi.sh psi.sh *.phi.dat *.psi.dat ./Dihedral/
cd Dihedral
sh phi.sh
sh psi.sh
mv phi.dat psi.dat ../Analysis_Script/
cd ../Analysis_Script/
paste <(awk '{print $2}' phi.dat) <(awk '{print $2}' psi.dat) >dihedral.dat
sh Free_energyPlot.sh
# Alanine_FelRepository
