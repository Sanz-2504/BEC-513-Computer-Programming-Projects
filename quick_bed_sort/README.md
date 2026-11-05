#  Project 1: Quick Bed Sort

A high-performance pipeline combining Python subprocess management with native Unix streaming utilities (`zcat`, `grep`, `sort`) to extract filtered genomic coordinates and index them into ascending sequence order.

## The Technical Problem
High-throughput sequencing output splits raw alignment data intervals (BED format) into multiple compressed `.bed.gz` segments. This data contains a massive amount of structural noise across unmapped scaffolds. 

To perform downstream analysis, these raw tracks must be merged, stripped of non-target chromosomes, and systematically sorted first by chromosome name, and then by their starting and ending coordinate integers.

## Computational Strategy (The Terminal Pipe)
Instead of consuming gigabytes of system RAM by reading large text rows into Python arrays, the script leverages an optimized, memory-efficient Shell pipeline via `subprocess.run()`:

1. **`zcat`**: Streams raw text data out from multiple compressed files (`shuf.a.bed.gz`, `shuf.b.bed.gz`) simultaneously without decompressing them onto the hard drive first.
2. **`grep -F -w -f`**: Fast fixed-string matching against `selection.tsv` to filter and retain rows matching targeted canonical chromosomes.
3. **`sort -k1,1 -k2,2n -k3,3n`**: Runs a multi-key stable sorting algorithm:
   - `-k1,1`: Sorts alphabetically by Chromosome name (Column 1).
   - `-k2,2n`: Sorts numerically by Start coordinate (Column 2).
   - `-k3,3n`: Sorts numerically by End coordinate (Column 3).

---

## Repository Workspace Structure
```text
quick_sort_bed/
├── sorted_bed_file_per_sample/   # Output directory created automatically
│   └── X.standard.sorted.bed    # Final consolidated, filtered, and sorted output
├── quick_bed_sort.py             # Main pipeline orchestrator script using sys.argv
├── selection.tsv                 # Target chromosome filtering whitelist index
├── shuf.a.bed.gz                 # Compressed raw genomic input segment A
└── shuf.b.bed.gz                 # Compressed raw genomic input segment B
```

---

## How to Execute the Pipeline

The script utilizes dynamic positional command-line arguments (`sys.argv`), allowing it to be reused on any sample dataset without manual code modification.

### Command Structure
```bash
python quick_bed_sort.py <sample_name> <selection_name> <selection_file> <input_bed_files...>
```

### Run Command for this Dataset
Open a terminal instance inside the `quick_sort_bed` directory and execute the pipeline using the following command structure:
```bash
python quick_bed_sort.py X standard selection.tsv shuf.a.bed.gz shuf.b.bed.gz
```

### Output Verification
Once finished, the pipeline will create the output folder and print:
```text
Processing sample 'X' using selection streams...
Output generated cleanly at: sorted_bed_file_per_sample/X.standard.sorted.bed
```
