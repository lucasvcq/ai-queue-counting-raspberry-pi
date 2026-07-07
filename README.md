# Queue Counting System — Raspberry Pi + AI

A camera-based system that counts people in a queue in real time, using a Raspberry Pi and an on-device object detection model (MobileNet-SSD).

## Overview

The goal was to detect and count the number of people waiting in a queue using a single camera feed, processed directly on a Raspberry Pi with a lightweight AI object detection model — no cloud processing required.

## Tech Stack

- **Hardware:** Raspberry Pi, Camera module
- **AI Model:** MobileNet-SSD (object detection)
- **Domain:** Computer vision, embedded AI inference

## Architecture

```
Camera ──► Raspberry Pi ──► MobileNet-SSD inference ──► Person detection & count
```

## Key Technical Points

- Running real-time object detection on constrained hardware (Raspberry Pi CPU, no GPU)
- Choosing MobileNet-SSD specifically for its speed/accuracy tradeoff on edge devices
- Filtering detections to reliably count people (avoiding double-counting, handling occlusion in a queue)

## Setup / Usage

```bash
# minimal steps to run it
```

## Results

<!-- Add accuracy, FPS achieved on the Pi, or a short demo GIF -->

## Demo

<!-- Add a photo/video/GIF of the detection running on a queue -->

## Context

Personal project — computer vision / embedded AI, built on Raspberry Pi.

> Note: code comments/documentation may be in French. This README provides an English summary of the project.
