#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `smartimport` package."""

import pytest

from click.testing import CliRunner

import smartimport
from smartimport import cli
from smartimport import str2features


def test_one_pixel_by_letter():
    """Test the OnePixelByLetter algorithm"""
    algo = str2features.OnePixelByLetter(max_length=6, letters="abcd")

    result = algo.convert('abcdAE')

    print(algo.to_str('abcdAE'))

    l = len("abcd") + 2

    assert result[0] == 1.0 #a
    assert result[1 * l + 1] == 1.0 #b
    assert result[2 * l + 2] == 1.0 #c
    assert result[3 * l + 3] == 1.0 #d
    assert result[4 * l + 0] == 1.0 #A
    assert result[4 * l + 5] == 1.0 #A upper
    assert result[5 * l + 4] == 1.0 #E

def test_one_pixel_by_position():
    """Test the OnePixelByPosition algorithm"""
    algo = str2features.OnePixelByPosition(depth=5, letters="abcd")
    print(algo.letters)

    result = algo.convert('abcaAE')

    print(algo.to_str('abcaAE'))

    l = len(algo.letters) + 1

    assert result[0 + 4] == 6/6 #a
    assert result[0 + 5] == 5/6 #b
    assert result[0 + 6] == 4/6 #c
    assert result[1 * l + 4] == 3/6 #a
    assert result[0 + 0] == 2/6 #A
    assert result[0 + l - 1] == 1/6 #E

def test_command_line_interface():
    """Test the CLI."""
    cli.main()
