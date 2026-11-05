
#  BEC-513: Computer Programming for Computational Biology

This repository contains high-performance, memory-efficient data processing pipelines and transcriptomics analysis scripts. Developed as part of the BEC-513 course curriculum for the M.Tech Structural and Computational Biology (SCB) program at IIT Roorkee.

---

## 🗂️ Portfolio Index & Project Directories

Each subfolder in this repository functions as an independent, fully documented module. Click into any folder to view its core scripts, visual chart outputs, and runtime execution instructions:

*   **📂 [TCGA_data_analysis](./TCGA_data_analysis):** Traverses clinical cancer data directories, isolates the **NKX2-1** lung adenocarcinoma biomarker row, executes a standardized log2(TPM + 1) normalization transformation, and maps differential patterns between primary tumors and healthy tissues.
*   **📂 [quick_bed_sort](./quick_bed_sort):** Employs memory-stable Unix pipelines via Python subprocess management (`zcat`, `grep`, `sort`) to extract filtered genomic intervals and index chromosome coordinates sequentially with an O(1) RAM footprint.
*   **📂 [rescale_to_reference](./rescale_to_reference):** Corrects library fragment-length extraction and amplification biases using a **Two-Pass Stochastic Rejection Sampling** downsampler that matches a target baseline envelope curve.
*   **📂 [v_plot](./v_plot):** Processes cell-free DNA (cfDNA) alignment streams via standard input, evaluates physical fragment midpoints, computes spatial offsets relative to transcription factor binding motifs (CTCF), and exports data matrices formatted for Gnuplot heatmaps.

```
## ⚙️ Environment Setup & Installation

To run any script within the individual subdirectories, ensure that the following requirements are met in the local terminal environment:

```bash
# Install core visualization package required for Project 2 and Project 4
pip install matplotlib

# (Optional) Verify Gnuplot installation for Project 3 rendering
gnuplot --version
```
