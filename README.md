# SNR Eval Python

This repository provides a small Python wrapper for the Matlab tool SNR Eval provided by Labrosa: https://labrosa.ee.columbia.edu/projects/snreval.


## Installation

### Prerequisites

Install the compiled version of [SNREval](https://labrosa.ee.columbia.edu/projects/snreval).

### Install using Pip

Install with pip:
```bash
pip install snreval
```

### Build from source

Clone this repository and install the requirements and the Python package:
```bash
pip install -r requirements.txt
python setup.py install
```


## Usage

The usage is simple:
```python
from snreval import SNREval

snr_eval = SNREval("/path/to/snreval")

# Either with a single .wav file
df = snr_eval.eval("/path/to/wave/file.wav")

# Or with a multiple .wav files listed in a .txt file
df = snr_eval.eval("/path/to/txt/file.txt")
```

The result `df` is a pandas DataFrame with the following columns:
- `file`: The path of the .wav file
- `STNR`: The [NIST STNR](http://labrosa.ee.columbia.edu/~dpwe/tmp/nist/doc/stnr.txt)
- `SNR`: The [WADA SNR](http://www.cs.cmu.edu/~robust/Papers/KimSternIS08.pdf)
