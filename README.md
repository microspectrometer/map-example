Example code to read the pixel-to-wavelength map file and use the
**pixel** and **wavelength** data to:

- log *only* the pixels listed in the map file
- align those counts values with the wavelengths of those pixels

# Documentation

```
$ python -m pydoc map_example
```

# A quick example

Write the **wavelength heading** to file:

```python
import pathlib
import map_example as mappy
pix, wav = mappy.ints_from_data_columns(pathlib.Path('1002-19_map.txt'))
with open('datalog.txt', "w") as df:
    df.write(",".join([str(w) for w in wav])+"\n")
```

Log counts values to file for those wavelengths:

```python
from microspeclib.simple import MicroSpecSimpleInterface
kit = MicroSpecSimpleInterface()
reply = kit.captureFrame()
pixnums = range(1,reply.num_pixels+1)
counts = reply.pixels
frame = dict(zip(pixnums, counts))
start = pix[0]; stop = pix[-1]
counts = [frame[pixel] for pixel in frame if start <= pixel <= stop]
with open('datalog.txt', "a") as df:
    df.write(",".join([str(val) for val in counts])+"\n")
```
