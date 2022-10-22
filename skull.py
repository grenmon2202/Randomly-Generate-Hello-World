import time
import random 
import string
import argparse
import multiprocessing
from multiprocessing import Process

count = 0

def parse_args():
    parser = argparse.ArgumentParser(description='Try and print a word by randomly generating it.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-w', '--word', type=str, default='Hello World', help='Word to print. Please don\'t use the default')
    parser.add_argument('-i', '--iters', type=int, default=0, help='Number of iterations to try and generate required word randomly. 0 for infinite')
    parser.add_argument('-t', '--target', type=int, default=1, help='Number of times word needs to be printed. 0 for infinite')
    parser.add_argument('-c', '--case', action='store_true', help='Use if you want to match case')
    parser.add_argument('-s', '--space', action='store_true', help='Use if you want to consider spaces too')
    parser.add_argument('-v', '--verbose', type=int, default=0, help='0: Print word only, 1: Print additional info like number of iterations needed, number of matches, 2: Print word generated at each iteration')
    parser.add_argument('-p', '--processors', type=int, default='100', help='Number of processers to use for parallel processing. Leaving it to default sets it to your maximum number of processors. Ignore the fact that it says 100')

    args = parser.parse_args()
    return args

def word_gen(letters, size):
    return ''.join(random.choices(letters, k=size))

def iterate(i, verbose, letters, target_word, target_succ):
    global count
    rand_word = word_gen(letters, len(target_word))
    if rand_word==target_word:
        if verbose!=0:
            print('---------------------------------')
            print(f'Target match! Iteration: {i+1}')
            print('---------------------------------')
        print(rand_word)
        count+=1

        if count==target_succ:
            if verbose!=0:
                print()
                print('Required number of targets found!')
                print(f'Number of iterations required: {i+1}')

    if verbose==2:
        print(f'Iteration {i+1}: {rand_word}')

def perform(target_word, iters=0, target_succ=1, verbose=0, match_case=False, use_spaces=False):
    letters = string.ascii_letters+' '
    if not match_case:
        target_word.lower()
        letters = string.ascii_lowercase+' '
    if not use_spaces:
        letters=letters.replace(' ', '')
        target_word=target_word.replace(' ', '')
    if iters!=0:
        for i in range(iters):
            iterate(i, verbose, letters, target_word, target_succ)
            if count==target_succ and target_succ!=0:
                break

    else:
        i = 0
        while True:
            iterate(i, verbose, letters, target_word, target_succ)
            i+=1
            if count==target_succ and target_succ!=0:
                break

    if verbose!=0:
        print()
        print(f'Total number of matches: {count}')

def main():
    start_time = time.time()

    args = parse_args()

    no_threads = max(min(args.processors, multiprocessing.cpu_count()), 1)

    if no_threads != 1 and args.target != 0:
        print('Multithreading is currently only supported with number of targets set to 0')
        exit(0)

    if no_threads == 1:
        perform(args.word, args.iters, args.target, args.verbose, args.case, args.space)

    else:
        threads = []
        for i in range(no_threads):
            if args.iters == 0:
                t = Process(target=perform, args=(args.word, args.iters, args.target, args.verbose, args.case, args.space))
            else:
                t = Process(target=perform, args=(args.word, int(args.iters/no_threads), args.target, args.verbose, args.case, args.space))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    end_time = time.time()
    print(f'Time taken for execution: {(end_time-start_time)}s')

if __name__ == '__main__':
    main()