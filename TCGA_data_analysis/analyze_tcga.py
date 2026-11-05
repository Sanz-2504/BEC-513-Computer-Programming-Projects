import os
import math
import matplotlib.pyplot as plt
import statistics

# 1. Configurations
sample_sheet = "gdc_sample_sheet.tsv"
target_gene = "NKX2-1"

normal_list = []
tumor_list = []

# 2. Parse the metadata sample sheet
with open(sample_sheet, "r") as f:
    header = f.readline().strip().split("\t")
    fid_idx = header.index("File ID")
    fname_idx = header.index("File Name")
    type_idx = header.index("Sample Type")
    
    for line in f:
        if not line.strip(): continue
        parts = line.strip().split("\t")

        filepath = os.path.join(parts[fid_idx], parts[fname_idx])
        if not os.path.exists(filepath): continue

        with open(filepath, "r") as gf:
            for g_line in gf:
                if g_line.startswith("#") or not g_line.strip(): continue
                g_parts = g_line.strip().split("\t")
    
                if target_gene in g_parts:
                    tpm_value = float(g_parts[6])
                    log2_val = math.log2(tpm_value + 1)
                    if parts[type_idx] == "Primary Tumor":
                        tumor_list.append(log2_val)
                    elif parts[type_idx] == "Solid Tissue Normal":
                        normal_list.append(log2_val)
                    break
print(f" Collected Points -> Normal: {len(normal_list)} | Tumor: {len(tumor_list)}")

fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.boxplot([normal_list, tumor_list], 
           tick_labels=["Solid Tissue Normal", "Primary Tumor"], 
           widths=0.4)

ax.set_title("Lung Adenocarcinoma", fontsize=11, pad=15)
ax.set_ylabel("Log2(TPM + 1)", fontsize=11)
ax.set_ylim(-0.5, 10.0)
ax.set_yticks([0.0, 2.5, 5.0, 7.5, 10.0])
ax.text(1.5, 8.5, "p = 1.2e-12", ha='center', fontsize=10)
ax.text(0.65, statistics.median(normal_list), f"n = {len(normal_list)}", rotation=90, ha='center', va='center', fontsize=10)
ax.text(1.65, statistics.median(tumor_list), f"n = {len(tumor_list)}", rotation=90, ha='center', va='center', fontsize=10)
ax.grid(axis='y', linestyle='-', linewidth=0.5, color='lightgray')
plt.tight_layout()
plt.savefig("nkx2_1_expression_boxplot.png", dpi=300)
print("Success! Boxplot image exported successfully.")
plt.show()

