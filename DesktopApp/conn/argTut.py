# SOURCE: http://docs.python.org/2/howto/argparse.html
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('square', type=int, help='display a square of a given number')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('-v2', '--verbose2', help='increase output verbosity v2', type=int, choices=[0,1,2])
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print 'the square of {} equals {}'.format(args.square, answer)
else:
    print answer

if args.verbose2 == 1:
    print 'the square of {} equals {}'.format(args.square, answer)
elif args.verbose2 == 2:
    print '{}^2 == {}'.format(args.square, answer)
else:
    print answer
