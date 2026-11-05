# Project 4: TCGA Data Analysis

An automated transcriptomics data extraction pipeline designed to crawl multi-directory cancer patient databases, parse expression vectors, and map differential gene expression profiles based on tissue clinical metadata.

## The Technical Problem
Clinical open-access datasets (like the National Cancer Institute's GDC portal) isolate individual patient RNA-sequencing count tables across thousands of independent subdirectories protected behind long alphanumeric hash string keys. 

This pipeline automates file system traversal to locate a target biomarker (**NKX2-1**), extract its normalized abundance metrics, and sort the data points by donor tissue phenotypes using a tracking matrix metadata sheet (`gdc_sample_sheet.tsv`).

## Algorithmic Execution Breakdown

The pipeline processes files dynamically using standard streaming steps to maintain safety across large file collections:

1. **Dynamic Column Mapping:** Parses the file header row of `gdc_sample_sheet.tsv` on the fly to record column index positions (`File ID`, `File Name`, `Sample Type`). This prevents hardcoded index shifts from breaking code execution.
2. **File System Cross-Referencing:** Iterates through patient metadata rows, constructs the dynamic operating system folder path path string components (`File ID / File Name`), and verifies physical file existence before opening connections.
3. **Target Gene Isolation:** Streams individual tab-separated expression lines, skipping metadata comment lines (`#`), to capture column 7 (`tpm_unstranded`) immediately when column 2 matches `NKX2-1`.
4. **Logarithmic Biomarker Transformation:** Converts raw transcript values to damp heavily skewed expression outliers into uniform statistical boundaries:
   
   Log2_Value = Log2(TPM + 1)
   
5. **Tissue Group Segregation:** Maps and appends calculations into explicit array buckets matching clean experimental definitions (`Primary Tumor` vs. `Solid Tissue Normal`).

---

## Repository Workspace Structure
```text
TCGA_data_analysis/
├── analyze_tcga.py               # Main data extraction and boxplot plotting pipeline
├── gdc_sample_sheet.tsv          # Tab-separated patient tissue metadata tracking sheet
├── gdc_manifest.txt              # NCI data download manifest and md5 integrity checksum tracker
├── nkx2_1_expression_boxplot.png # Exported high-resolution boxplot figure chart
├── tcga_data.tar.gz              # Compressed raw clinical repository data archive
└── [Alphanumeric Hash Folders]/  # Extracted patient directories containing expression data
```

---

## How to Execute the Pipeline

Ensure that `gdc_sample_sheet.tsv` and The unzipped alphanumeric patient hash data folders are sitting in the same working folder path right next to the python script.

### 1. Execute the Pipeline File
Open The terminal window inside the `TCGA_data_analysis` directory space and run:
```bash
python analyze_tcga.py
```

### 2. Execution Logging Log Outputs
When running smoothly, the terminal session will output The dataset sample counts directly:
```text
Step 1: Processing RNA-seq data directories...
Collected Points -> Normal: 59 | Tumor: 539
Generating boxplot visualization...
Success! Boxplot image exported successfully.
```

### Statistical Chart Properties
The pipeline outputs a publication-grade figure layout (`nkx2_1_expression_boxplot.png`) configured with strict aesthetic properties:
- **X-Axis Categories:** Side-by-side comparative boxes placing `Solid Tissue Normal` on the left and `Primary Tumor` on the right.
- **Y-Axis Scaling Scale:** Formatted across a standardized `Log2(TPM + 1)` coordinate window spanning from `-0.5` up to `10.0`.
- **Sample Size Annotations:** Displays total sample counts (`n=59` and `n=539`) positioned horizontally right beside the visual center of their corresponding boxplot bodies using precise text adjustments.
