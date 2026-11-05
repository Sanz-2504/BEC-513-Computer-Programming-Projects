# 1. Set the output type to a high-quality PNG image file
set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
set output 'vplot_heatmap.png'

# 2. Configure a professional 2D color heatmap grid (pm3d view)
set pm3d map
set palette rgbformulae 22,13,10

# 3. Add formal labels to your graph axes
set title "cfDNA V-plot Architecture Around CTCF Sites"
set xlabel "Offset from CTCF Binding Center (bp)"
set ylabel "cfDNA Fragment Length (bp)"
set cblabel "Frequency Count"

# 4. Set boundaries so the graph looks sharp
set xrange [-500:500]
set yrange [30:250]

# 5. Draw the graph using your data matrix file
splot "matrix_output.txt" using 1:2:3 notitle
