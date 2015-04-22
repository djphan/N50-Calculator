#!/usr/bin/env python
# Run using python3 N50_Calculator <Input Path> <GenomeSize (Optional)>
import sys
import os
import scipy

def file_parser(file_path):
    # Parses a txt file to consolidate all the contig lengths into a list
    # txt file must contain contigs on seperate lines for this parsing func to work
    output = []
    num_contig = 0
    f = open(str(file_path), 'r')
    for line in f:
        # Parse and only add numbers to the list
        try: 
            output = output + [int(line)]
            num_contig += 1

        except ValueError as e:
            continue

    f.close()

    return output, num_contig

def NGorN50(file_path='contigs.txt', genomesize=None):
    contigs, num_contig = file_parser(file_path)
    print( "Total number of contigs: %d " %(num_contig) ) # Expect 20

    # Sort the contigs in reverse order in an array e.g. 
    # array([79, 23, 10])
    contigs = scipy.sort(contigs)[::-1]
    #print(contigs)

    # Calculate sum to compare against for N50s or NG50
    if genomesize == None:
        contig_sum = contigs.sum()/2
        print( "50 Contig Sum is: %d" % (contig_sum) )
    else:
        contig_sum = int(genomesize)/2
        print ("50 Genome Size specified: %d" %(contig_sum))

    for counter in range(1, num_contig+1):
        # TODO: Consider memoizing this if you need to reuse this script for large contigs for performance gains.

        # Check the accumulated sum against the comparison
        if contigs[0:counter].sum() > contig_sum:
            print( "Partial Contig Sum is: %d, with counter: %d, and contig length %d" 
                % (contigs[0:counter].sum(), counter, contigs[counter-1]) )
            # Only need to find the first case
            break

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            NGorN50(file_path=sys.argv[1])
        else:
            print ('Improper Input Path Specified')
            print ('Please use: python3 N50_Calculator <Input Path> <Genome Size (Optional)>') 
            sys.exit()

    elif len(sys.argv) == 3:
        try:
            int(sys.argv[2])
            NGorN50(sys.argv[1], sys.argv[2])
        except ValueError:
            print ('Improper Genome Size specified')
            print ('Please use: python3 N50_Calculator <Input Path> <Genome Size (Optional)>') 
            sys.exit()

    else:
   	    print ('Improper input format')
   	    print ('Please use: python3 N50_Calculator <Input Path> <Genome Size (Optional)>') 
   	    sys.exit()


		


