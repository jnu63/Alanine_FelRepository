#Extracting Psi values from all the files
touch file.txt
for ((i=0; i<36; i++))
do
	for ((j=0; j<36; j++))
	do
		tail -n 10 $i.$j.psi.dat >d.dat
		cat file.txt d.dat >file.dat
		mv file.dat file.txt
		rm d.dat
	done
done
mv file.txt psi.dat
