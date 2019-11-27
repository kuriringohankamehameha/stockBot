import sys

with open(sys.argv[1], 'r') as rfile:
    with open('op.csv', 'w') as wfile:
        for line in rfile:
            wfile.write(''.join(','.join(line.split(',')[:2]).split('"')))
            wfile.write('\n')
