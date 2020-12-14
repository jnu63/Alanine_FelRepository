# **Establishing a Protocol to Study the Free Energy Surface of Ala-Dipeptide**
Here, proposed a simplest method to study the FEL of small molecules which followed the generation of conformation, exhaustive sampling and recovering of free energy landscape using Boltzmann Distribution. Alanine-Dipeptide used as a model system with two angular degrees of freedom.

![Alt text](Protocol.jpg?raw=true "Title")

## *Package Content*
- Initial Structure of Alanine Dipeptide
- Parameter File for Simulation 
- Simulation Running Code
- Analysis code

## *Dependencies* :
- [VMD](https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD)
- [AMBER and AmberTools](https://ambermd.org/GetAmber.php)
- [cpptraj](https://ambermd.org/GetAmber.php#ambertools)
- [gmx sham](http://manual.gromacs.org/documentation/current/onlinehelp/gmx-sham.html)
- Python v3
- python libraries

## *Code Execution*
```
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
```

## *Contact Information* :
For further details and bugs feel free to write  
- *Ruhar*,  ruhar63_sit@jnu.ac.in 
- *Andrew Lynn*, andrew@jnu.ac.in
