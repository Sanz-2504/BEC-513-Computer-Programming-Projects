import os
import sys
import subprocess

sample_name = sys.argv[1]       # e.g., X
selection_name = sys.argv[2]    # e.g., standard
selection_file = sys.argv[3]    # e.g., selection.tsv
bed_files = sys.argv[4:]        # e.g., ['shuf.a.bed.gz', 'shuf.b.bed.gz']
    
output_dir = "sorted_bed_file_per_sample"
output_filename = f"{sample_name}.{selection_name}.sorted.bed"
final_output_path = os.path.join(output_dir, output_filename)
os.makedirs(output_dir, exist_ok=True)

input_files_string = " ".join(bed_files)

    # - zcat streams data -> grep retains selection rows -> sort organizes text blocks
terminal_pipe_command = (
        f"zcat {input_files_string} | "
        f"grep -F -w -f {selection_file} | "
        f"sort -k1,1 -k2,2n -k3,3n > {final_output_path}"
    )

print(f"Processing sample '{sample_name}' using selection streams...")
    
    # Trigger the pipeline natively in the system shell
subprocess.run(terminal_pipe_command, shell=True, check=True)

print(f"Output generated cleanly at: {final_output_path}")

