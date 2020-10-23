#! /usr/bin/env python3

import argparse
import re
import pandas as pd


def print_move(old_index, new_index, swapping):
    # print how to swap or sort samples to achieve the correct order

    if swapping:
        arrow = '<-->'
    else:
        arrow = '-->'

    print(f'{old_index+1} {arrow} {new_index+1}')


def print_moves(sample_tuples, sorted_sample_tuples, swapping):
    # print how to sort samples into the new rack
    for new_index, ele in enumerate(sorted_sample_tuples):
        # there might be a problem if there is one sample twice ??, therefore, look at the last index where the element occurs,
        # so that an already sorted sample is not moved again
        old_index = len(sample_tuples) - 1 - sample_tuples[::-1].index(ele)

        if swapping:
            if old_index != new_index:
                sample_tuples[old_index], sample_tuples[new_index] = sample_tuples[new_index], sample_tuples[old_index]
                print_move(old_index, new_index, args.swapping)
        else:
            # put a None value in there in case of duplicates (so that a sample at a certain position isn't said to be moved
            # twice)
            sample_tuples[old_index] = None
            print_move(old_index, new_index, args.swapping)


def sample_type_sort(sample_type):

    type_order = ('SE', 'AB', 'SP')
    return type_order.index(sample_type)


def sample_sort(sample_tuples, swapping):

    return sorted(sample_tuples, key=lambda sample_tuple: (sample_type_sort( 
    	          sample_tuple[0]), sample_tuple[1], sample_tuple[2]))


def main(args):

    sample_tuples = []

    ## for tsv files:
    # with open(args.infile, 'r') as infile:

    # 	for line in infile:

    # 		external_number = line.split('\t')[2]

    df = pd.read_excel(args.infile)

    for index, row in df.iterrows():

        external_number = row[2]

        try:
            # sample_tuple consists of sample_type, patient_id, swab_number
            sample_tuple = re.search(
                '(SE|AB|SP)([0-9]{4})(A[A-Z])', external_number).groups()
        # continue if no match has been found
        except AttributeError:
            continue

        sample_tuples.append(sample_tuple)

    sorted_sample_tuples = sample_sort(sample_tuples, args.swapping)

    print_moves(sample_tuples, sorted_sample_tuples, args.swapping)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='sort samples by 1) sample type, 2) patient ID, 3) swap number')

    parser.add_argument('infile', metavar='input_file', type=str)

    parser.add_argument('--swapping', default=False, action='store_true', help=				   'Show how to swap samples instead of sorting them into'
    	                'a new rack')

    args = parser.parse_args()

    main(args)
