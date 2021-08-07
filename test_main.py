#!/usr/bin/env python3
from functools import partial
from os.path import splitext
from glob import glob
import pytest

from main import main


approx = partial(pytest.approx, rel=5e-6)


def search_tcs():
    for tc in sorted(glob("./testcases/*.in")):
        tc, _ = splitext(tc)
        yield f"{tc}.in", f"{tc}.out"


@pytest.mark.parametrize("i_f, e_f", search_tcs())
def test_integration_testcases(i_f, e_f):
    with open(i_f, "r") as f:
        avg, served, lost = main(f)

    with open(e_f, "r") as f:
        expects = f.readline().strip()
        assert f"{avg:.6} {served} {lost}" == expects
