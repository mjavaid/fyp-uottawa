import json
from pprint import pprint
import argparse

X = 0
Y = 0

def testOutput():
    scan_data=open('out-0.txt')
    data = json.load(scan_data)
    output = []
    for item in data:
        output.append({'y':item['y'], 'offset':abs(item['x']-X)})
    pprint(output)
    scan_data.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-x','--xcheck', type=int, help='X Offset')
    args = parser.parse_args()
    X = args.xcheck
    testOutput()
