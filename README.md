## Sorting samples into racks

Problem: samples are sitting in a rack unsorted (with respect to their "externe Nummer"); they are scanned into an Excel file in that order

Objective: sort the samples in the rack by 

* A) placing them in a new rack in sorted order
* B) swapping them in the same rack until they are in sorted order (in-place)

The script ("sort_samples.py") implements both methods (considering also the possibility of duplicate sample numbers). 
The script can be run by placing it in the same directory as the Excel sheet and running 

`./sample_sort.py <Excel file name>`

on the command line (e.g. in the PowerShell on Windows).

By default, method A is used and the output will look something like this:

```

```


