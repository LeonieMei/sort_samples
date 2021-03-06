#! /usr/bin/env python3

import argparse
import re
import pandas as pd
from operator import itemgetter


def map_rack_pos(index, args):

    # add 1 so the index counting starts at 1 (and not at 0)
    index += 1

    rack_letters = ["A", "B", "C", "D", "E"]
    # e.g. for A: 0, for B: 1 etc.
    rack_letter_index = index//(args.positions_per_rack_row+1)
    rack_letter = rack_letters[rack_letter_index]

    index -= rack_letter_index * args.positions_per_rack_row
    if index<10:
        filler = '0'
    else:
        filler = ''
    return f'{rack_letter}_{filler}{index}'


def print_overview(sorted_samples, args):

    print('\nrack position <-- sample ID')
    for index, sample in enumerate(sorted_samples):
        print(f'{map_rack_pos(index, args)} <-- {"".join(sample[:1])}')


def print_move(old_index, new_index, args):
    # print how to sort samples to achieve the correct order
    print(f'{map_rack_pos(old_index, args)} --> {map_rack_pos(new_index, args)}')


def print_moves(sorted_samples, args):

    print_overview(sorted_samples, args)
    print('\nold position --> new position')

    if args.inplace:
       
        check_sorting = [None] * len(sorted_samples) # check in the end if the sorting was done correctly
        mapping = {sample[1]: new_index for new_index, sample in enumerate(
            sorted_samples)}

        # process the first sample
        old_index = next(iter(mapping))  # get the first key of mapping
        new_index = mapping[old_index]
        print_move(old_index, new_index, args)
        check_sorting[new_index] = old_index
        del mapping[old_index]

        while mapping:

            try:
                old_index = new_index
                new_index = mapping[old_index]
            # when filling in an already empty position:
            except KeyError:  
                old_index = next(iter(mapping))  # get the next key of mapping
                new_index = mapping[old_index]

            if old_index!=new_index:
                print_move(old_index, new_index, args)

            check_sorting[new_index] = old_index
            del mapping[old_index]

        assert([sample[1] for sample in sorted_samples] == check_sorting), 'sorting gone wrong'


    else:
        for new_index, sample in enumerate(sorted_samples):
            # sample[3] is the old index
            print_move(sample[1], new_index, args)


def sample_sort(samples):
    return sorted(samples, key=itemgetter(0))


def main(args):


    samples = []

    df = pd.read_csv(args.infile, sep=';')


    index = 0 # index for each sample
    for i, row in df.iterrows():

        external_number = row[1]
        sample = (external_number.strip(), index)
        index += 1

        samples.append(sample)

    sorted_samples = sample_sort(samples)
    print_moves(sorted_samples, args)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='sort samples by 1) sample type, 2) patient ID, 3) swap'
        'number')

    parser.add_argument('infile', metavar='input_file', type=str)

    parser.add_argument('--inplace', default=False, action='store_true',
                        help='Show how to sort the samples in-place instead of sorting them into a new rack')
    parser.add_argument('--positions_per_rack_row', default=45, type=int,
                        help='The number of positions per row in the given rack. Default=45.')

    args = parser.parse_args()

    main(args)
