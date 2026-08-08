from __future__ import annotations

from trevo_pagespeed.stats import summarize


def test_summarize_basic_worst_is_max():
    s = summarize([100.0, 200.0, 300.0], worst_is_max=True)
    assert s.n == 3
    assert s.minimum == 100.0
    assert s.maximum == 300.0
    assert s.median == 200.0
    assert s.mean == 200.0
    assert s.worst == 300.0


def test_summarize_worst_is_min_for_scores():
    s = summarize([90.0, 95.0, 100.0], worst_is_max=False)
    assert s.worst == 90.0


def test_summarize_empty_list():
    s = summarize([])
    assert s.n == 0
    assert s.minimum is None
    assert s.median is None
    assert s.worst is None


def test_summarize_ignores_none_values():
    s = summarize([1.0, None, 3.0])  # type: ignore[list-item]
    assert s.n == 2
    assert s.median == 2.0


def test_summarize_even_count_median():
    s = summarize([1.0, 2.0, 3.0, 4.0])
    assert s.median == 2.5
