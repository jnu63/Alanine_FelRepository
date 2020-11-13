#tleap system preparation for simulation
source oldff/leaprc.ff99SB
pdb=loadPDB temp.pdb
loadAmberParams frcmod.ionsjc_tip3p
solvateoct pdb TIP3PBOX 8.0
saveAmberParm pdb temp.parm7 temp.rst7
quit
