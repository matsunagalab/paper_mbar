package require psfgen
topology top_all36_cgenff.rtf
topology V2R.top

segment V2R {
pdb V2R.pdb
first NONE
last NONE
}

coordpdb V2R.pdb V2R

writepsf solute.psf
writepdb solute.pdb


package require solvate
solvate solute.psf solute.pdb -rotate -minmax {{-26 -26 -26} {26 26 26}} -o solvate

#####  add counter ions by using the autoionize plugin
#mol delete all
#package require autoionize
#autoionize -psf solvate.psf -pdb solvate.pdb -sc 0.15-cation SOD -anion CLA -seg ION -o ionize

#####  invert the center of mass and check boxsize
set all [atomselect top all]
$all moveby [vecinvert [measure center $all weight mass]]
$all writepdb ionize.pdb
$all writepsf ionize.psf

set minmax [measure minmax $all]
foreach {min max} $minmax { break }
foreach {xmin ymin zmin} $min { break }
foreach {xmax ymax zmax} $max { break }
puts "Box size estimation:"
puts "boxsizex = [expr abs($xmin)+ $xmax + 1.0]"
puts "boxsizey = [expr abs($ymin)+ $ymax + 1.0]"
puts "boxsizez = [expr abs($zmin)+ $zmax + 1.0]"

exit
