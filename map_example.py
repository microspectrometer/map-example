#!python.exe
# -*- coding: utf-8 -*-
r"""Example datalogging only pixels that match the map file wavelengths

Run this script as-is and it generates "datalog.txt".

Import this script to use as a module.

Example
-------
>>> import map_example as mappy

Read the map file
>>> pix, wav = mappy.ints_from_data_columns(pathlib.Path('1002-19_map.txt'))

Write the wavelength heading to file
>>> with open('datalog.txt', "w") as df:
...     df.write(",".join([str(w) for w in wav])+"\n") #doctest: +SKIP

Get the start and stop pixel
>>> start = pix[0]
>>> stop = pix[-1]

Get a frame of data to work with
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> reply = kit.captureFrame()
>>> pixnums = range(1,reply.num_pixels+1)
>>> counts = reply.pixels

Store the frame as a dictionary to look up counts by pixel number
>>> frame = dict(zip(pixnums, counts))

Extract only the pixels that are in the map file
>>> counts = [frame[pixel] for pixel in frame if start <= pixel <= stop]
>>> len(counts)
138
>>> type(counts)
<class 'list'>

Append the counts data to file
>>> with open('datalog.txt', "a") as df:
...     df.write(",".join([str(val) for val in counts])+"\n") #doctest: +SKIP

The map-reading stuff is in lines 127 to 138 and 178 to 184. If
you don't want to import this file, here's a condensed version of
what those lines do to get lists of pixels and wavelengths:

>>> with open('1002-19_map.txt') as mapfile:
...    row_gen = (
...        line.strip('\n').split('\t') for line in mapfile
...        if not line.startswith('#') and not line.startswith('\n')
...        )
...    columns = tuple(zip(*row_gen))
...    pixels, wavelen = tuple(
...        [int(string) for string in columns[col]]
...        for col in range(len(columns))
...        )

"""

import pathlib
from microspeclib.simple import MicroSpecSimpleInterface

def strings_from_data_columns(tsv_datafile : pathlib.Path) -> tuple:
    r"""Return columns of a tab-separated data file as tuples of strings.

    - lines starting with ``#`` (comment lines) are ignored
    - blank lines are ignored
    - works for an arbitrary number of columns

    Example
    -------

    Get the two columns of the map file:

    >>> pix, wav = strings_from_data_columns(pathlib.Path('1002-19_map.txt'))

    >>> print(f"Pixel numbers: {pix[0]} ... {pix[-1]}")
    Pixel numbers: 227 ... 364

    >>> print(f"λ [nm]: {wav[0]} nm ... {wav[-1]} nm")
    λ [nm]: 280 nm ... 1017 nm

    Alternatively, get all columns as a tuple and use index as column number:

    >>> cols = strings_from_data_columns(pathlib.Path('1002-19_map.txt'))

    >>> print(f"Column 0: {cols[0][0]} ... {cols[0][-1]} (Pixel)")
    Column 0: 227 ... 364 (Pixel)

    >>> print(f"Column 1: {cols[1][0]} ... {cols[1][-1]} (λ [nm])")
    Column 1: 280 ... 1017 (λ [nm])

    Parameters
    ----------
    tsv_datafile
        File path of the tab-separated data file.

    Returns
    -------
    tuple
        Index into the return value to access each column of the tab-separated
        data file. Each column is a tuple of strings.

        For example, if there are two data columns, the structure of the
        return value looks like this::

            tuple (return value)
            │
            ├── tuple (data column 0: tuple[0])
            │   │
            │   ├── str (first entry: tuple[0][0])
            │   │   ...
            │   └── str (last entry: tuple[0][-1])
            └── tuple (data column 1: tuple[1])
                │
                ├── str (first entry: tuple[1][0])
                │   ...
                └── str (last entry: tuple[1][-1])

        It is up to the application to convert the string to an
        appropriate numeric data type.

    """

    with open(tsv_datafile) as datafile:

        # Yield one line of the file as a list from tab-separated values
        data = (
            # example for line in datafile: '1\t2\n' -> ['1', '2']
            line.strip('\n').split('\t') for line in datafile
            # ignore header lines and blank lines
            if not line.startswith('#') and not line.startswith('\n')
            )

        # Unzip the data to return a tuple for each column.
        return tuple(zip(*data))

def ints_from_data_columns(tsv_datafile : pathlib.Path) -> tuple:
    """Return columns of a tab-separated data file as lists of ints.

    - lines starting with ``#`` (comment lines) are ignored
    - blank lines are ignored
    - works for an arbitrary number of columns

    Example
    -------

    Get the two columns of the map file:

    >>> pix, wav = ints_from_data_columns(pathlib.Path('1002-19_map.txt'))

    >>> print(f"Pixel numbers: {pix[0]} ... {pix[-1]}")
    Pixel numbers: 227 ... 364
    >>> print(f"λ [nm]: {wav[0]} nm ... {wav[-1]} nm")
    λ [nm]: 280 nm ... 1017 nm

    Parameters
    ----------
    tsv_datafile
        File path of the tab-separated data file.

    Returns
    -------
    tuple
        Index into the return value to access each column of the tab-separated
        data file. Each column is a tuple of ints.

    See Also
    --------
    strings_from_data_columns
        Read data as **strings** instead of **ints**.
        :func:`ints_from_data_columns` (this function) uses
        :func:`strings_from_data_columns`.
    """
    # Get every column in the text file
    data = strings_from_data_columns(tsv_datafile)

    # Convert every string to an int
    return tuple( [int(string) for string in col] for col in data )

if __name__ == '__main__':
    # Read the map file
    pix, wav = ints_from_data_columns(pathlib.Path('1002-19_map.txt'))

    # Figure out the start and stop pixel
    start_pixel = pix[0]; stop_pixel = pix[-1]

    # Store the map as a dictionary from pixel number to wavelength
    chr_map = dict(zip(pix, wav))

    print("\n"
         "-------------------------------------------\n"
         "| Examples using the 'chr_map' dictionary |\n"
         "-------------------------------------------\n"
         )
    print(f"Pixel {start_pixel} is {chr_map[start_pixel]}nm")
    print(f"Pixel {stop_pixel} is {chr_map[stop_pixel]}nm")

    # Index the frame data for logging to file under a heading of
    # wavelengths

    # Create the heading of wavelengths
    data = ",".join([str(w) for w in wav])+"\n"
    with open('datalog.txt', "w", encoding="utf-8") as df:
        df.write(data)

    # Grab three frames and append each to the file
    #
    # Open communication
    kit = MicroSpecSimpleInterface()

    # Datalog
    with open('datalog.txt', "a", encoding="utf-8") as df:
        num_frames = 3
        for i in range(num_frames):
            reply = kit.captureFrame()
            frame = dict(zip(
                            range(1,reply.num_pixels+1), # <- pixel number 1:N
                            reply.pixels) # <---------------- counts
                            )
            # Extract ONLY the data in the wavelength range
            # and join each counts value with commas
            data = ",".join([str(frame[pixel]) for pixel in frame
                    if start_pixel <= pixel <= stop_pixel
                   ])+"\n"
            df.write(data)

    print("\n"
         "-----------------------------------------\n"
         "| Examples using the 'frame' dictionary |\n"
         "-----------------------------------------\n"
         )

    # Grab a frame of data.
    reply = kit.captureFrame()

    # Store the data as a dictionary from pixel number to counts
    # (the new API returns this datatype from kit.captureFrame() )
    pixnums = range(1,reply.num_pixels+1)
    counts = reply.pixels
    frame = dict(zip(pixnums, counts))

    # Look up the counts at an arbitrary pixel.
    print(f"The measurement at pixel 273 is {frame[273]} counts.")
