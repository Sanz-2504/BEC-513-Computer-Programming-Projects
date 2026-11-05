# Project 3: V-plot

An optimized bioinformatics streaming pipeline designed to process cell-free DNA (cfDNA) fragment endpoints, map spatial midpoints relative to genomic transcription factor binding sites (CTCF), and generate long-form data matrix grids for high-resolution structural mapping.

## The Technical Problem
Cell-free DNA (cfDNA) fragmentation patterns reflect the physical footprint of nucleosomes and transcription factors protecting the DNA molecule from enzymatic cleavage in the bloodstream. 

To visualize this protective architecture around transcription factors like CTCF, a **V-Plot** is required. This tool maps the cross-sectional fragment lengths (Y-axis) against the distance (Offset) of the fragment's true midpoint from the exact center of the binding motif (X-axis).

## Algorithmic Execution Breakdown

The script processes genomic data via a standard input text stream (`sys.stdin`) to guarantee **O(1) Memory Complexity**, processing millions of alignments sequentially:

1. **Fragment Length Evaluation (Y-Value):** Extracts the absolute alignment start and end boundaries (columns 8 and 9) to calculate total insert footprint size.
2. **cfDNA Midpoint Isolation:** Locates the physical center position of the circulating fragment footprint:
   
   frag_center = (frag_start + frag_end) // 2
   
3. **Motif Target Coordinate Parsing:** Parses complex string attributes inside column 4 (e.g., turning `chr1:91382-91550|...` into `91382-91550`) to isolate and evaluate the exact center point of the functional binding motif.
4. **Relative Offset Calculation (X-Value):** Computes the relative physical displacement between the fragment center and the protein binding footprint:
   
   offset = frag_center - ctcf_center
   
5. **Window Limitation Filtration:** Restricts footprint tallies strictly within a standardized visual window boundary spanning from `-500 bp` to `+500 bp`.
6. **Gnuplot Block Serialization:** Loops through the continuous spatial scale, outputting structured space-separated coordinate blocks (`Offset \t Fragment_Size \t Density_Count`) isolated by blank line gaps to feed Gnuplot's heatmap engine natively.

---

## Repository Workspace Structure
```text
v_plot/
├── vplot_matrix.py      # Main pipeline script processing stream inputs via stdin
├── mapped.bed.gz        # Compressed raw fragment mapping dataset
├── matrix_output.txt    # Long-form coordinate matrix output file
├── Plot.gp              # Gnuplot script setting canvas and heatmap parameters
├── vplot_heatmap.png    # Final exported high-resolution 2D V-plot visualization
└── README.md            # Project operational documentation
```

---

## How to Execute the Pipeline and Generate the V-Plot

Because the script processes streams directly from standard input, it integrates seamlessly into native Linux pipelines using Unix pipe operators (`|`).

### 1. Generate the Matrix Grid
Open the terminal inside the `v_plot` directory and execute the streaming pipe command directly:
```bash
zcat mapped.bed.gz | python3 vplot_matrix.py > matrix_output.txt
```

### 2. Render the Final Heatmap Plot Image
Run the configured Gnuplot script to build and export the production-grade graphic layout automatically:
```bash
gnuplot Plot.gp
```

### Visualization Metrics
The final image output (`vplot_heatmap.png`) displays a clear double-stranded V-shape distribution envelope, indicating protective nucleosomal wrapping rings flanking the central hyper-accessible CTCF core region.
