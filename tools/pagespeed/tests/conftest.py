from __future__ import annotations

import pytest

from trevo_pagespeed.config import Config


@pytest.fixture
def config() -> Config:
    return Config(api_key="fake-key-AIzaTESTKEY1234567890", timeout_seconds=5.0)


@pytest.fixture
def sample_lighthouse_json() -> dict:
    return {
        "lighthouseResult": {
            "finalUrl": "https://trevodigitalconversoes.github.io/produtos/fotografia-presets-lightroom/",
            "lighthouseVersion": "12.2.0",
            "fetchTime": "2026-08-08T12:00:00.000Z",
            "runWarnings": [],
            "environment": {"benchmarkIndex": 1500},
            "categories": {
                "performance": {"score": 0.92},
                "accessibility": {"score": 0.98},
                "best-practices": {"score": 1.0},
                "seo": {"score": 1.0},
            },
            "audits": {
                "first-contentful-paint": {
                    "title": "First Contentful Paint",
                    "numericValue": 1200.5,
                    "numericUnit": "millisecond",
                    "score": 0.9,
                    "displayValue": "1.2 s",
                },
                "largest-contentful-paint": {
                    "title": "Largest Contentful Paint",
                    "numericValue": 2100.0,
                    "numericUnit": "millisecond",
                    "score": 0.85,
                    "displayValue": "2.1 s",
                },
                "total-blocking-time": {
                    "title": "Total Blocking Time",
                    "numericValue": 50.0,
                    "numericUnit": "millisecond",
                    "score": 1.0,
                    "displayValue": "50 ms",
                },
                "cumulative-layout-shift": {
                    "title": "Cumulative Layout Shift",
                    "numericValue": 0.02,
                    "numericUnit": "unitless",
                    "score": 1.0,
                    "displayValue": "0.02",
                },
                "total-byte-weight": {
                    "title": "Total Byte Weight",
                    "numericValue": 850000,
                    "numericUnit": "byte",
                    "score": 0.8,
                    "displayValue": "850 KiB",
                },
                "network-requests": {
                    "title": "Network Requests",
                    "details": {"items": [{"url": "a"}, {"url": "b"}, {"url": "c"}]},
                },
                "largest-contentful-paint-element": {
                    "title": "Largest Contentful Paint element",
                    "details": {
                        "items": [
                            {
                                "node": {
                                    "snippet": "<img src=mockup-hero-04.jpg>",
                                    "selector": "main > section > img",
                                },
                                "url": "https://trevodigitalconversoes.github.io/produtos/fotografia-presets-lightroom/assets/mockup-hero-04.jpg",
                            }
                        ]
                    },
                },
                "unused-css-rules": {
                    "title": "Reduce unused CSS",
                    "score": 0.7,
                    "displayValue": "Potential savings of 350 ms",
                    "description": "Remove dead rules from stylesheets.",
                    "scoreDisplayMode": "numeric",
                    "details": {"overallSavingsMs": 350, "overallSavingsBytes": 12000},
                },
                "modern-image-formats": {
                    "title": "Serve images in next-gen formats",
                    "score": 1.0,
                    "displayValue": "",
                    "description": "",
                    "scoreDisplayMode": "numeric",
                    "details": {},
                },
            },
        }
    }
