# ASA v1.1 — Application Strategy Analyzer

ASA is a Python + SQLite behavioral analytics engine for job and internship applications.

This repository contains the first complete implementation of the ASA system, focused on:
- minimal user input
- deterministic metrics
- time-aware behavior tracking
- restrained, non-judgmental narrative outputs

## What it does

ASA ingests three types of events:
- applications
- outreach attempts
- market responses

From these, it computes:
- application-level states
- channel-level signal strength
- portfolio-level behavioral patterns

Outputs are generated as short, neutral insight bundles designed to support reflection and decision-making — not automation or ranking.

## Architecture

The system is structured around four pillars:

- Pillar A — Data ingestion (writes only)
- Pillar B — Canonical metrics & time awareness
- Pillar C — Behavioral state classification
- Pillar D — Narrative assembly with suppression rules

All interpretation is layered on top of immutable metrics.

## Status

This is v1.1: a first complete implementation.

Planned future work includes:
- response latency modeling
- decay-weighted signals
- opportunity scoring
- modularization and CLI tooling

## Running

```bash
python3 scripts/score_applications.py

