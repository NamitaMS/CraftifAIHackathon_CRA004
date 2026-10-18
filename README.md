# 🚀 Edge Vision Pipeline with CraftifAI PipeGen

> **HackwithBangalore 4.0 Submission** | **Track A: PipeGen** | **Team ID:** CRA004

---

## 📌 Executive Summary
Our project implements an advanced, production-ready edge AI vision pipeline built using **CraftifAI PipeGen**. By leveraging agentic AI pipeline generation and NVIDIA DeepStream, this solution transforms real-time video feeds into actionable intelligence—designed specifically for low-latency edge deployment on NVIDIA Jetson and x86 GPU hardware.

---

## 🛠️ Tech Stack & Architecture
- **AI Pipeline Synthesis:** CraftifAI PipeGen v0.5.1
- **Vision & Streaming Framework:** NVIDIA DeepStream SDK / TensorRT
- **Target Deployment:** NVIDIA GPUs / Jetson AGX Orin / Orin Nano
- **Language Stack:** C / C++, Bash, Python

---

## ⚡ How PipeGen Was Used
1. **Natural Language Requirements:** Defined our real-world perception goals directly inside PipeGen.
2. **Pipeline Intermediate Representation (PIR):** Generated and verified the hardware-agnostic node graph.
3. **Model Compilation:** Automated TensorRT model optimization and speed reporting.
4. **Production Output:** Generated the complete set of C/C++ source code, DeepStream configurations, and deployment scripts.

---

## 🚀 Quick Start Guide

### Prerequisites
- NVIDIA Driver `560.35.03+` (or `560.76+` on Windows WSL2 host)
- Docker & NVIDIA Container Toolkit configured properly

### Deployment
Clone the repository and launch the generated deployment script:

```bash
# Clone your repository
git clone [https://github.com/nagurukethankumarreddy-alt/CraftifAIHackathon_CRA004.git](https://github.com/nagurukethankumarreddy-alt/CraftifAIHackathon_CRA004.git)
cd CraftifAIHackathon_CRA004

# Run the PipeGen production deployment script
bash run.sh
