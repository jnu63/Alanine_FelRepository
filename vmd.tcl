#'''
#Created on November 12, 2020
#@author: Ruhar 
#'''
#VMD tcl file for generating 36x36 conformations.

set outfile [open angle.dat w]
for {set i 0} {$i < 36} {incr i} {
	set sel [atomselect top "resid 1 2 and name CA"]
	$sel get phi
	set curphi [$sel get phi]
	set cuphi [lindex $curphi 1]
	set newphi [expr {$cuphi+10}]
	$sel set phi $newphi
	set a [$sel get phi]
	set r [lindex $a 1]
        for {set j 0} {$j <36} {incr j} {
		$sel get psi 
		set curpsi [$sel get psi]
		set cupsi [lindex $curpsi 0]
		set newpsi [expr {$cupsi+10}]
		$sel set psi $newpsi
		set b [$sel get psi]
		set s [lindex $b 0]
		puts $outfile "$i.$j.pdb $r $s"		
		set conf [atomselect top protein]	
		$conf writepdb $i.$j.pdb
	}
}

close $outfile	
