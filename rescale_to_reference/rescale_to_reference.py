import os
import gzip
import random
import matplotlib.pyplot as plt

# 1. INITIAL CONFIGURATIONS
query_file = "query.bed.gz"
reference_file = "reference.hist"
output_file = "query_rescaled.bed"

random.seed(42)

# 2. LOAD REFERENCE BLUEPRINT (THE GREEN TARGET PROFILE)
ref_dist = {}

with open(reference_file, 'r') as f:
    for line in f:
        cleaned_line = line.strip()
        if not cleaned_line or cleaned_line.startswith('#'):
            continue
            
        parts = cleaned_line.split()
        target_length = int(parts[0])
        target_probability = float(parts[1])
        ref_dist[target_length] = target_probability

# 3. PASS 1: SCAN EMPIRICAL DATA TO COUNT FRAGMENT SIZES (THE PURPLE CURVE)
print("Analyzing query file profile")

query_counts = {}
total_query_records = 0

with gzip.open(query_file, 'rt') as f:
    for line in f:
        cleaned_query_line = line.strip()
        if not cleaned_query_line:
            continue
        cols = cleaned_query_line.split('\t')
        start_coord = int(cols[1])
        end_coord = int(cols[2])
        length = end_coord - start_coord
        current_count = query_counts.get(length, 0)
        query_counts[length] = current_count + 1
        total_query_records = total_query_records + 1

# 4. CALCULATE THE MAX CAPACITY BOTTLENECK (SCALING ENVELOPE)
max_total_output = float('inf')

for length in ref_dist.keys():
    target_freq = ref_dist[length]
    if target_freq > 0:
        available = query_counts.get(length, 0)
        max_allowed = available / target_freq
        if max_allowed < max_total_output:
            max_total_output = max_allowed

# 5. ASSIGN INDIVIDUAL SURVIVAL CHANCE VALUES PER SIZE CATEGORY
sampling_probabilities = {}

for length in ref_dist.keys():
    target_freq = ref_dist[length]
    available = query_counts.get(length, 0)
    if available > 0:
        target_count = max_total_output * target_freq
        calculated_chance = target_count / available
        survival_score = min(1.0, calculated_chance)
        sampling_probabilities[length] = survival_score
    else:
        sampling_probabilities[length] = 0.0

# 6. PASS 2: STOCHASTIC SELECTION FILTER LOOP (DOWN-SAMPLING SUB-SET)
print(f"Sub-sampling lines and saving to {output_file}")

output_dir = os.path.dirname(output_file)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

rescaled_counts = {}
total_rescaled_records = 0

with gzip.open(query_file, 'rt') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
        cleaned_pass2_line = line.strip()
        if not cleaned_pass2_line:
            continue
            
        cols = cleaned_pass2_line.split('\t')
        start_coord = int(cols[1])
        end_coord = int(cols[2])
        length = end_coord - start_coord
        keep_prob = sampling_probabilities.get(length, 0.0)
        random_roll = random.random()

        if random_roll < keep_prob:
            f_out.write(line)
            current_rescaled_tally = rescaled_counts.get(length, 0)
            rescaled_counts[length] = current_rescaled_tally + 1  
            total_rescaled_records = total_rescaled_records + 1

print("Success! Dataset rescaled perfectly.")

# 7. GENERATE THE MATPLOTLIB VERIFICATION CHART VISUALIZATION
print("Rendering distribution chart...")
ref_lengths = sorted(ref_dist.keys())
ref_frequencies = []
orig_frequencies = []
rescaled_frequencies = []

for x in ref_lengths:
    val = ref_dist[x]
    ref_frequencies.append(val)

for x in ref_lengths:
    count = query_counts.get(x, 0)
    if total_query_records > 0:
        prob = count / total_query_records
    else:
        prob = 0
    orig_frequencies.append(prob)

for x in ref_lengths:
    count = rescaled_counts.get(x, 0)
    if total_rescaled_records > 0:
        prob = count / total_rescaled_records
    else:
        prob = 0
    rescaled_frequencies.append(prob)

plt.figure(figsize=(8, 5.5))

# 8. Plot target distribution curve tracking lines
plt.plot(ref_lengths, orig_frequencies, color='purple', label='Original Query (Distorted)', linewidth=2)
plt.plot(ref_lengths, ref_frequencies, color='green', label='Reference Target', linewidth=2)
plt.plot(ref_lengths, rescaled_frequencies, color='black', linestyle='--', label='Rescaled Output', linewidth=1.8)

# 9. Format text description layer bounds
plt.title("Fragment Length Distribution Matching Profile", fontsize=12, pad=12)
plt.xlabel("Fragment Length (bp)")
plt.ylabel("Frequency Probability")
plt.legend(frameon=True, facecolor='white', edgecolor='lightgray')
plt.grid(axis='both', linestyle=':', alpha=0.6)

# 10. Export clear publication-grade image directly into local directory bounds
plt.savefig("project2_rescaling_profile.png", dpi=300, bbox_inches='tight')
print(" Verification chart saved successfully as: 'project2_rescaling_profile.png'")
plt.show()
