import sys
def main():
    matrix_counts = {}
    MIN_OFFSET, MAX_OFFSET = -500, 500

    print("Processing mapped.bed.gz stream...", file=sys.stderr)
    for line in sys.stdin:
        if not line.strip() or line.startswith('#'):
            continue
        columns = line.strip().split('\t')
        
        try:
            # 1. Calculate Fragment Length (Y-value) using columns 8 and 9
            frag_start = int(columns[8])
            frag_end = int(columns[9])
            frag_length = frag_end - frag_start
            
            # 2. Find the Midpoint of our cfDNA Fragment
            frag_center = (frag_start + frag_end) // 2
            
            # 3. Extract and parse the CTCF binding site coordinates from column 4
            # This turns 'chr1:91382-91550|...' into '91382-91550'
            ctcf_coords_text = columns[4].split(':')[1].split('|')[0]
            ctcf_start, ctcf_end = map(int, ctcf_coords_text.split('-'))
            ctcf_center = (ctcf_start + ctcf_end) // 2
            
            # 4. Calculate the relative Offset position (X-value)
            offset = frag_center - ctcf_center
            
        except (ValueError, IndexError):
            continue # Safely skip malformed lines

        # 5. Tally up matching cells inside our window limits
        if MIN_OFFSET <= offset <= MAX_OFFSET:
            if offset not in matrix_counts:
                matrix_counts[offset] = {}
            matrix_counts[offset][frag_length] = matrix_counts[offset].get(frag_length, 0) + 1

    # 6. Print out the final Gnuplot long-form matrix structure
    for current_offset in range(MIN_OFFSET, MAX_OFFSET + 1):
        if current_offset in matrix_counts:
            for current_size in sorted(matrix_counts[current_offset].keys()):
                count = matrix_counts[current_offset][current_size]
                print(f"{current_offset}\t{current_size}\t{count}")
        print("") # Crucial empty blank line break for Gnuplot grid row layout

    print("Success! The matrix output file has been generated.", file=sys.stderr)

if __name__ == "__main__":
    main()



