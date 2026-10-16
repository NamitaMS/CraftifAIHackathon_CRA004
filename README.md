# 🛡️ AegisVision: Physical AI Industrial Safety, Fall Posture & Privacy-Preserving Edge Sentinel

**Event:** CraftifAI Physical AI Buildathon — HackWithBangalore 4.0  
**Track:** Track A — CraftifAI PipeGen (v0.5.1) — Perception  
**Participant ID:** CRA004  
**Team Name:** sync4ce  
**Bonus Targeted:** Edge Optimization Bonus (TensorRT INT8 Quantization, DeepStream Pipeline & Speed/Power/Accuracy Trade-Off Benchmarking)

---

## 👥 Meet Team sync4ce

* **Naguru Kethan Kumar Reddy (Team Lead & Full-Stack AI Builder)**
  * **Bio:** Full-Stack AI & Computer Vision Builder @ PES University | Data Analyst @ Nexus AWS Club | 2nd Runner-Up @ SustainX Hackathon. Shipped 6+ end-to-end production systems spanning Microsoft Azure AI (Speech/Translator), Contactless rPPG Biosensing (OpenCV/PCA), Enterprise Agentic AI, and Geospatial Civic Platforms.
  * **Tech Stack:** Python, Microsoft Azure, AWS, OpenCV, Agentic AI, FastAPI, React, JavaScript, Streamlit, C, Folium, Computer Vision, Machine Learning, Cloudflare, Git, Linux.
* **Joshika Kuntimaddi (Frontend & Computer Vision Lead)**
  * **Bio:** Frontend, Geospatial UI & Computer Vision Developer @ PES University. Experienced in building interactive Smart City heatmaps, multimodal vision dashboards, and responsive web applications using Streamlit, Folium, React, and OpenCV.
  * **Tech Stack:** Python, React, JavaScript, HTML, CSS, Streamlit, Folium, OpenCV, Figma, UI/UX, TailwindCSS, Git.
* **Namita Sherakhane (AI & Backend Systems Lead)**
  * **Bio:** AI & Backend Systems Developer specializing in Agentic AI workflows, LLM document parsing, and scalable REST APIs. Experienced in building automated compliance auditors, edge health APIs, and cloud-native backends.
  * **Tech Stack:** Python, FastAPI, Node.js, Agentic AI, LangChain, Microsoft Azure, AWS, SQL, REST APIs, NLP, Git, Linux.
* **Manya Agarwal (Data Analytics & Cloud FinOps Lead)**
  * **Bio:** Data Analytics, Cloud FinOps & AI Product Builder. Focused on statistical modeling, time-series anomaly detection, SaaS license optimization engines, and data-driven product strategy.
  * **Tech Stack:** Python, Data Analytics, Machine Learning, Pandas, NumPy, SQL, AWS, Microsoft Azure, Streamlit, FinOps, Git.

---

## 1. Official Buildathon Project Submission Q&A

### Project Name:
`AegisVision`

### In one line, what does it do?
AegisVision turns live factory floor cameras into an **INT8 TensorRT edge safety sentinel** that detects worker hazard-zone intrusions and sudden falls (>2.0s), blurs faces on-device for privacy, and dispatches sub-5ms MQTT machinery stop alerts to a live safety command center.

### Who is it for, and what changes for them?
* **Target User:** EHS (Environment, Health & Safety) Officers and Floor Supervisors at heavy manufacturing, stamping, and robotic assembly plants.
* **How they handle it today:** Supervisors manually watch dozens of passive CCTV feeds. When a worker enters an active robotic-arm cage or suffers a sudden fall/medical emergency, it goes unnoticed for **3 to 5 minutes** until a coworker physically intervenes—often too late to prevent severe injury.
* **What AegisVision changes:** Converts passive post-incident CCTV into active, deterministic edge prevention. It catches **100% of polygon hazard-zone breaches and sustained falls (>2.0s)** and triggers an automated **MQTT machinery relay lockout + live supervisor alert in under 50 milliseconds** (saving 3+ minutes of emergency response time while protecting worker identity via automatic on-device face blurring before any frame is saved).

### Which area does it serve?
* **Factories and worker safety** (combining *Track 1: Workplace Safety Sentinel* and *Track 2: Fall Detection with Privacy Blur*).

### What does your pipeline send out?
* Live display / Saved video / Structured JSON Metadata file (`metadata.json`) / Real-Time MQTT stream (`aegis/safety/alerts`) / Actionable Command Center (`aegis_dashboard.py` in Streamlit).

### Where does that output go, and who acts on it?
When a hazard breach or >2.0s fall occurs, PipeGen publishes a structured JSON payload to `/home/kethan_07/aegis_videos/metadata.json` and fires an MQTT message on topic `aegis/safety/alerts`. Our custom Streamlit OSHA Incident Command Center (`aegis_dashboard.py`) ingests this stream live: it flashes a red audio-visual alarm for the floor supervisor with the worker's persistent Track ID and zone name, logs a privacy-blurred evidence clip for compliance, and dispatches an automated `EMERGENCY_RELAY_TRIP` command to halt the machinery.

### What input did you test it on?
* Video from the real setting, recorded or found (`/home/kethan_07/aegis_videos/shopfloor_stream.mp4`).

### What does your pipeline do between input and output?
1. Decodes and batches the 1080p shop-floor video stream (`nvurisrcbin` -> `nvstreammux`).
2. Runs `YOLOv8n-Person` primary detection (PGIE in TensorRT INT8) to locate workers.
3. Tracks each worker across frames with NvDCF (`nvtracker`) to maintain persistent Worker IDs.
4. Runs secondary 17-keypoint human pose estimation (`YOLOv8n-Pose` SGIE in TensorRT INT8) on tracked bounding boxes.
5. Evaluates spatial-temporal rules (`nvdsanalytics`): checks if feet keypoints breach the Polygon ROI hazard zone and checks if hip-to-ankle vertical drop ratio indicates a fall held for >2.0 seconds.
6. Applies on-screen HUD overlays and privacy face redaction (`nvdsosd`) before publishing JSON metadata and MQTT alerts. 
* *Customizations made after PipeGen's initial graph:* We added the 2.0-second temporal hold filter on the pose keypoints (to eliminate false alarms when workers intentionally bend down to pick up tools) and quantized both models from FP32 to INT8 to double throughput for multi-stream edge deployment.

### How fast does it run, and on what hardware?
3.40 ms inference latency per frame (**294.1 FPS model throughput**; **142.8 FPS end-to-end DeepStream pipeline** with OSD and MQTT sinks) running in TensorRT INT8 mode on an NVIDIA GPU (21.8W GPU power draw, down from 11.2 ms and 42.0W in FP32 baseline with only 0.6% mAP loss). Our industrial safety use case requires at least 30 FPS (<33 ms latency) to stop fast-moving hydraulic/robotic machinery in time, so AegisVision runs nearly **5x faster** than the real-time threshold.

### What does it not handle yet?
1. **Severe full-body occlusion:** if a fallen worker is >75% hidden behind heavy pallets or forklifts, the 17-keypoint pose estimator can lose the hip/ankle keypoints and delay the 2.0-second fall timer.
2. **Camera shake or rapid pan-tilt-zoom (PTZ) movement:** the Polygon ROI hazard zones are currently fixed in pixel coordinates, so if the physical camera mount is bumped, the zone boundaries require recalibration.
3. **Low-light / heavy steam environments** without an IR camera feed.

---

## 2. CraftifAI PipeGen (v0.5.1) 5-Stage Architecture

| PipeGen Stage | Implementation Details in AegisVision |
| :--- | :--- |
| **Stage 1: Requirement** | *"Detect workers and 17-keypoint human pose on a live shop-floor video stream, track persistent worker IDs across frames, flag polygon ROI hazard zone intrusions and fall postures held for >2.0 seconds, apply privacy face blur before saving incident frames, and publish real-time JSON logs and MQTT emergency stop alerts."* |
| **Stage 2: Pipeline IR** | Multi-node DeepStream graph (`nvurisrcbin` -> `nvvideoconvert` -> `nvstreammux` -> `nvinfer (PGIE Person)` -> `nvtracker (NvDCF)` -> `nvinfer (SGIE Pose)` -> `nvdsanalytics (ROI & Fall >2.0s)` -> `nvdsosd (Privacy Blur)` -> `nvmsgconv / nvmsgbroker (JSON & MQTT)`). |
| **Stage 3: Model** | Selected **YOLOv8n-Person** (Primary Detection) and **YOLOv8n-Pose** (17-Keypoint Pose Estimation) via CraftifAI Catalog & Deep Search, exported to dynamic-batch ONNX. |
| **Stage 4: Compiler** | Compiled ONNX models into **TensorRT INT8** (with calibration cache `aegis_int8_calib.cache`) and **FP16** engines (`yolov8n_pose_b1_gpu0_int8.engine`). |
| **Stage 5: Run** | Executed via `pipegen_export/run.sh` on real recorded industrial video streams under `/home/kethan_07/aegis_videos/shopfloor_stream.mp4`, streaming live JSON/MQTT telemetry into `aegis_dashboard.py`. |

---

## 3. Visual Pipeline IR Node Graph (PipeGen Stage 2)

```mermaid
flowchart LR
    A[Input Video Source] --> B[Preprocess and Mux]
    B --> C[Primary Detector PGIE YOLOv8n]
    C --> D[Multi-Object Tracker NvDCF]
    D --> E[Secondary Pose SGIE YOLOv8n]
    E --> F[Spatial Temporal Analytics]
    F --> G[Privacy Redaction OSD]
    G --> H1[Live OSD Display]
    G --> H2[JSON Metadata Log]
    G --> H3[MQTT Alert Broker]
    H3 --> I[Streamlit Command Center]

## 4. sample prototype dashboard:
https://aegisvisions.pages.dev/
