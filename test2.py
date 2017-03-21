with open('/file1') as uncl, \
     open('/file2') as iem, \
     open('/file3', 'w') as f:
    for line in uncl:
        line = line.strip()
        for line2 in iem:
            line2 = line2.strip()
            if line in line2:
                f.write(line)
                f.write(next(iem))

