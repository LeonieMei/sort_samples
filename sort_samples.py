#! /usr/bin/env python3

import argparse
import re
import pandas as pd


def print_move(old_index, new_index):
    # print how to sort samples to achieve the correct order
    print(f'{old_index+1} --> {new_index+1}')


def print_moves(sorted_samples, inplace):

    if inplace:
       
        check_sorting = [None] * len(sorted_samples) # check in the end if the sorting was done correctly
        mapping = {sample[3]: new_index for new_index, sample in enumerate(
            sorted_samples)}

        # process the first sample
        old_index = next(iter(mapping))  # get the first key of mapping
        new_index = mapping[old_index]
        print_move(old_index, new_index)
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
                print_move(old_index, new_index)

            check_sorting[new_index] = old_index
            del mapping[old_index]

        assert([sample[3] for sample in sorted_samples] == check_sorting), 'sorting gone wrong'


    else:
        for new_index, sample in enumerate(sorted_samples):
            # sample[3] is the old index
            print_move(sample[3], new_index)


def sample_type_order(sample_type):

    type_order = ('SE', 'AB', 'SP')
    return type_order.index(sample_type)


def sample_sort(samples, inplace):

    return sorted(samples, key=lambda sample: (sample_type_order(
                  sample[0]), sample[1], sample[2]))


def main(args):

    samples = []

    # for tsv files:
    # with open(args.infile, 'r') as infile:

    #   for line in infile:

    #       external_number = line.split('\t')[2]

    df = pd.read_excel(args.infile)

    index = 0 # index for each sample
    for i, row in df.iterrows():

        external_number = row[2]

        try:
            # sample consists of sample_type, patient_id, swab_number
            sample = list(re.search(
                '(SE|AB|SP)([0-9]{4})(A[A-Z])', external_number).groups())
            # add an index to each sample to be able to map the old to the new
            # indices
            sample.append(index)
            index+=1
        # continue if no match has been found
        except AttributeError:
            continue

        samples.append(sample)

    sorted_samples = sample_sort(samples, args.inplace)

    print_moves(sorted_samples, args.inplace)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='sort samples by 1) sample type, 2) patient ID, 3) swap'
        'number')

    parser.add_argument('infile', metavar='input_file', type=str)

    parser.add_argument('--inplace', default=False, action='store_true',
                        help='Show how to sort the samples in-place instead of' 'sorting them into a new rack')

    args = parser.parse_args()

    main(args)
