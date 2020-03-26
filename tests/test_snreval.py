#!/usr/bin/env python
# coding: utf-8

import pytest
from snreval import SNREval


def test_snreval():
    with pytest.raises(IOError):
        snr_eval = SNREval("")

    with pytest.raises(IOError):
        snr_eval = SNREval.eval(SNREval, "")

    result = "/some/file.wav\t0.0\t0.0\t0.0\t25.2\t32.6\n" + \
        "# Some line to ignore\n" + \
        "/some/other/file.wav\t0.0\t0.0\t0.0\t12.3\t6.9"
    df = SNREval._parse_result(SNREval, result)

    assert len(df) == 2
    assert df.loc[0, "file"] == "/some/file.wav"
    assert df.loc[0, "STNR"] == 25.2
    assert df.loc[0, "SNR"] == 32.6
