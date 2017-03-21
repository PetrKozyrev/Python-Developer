from tqdm import tqdm

with open('/home/petr/master/classifier/unclassified_ids_1-48.txt') as uncl, \
     open('/home/petr/master/classifier/unclass_1-38.fa', 'w') as f:
    for line in tqdm(uncl):
        line = line.strip()
        with open('/home/petr/master/metagenome_samples/low_merge/stitched_reads/K1_IEM-38_S36_L001.assembled.fastq') as iem:
            for line2 in iem:
                line2 = line2.strip()
                if line in line2:
                    f.write(line + '\n')
                    f.write(next(iem) + '\n')
