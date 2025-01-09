#include "work.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <errno.h>

//Huge Page size = 2MB
#define PAGE_SIZE (2*1024*1024) 

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: main <last 5 digits of your reg. no>\n");
    return EXIT_FAILURE;
  }
  
  work_init(atoi(argv[1]));

  // Put your changes here

//Allocate memory using Huge Pages and map the addresses from largepages.txt

FILE *file = fopen("largepages.txt", "r"); 
if (!file) { 
	perror("Failed to open largepages.txt"); 
	return EXIT_FAILURE; 
	} 
	
char line[256]; 

//Reading the base addresses from the largepages.txt file and allocating huge pages at that address
while (fgets(line, sizeof(line), file)) {
	unsigned long base_addr = strtoul(line, NULL, 10); 
	void *addr = (void *) base_addr; 
	
	// Allocate memory using mmap at specified address
	void *mapped = mmap(addr, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED | MAP_HUGETLB, -1, 0); 
	if (mapped == MAP_FAILED) { 
		fprintf(stderr, "mmap failed at address %lx\n", base_addr);
		fclose(file); 
		return EXIT_FAILURE; 
	}  
}

fclose(file);


  if (work_run() == 0) {
    printf("Work completed successfully\n");
  }

  return 0;
}
