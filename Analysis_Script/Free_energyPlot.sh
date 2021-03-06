'''
Created on November 12, 2020
@author: Ruhar 
'''
perl sham.pl -i1 phi.dat -i2 psi.dat -data1 1 -data2 1 -o gsham_input.xvg
gmx sham -f gsham_input.xvg -ls fel.xpm
python xpm2mat.py fel.xpm ares.dat
sed 's/[a-zA-Z#]//g' ares.dat | tail -n +2 >ares4.dat
gmx xpm2ps -f fel.xpm -o fel.eps -rainbow red
python Free_energyPlot.py

#paste <(awk '{print $2}' phi.dat) <(awk '{print $2}' psi.dat) >dihedral.dat
python binstring_multiproc.py -input dihedral.dat -weight weights.csv -lambda 0.7 -disc 3 
python Reweighting_FreeEnergyPlot.py -input dihedral.dat -job weighthist -Xdim -180 180 -Ydim -180 180 -disc 3 -weight weights.csv 
