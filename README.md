# WebRTC Reliability Framework

An automated testing framework for WebRTC peer connection reliability, latency measurement, and cross-browser behavioral comparison, targeting Apple's WebKit engine (the engine powering FaceTime).

## Motivation

FaceTime is built on WebRTC. This framework tests the reliability, latency, and degradation behavior of WebRTC peer connections in WebKit vs Chromium, the same testing Apple's FaceTime SDET team performs.

## Tech Stack
- **Python 3.10**
- **Playwright** - WebKit and Chromium browser automation
- **pytest** - test runner and fixture management
- **pytest-html** - HTML reports with failure screenshots

## Structure
```
tests/
├── test_connection.py   # Peer connection establishment tests
├── test_latency.py      # Connection latency benchmarks
├── test_degradation.py  # Network condition simulation
└── test_comparison.py   # WebKit vs Chromium behavioral differences
pages/
└── webrtc_page.py       # Page Object Model for WebRTC operations
utils/
└── metrics.py           # Latency and reliability measurement helpers
```

## Running Tests
```bash
pip install -r requirements.txt
playwright install webkit chromium
pytest tests/ -v
```

## Status
🚧 In progress