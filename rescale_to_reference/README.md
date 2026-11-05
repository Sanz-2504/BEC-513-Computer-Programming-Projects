# Project 2: Rescale to Reference

A rigorous, memory-efficient data-scaling pipeline that eliminates experimental length-dependent amplification and capture biases from raw genomic fragment libraries using statistical **Two-Pass Rejection Sampling**.

## The Technical Problem
High-throughput DNA sequencing platforms naturally suffer from fragment-length biases, systematically over-representing or under-representing specific sequence sizes. This software takes a highly skewed empirical genomic library (`query.bed.gz`) and downsamples its records stochastically until its distribution shape perfectly matches a target expected baseline profile curve (`reference.hist`).

## Algorithmic Execution Breakdown

The pipeline runs a two-pass stream-parsing strategy to maintain an **O(1) memory footprint**, preventing system RAM crashes even when processing millions of sequence tracking lines:

1. **Pass 1 (Empirical Profiling):** Streams the compressed binary `.gz` file line-by-line. It extracts genomic boundary indices, computes fragment span lengths (End - Start), and counts size frequencies without loading the file matrix into memory.
2. **Bottleneck Evaluation:** Scans the distribution discrepancies against the reference targets to determine the absolute tightest dataset bottleneck ratio (Max Total Output).
3. **Probability Threshold Mapping:** Computes an individual, clamped survival threshold (P_keep) for each specific fragment size footprint:
   Survival Score = Minimum(1.0, (Target Frequency * Bottleneck) / Available Raw Counts)
4. **Pass 2 (Stochastic Filtration):** Re-streams the compressed file, rolling an independent pseudo-random decimal die (`random.random()`) between 0.0 and 1.0 against the calculated threshold vector to drop excess rows dynamically.

---

## Repository Workspace Structure
```text
rescale_to_reference/
├── query.bed.gz                 # Compressed raw genomic input dataset
├── reference.hist               # Target fragment length probability baseline matrix
├── query_rescaled.bed           # Final balanced, downsampled output dataset
├── rescale_to_reference.py      # Main pipeline script with unrolled logic lines
└── rescaling_profile.png # Exported high-resolution verification chart
```

---

## How to Execute the Pipeline

Ensure that `query.bed.gz` and `reference.hist` are placed in the exact same directory folder alongside the script.

### 1. Run the Data Pipeline
Open the terminal inside the `rescale_to_reference` directory and execute:
```bash
python rescale_to_reference.py
```

### 2. Output Verification Logs
Upon successful execution, the terminal session will output:
```text
Analyzing query file profile (Pass 1)...
Sub-sampling lines and saving to query_rescaled.bed (Pass 2)...
Success! Dataset rescaled perfectly.
Rendering distribution chart...
Verification chart saved successfully as: 'project2_rescaling_profile.png'
```

### Verification Visualization Chart
The script automatically generates a high-resolution chart (`project2_rescaling_profile.png`) plotting three distinct layers to visually verify the mathematical correction:
- **Purple Line:** The original distorted, heavily biased query distribution curve.
- **Green Line:** The target reference profile baseline template.
- **Black Dashed Line:** The newly rescaled output dataset, demonstrating a perfect shape envelope match.
