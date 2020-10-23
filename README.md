# Sorting samples in racks

## Problem
Samples are sitting in a rack unsorted (with respect to their "externe Nummer"); they are scanned into an Excel file in that order

## Objective
Sort the samples in the rack by 

* A) placing them in a new rack in sorted order
* B) sort them in the same rack until they are in sorted order (in-place)

## Usage
The script ("sort_samples.py") implements both of these methods. It can be run by placing it in the same directory as the Excel file and typing 

`./sample_sort.py <excel_filename>`

on the command line (e.g. in the PowerShell on Windows). Alternatively, you can store the script in a different directory and
additionally pass it the path to the directory where the Excel file sits:

`./sample_sort.py <path/to/excelfile_directory/excel_filename>`

By default, method A is used and the output will look something like this:

```
16 --> 1
7 --> 2
2 --> 3
14 --> 4
17 --> 5
15 --> 6
.
.
.
```

..., i.e. the sample on position 16 should be moved to position 1 on the new rack and so on.

For method B, run:

`./sample_sort --inplace <excel_filename>`

..., which will produce output looking like this:

```
16 --> 1
1 --> 12
12 --> 9
9 --> 16
7 --> 2
2 --> 3
.
.
.
```

## Data
`tobi_samples.xlsx` (example Excel sheet to run the script on)

### Requirements
pandas

### Possible issues
if pandas is not available, the script could be slightly adjusted to work with a `.tsv` instead of an `.xlsx` file

