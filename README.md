# 🛡️ AegisVision: Physical AI Industrial Safety, Fall Posture & Privacy-Preserving Edge Sentinel

**Track:** Track A — CraftifAI PipeGen (v0.5.1) — Perception  
**Team Name:** sync4ce  
**Bonus Targeted:** Edge Optimization Bonus (TensorRT INT8 Quantization, DeepStream Pipeline & Trade-Off Report)

---

## 👥 Meet Team sync4ce

* **Naguru Kethan (Team Lead & Full-Stack AI Builder)**
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

## 1. Project Description & Problem Statement
Industrial manufacturing floors and high-risk work zones suffer from preventable fatal injuries because traditional CCTV systems only provide passive post-incident recordings. When a worker enters an active robotic/hydraulic press hazard zone or suffers a sudden fall, every millisecond counts—yet streaming raw high-definition video to the cloud introduces unacceptable network latency and violates worker privacy.

**AegisVision** solves this by combining **Workplace Safety Sentinel (Track 1)** and **Fall Detection with Privacy Blur (Track 2)** into a single, ultra-low-latency GPU-accelerated edge vision pipeline built end-to-end in **CraftifAI PipeGen v0.5.1**.

---

## 2. Full 5-Stage PipeGen Architecture (Track A Mandatory Breakdown)

| PipeGen Stage | Implementation Details in AegisVision |
| :--- | :--- |
| **1. Requirement** | *"Detect workers and 17-keypoint human pose on a live shop-floor video/USB camera stream, track persistent worker IDs across frames, flag polygon ROI hazard zone intrusions and fall postures held for >2.0 seconds, apply privacy face blur before saving incident frames, and publish real-time JSON logs and MQTT emergency stop alerts."* |
| **2. Pipeline IR** | Generated multi-node DeepStream graph (`nvurisrcbin` → `nvvideoconvert` → `nvinfer (Primary Detector)` → `nvtracker (NvDCF)` → `nvinfer (Secondary Pose)` → `nvdsanalytics (ROI & Fall Logic)` → `nvdsosd (Privacy Redaction)` → `nvmsgconv / nvmsgbroker (MQTT & JSON Sink)`). |
| **3. Model Selection** | Selected **YOLOv8n-Person** (Primary Detection) and **YOLOv8n-Pose** (17-Keypoint Pose Estimation) via CraftifAI Catalog & Deep Search, exported to dynamic-batch ONNX. |
| **4. Compiler (TensorRT)** | Compiled ONNX models into **TensorRT INT8** (with calibration cache) and **FP16** execution engines (`model_b1_gpu0_int8.engine`). |
| **5. Live Run & Actionable Output** | Executed via `pipegen_export/run.sh` on live video streams under `/home`, streaming real-time JSON metadata and MQTT triggers (`aegis/safety/alerts`) into our **Streamlit OSHA Command Center (`aegis_dashboard.py`)**. |

---

## 3. Evidence 1: PipeGen Stage 2 — Pipeline IR Node Graph

```mermaid
graph LR
    A[Video / USB Camera Input<br/>/home/kethan_07/aegis_videos] --> B[nvvideoconvert &<br/>nvstreammux 1920x1080]
    B --> C[nvinfer: PGIE<br/>YOLOv8n Person INT8]
    C --> D[nvtracker: NvDCF<br/>Persistent Worker IDs]
    D --> E[nvinfer: SGIE<br/>YOLOv8n-Pose 17-Keypoint INT8]
    E --> F[nvdsanalytics<br/>Polygon ROI & Fall >2.0s Check]
    F --> G[nvdsosd<br/>Privacy Face Blur & HUD]
    G --> H1[RTSP / Live OSD Display]
    G --> H2[JSON Telemetry Log<br/>metadata.json]
    G --> H3[MQTT Action Broker :1883<br/>Topic: aegis/safety/alerts]
    H3 --> I[AegisVision Streamlit<br/>Command Center & Relay Trip]
