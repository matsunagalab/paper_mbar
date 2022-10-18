# get replica temperatures in each snapshot
grep "Parameter    :" ../../4_production/run.log | sed 's/Parameter    :/ /' > temperature.dat

# plot replica temperatures in each snapshot
cat << EOF > tmp.plt
set term png
set mxtics
set mytics
set xlabel "Time (ps)"
set ylabel "Temperature (K)"
set output "output_temperature.png"
plot "temperature.dat" using (\$0*2.5):1  with lines lc rgb "blue" title "repID=1 ", "temperature.dat" using (\$0*2.5):2  with lines lc rgb "cyan" title "repID=2 ", "temperature.dat" using (\$0*2.5):3  with lines lc rgb "green" title "repID=3 ", "temperature.dat" using (\$0*2.5):4  with lines lc rgb "red" title "repID=4 "
EOF

gnuplot tmp.plt
rm -rf tmp*
