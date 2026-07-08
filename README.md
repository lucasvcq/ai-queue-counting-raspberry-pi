# Queue Counting System — Raspberry Pi + AI + ThingsBoard

A camera-based system that detects and counts people in a queue in real time on a Raspberry Pi, and streams the results to a ThingsBoard dashboard via MQTT for live visualization and alerts.

## Overview

The goal was to detect and count people waiting in a queue using a single camera feed, processed directly on a Raspberry Pi with a lightweight, custom-trained AI model — then push the results to **ThingsBoard** over **MQTT** for real-time monitoring (dashboard + alerts), without needing to check the Pi directly.

## Tech Stack

- **Hardware:** Raspberry Pi, Camera module
- **AI Model:** Custom object/person detection model trained with Google Teachable Machine (MobileNet-based), exported as `keras_model.h5`
- **Communication:** MQTT
- **Visualization/Alerts:** ThingsBoard dashboard
- **Language:** Python

## Architecture

```
Camera ──► Raspberry Pi ──► Teachable Machine model (Keras/MobileNet)
                                    │
                                    ▼
                          Person count / detection
                                    │
                                    ▼ MQTT
                              ThingsBoard
                        (live dashboard + alerts)
```

## Key Technical Points

- Training a lightweight custom detection model with Teachable Machine and running inference in real time on Raspberry Pi hardware (CPU only, no GPU)
- Publishing live count data over **MQTT** to a **ThingsBoard** instance for remote, real-time visualization
- Configuring alert thresholds in ThingsBoard so the queue status can be monitored without manually checking the camera feed
- Filtering detections to reliably count people in a queue context (avoiding double-counting, handling occlusion)

## Setup / Usage

```bash
# minimal steps to run it
```

## Results

<!-- Add accuracy, FPS achieved on the Pi, or a screenshot of the ThingsBoard dashboard -->

## Demo

<!-- Add a photo/video of the detection running + a screenshot of the ThingsBoard dashboard -->

## Context

Personal project — embedded AI, computer vision, and IoT dashboarding on Raspberry Pi.

> Note: code comments/documentation may be in French. This README provides an English summary of the project.
