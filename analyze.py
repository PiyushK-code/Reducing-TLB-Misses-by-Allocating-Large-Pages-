import sys
import re
import os
from collections import defaultdict

def analyze_large_pages(n):

    # Dictionary to store the count of TLB misses for each 2MB region
    tlb_miss_count = defaultdict(int)
    
    #Executing perf stat command dynamically to store base and end address in file addr.txt
    os.system("./main 24105 > addr.txt")
 
    #Reading base and end address to check range   
    with open("addr.txt", 'r') as file:
        base_end = file.read()
        
    # Use regex to find the base and end addresses
    match = re.search(r'Base:\s*(0x[0-9a-fA-F]+)\s*End:\s*(0x[0-9a-fA-F]+)', base_end)
    
    if match:
        base_addr = int(match.group(1),16)
        end_addr = int(match.group(2),16)
    
    # Read the miss_load.txt file
    with open("miss_load.txt", "r") as f:
        lines=f.readlines()

    for line in lines:
            # Split the line into columns
            columns = line.split()

            # Ensure line contains a TLB miss
            if len(columns) > 15 and columns[12] == "L2" and columns[13] == "miss":
                
                # Extract the memory address in hex (in "Data Symbol" column)
                address_hex = columns[9]
                
                
                if address_hex.startswith("0x"):
                   
                   # Convert the address from hex to decimal
                   address = int(address_hex, 16)

		   # Checking address range
                   if(address >= base_addr and address <= end_addr):
			
                      # Calculate the 2MB region (shift by 21 bits)
                      region = address >> 21

                      # Increment the count of TLB misses for this region
                      tlb_miss_count[region] += 1
    
    # Sort regions by the number of TLB misses in descending order
    sorted_regions = sorted(tlb_miss_count.items(), key=lambda x: x[1], reverse=True)
    
    # Write the top 'n' most missed 2MB regions to the output file (largepages.txt)
    with open("largepages.txt", "w") as out:
        for region, count in sorted_regions[:n]:
            
            # Convert region back to the base address (shift by 21 bits)
            base_address = region << 21
            out.write(f"{base_address}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <number_of_large_pages>")
        sys.exit(1)
    
    # Number of large pages to analyze (passed as argument)
    n = int(sys.argv[1])
    
    analyze_large_pages(n)

