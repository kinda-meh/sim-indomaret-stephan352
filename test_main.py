#!/usr/bin/env python3
from functools import partial
from os.path import splitext
from glob import glob
import pytest

from main import main


approx = partial(pytest.approx, abs=5e-4)


def search_tcs():
    for tc in sorted(glob("./testcases/*.in")):
        tc, _ = splitext(tc)
        yield f"{tc}.in", f"{tc}.out"


@pytest.mark.parametrize("i_f, e_f", search_tcs())
def test_integration_testcases(i_f, e_f):
    with open(i_f, "r") as f:
        avg, served, lost = main(f)

    with open(e_f, "r") as f:
        e_avg, e_served, e_lost = f.readline().split()
        assert (avg, served, lost) == (approx(float(e_avg)), int(e_served), int(e_lost))
