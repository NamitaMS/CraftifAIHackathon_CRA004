import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AegisVision | Industrial Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cohesive dark industrial interface. All event and payload data below is simulated.
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
  background:
    radial-gradient(ellipse at 10% 0%, rgba(14, 165, 164, .13), transparent 32%),
    linear-gradient(145deg, #08111f 0%, #0b1422 52%, #0c1726 100%);
}
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1600px; }
h1, h2, h3 { letter-spacing: -0.035em; }
h1 { font-size: clamp(2rem, 4vw, 3rem) !important; font-weight: 800 !important; }
h2, h3 { color: #e5edf8; }
[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(18, 32, 51, .96), rgba(12, 24, 40, .96));
  border: 1px solid #24364b; border-radius: 16px; padding: 18px 20px;
  box-shadow: 0 12px 30px rgba(0,0,0,.14);
}
[data-testid="stMetricLabel"] { color: #9aadc3; font-size: .82rem; }
[data-testid="stMetricValue"] { color: #f0f6ff; font-weight: 750; }
[data-testid="stMetricDelta"] { font-size: .76rem; }
div[data-testid="stAlert"] { border-radius: 12px; }
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-color: #26384d; border-radius: 16px;
}
.stSelectbox [data-baseweb="select"] > div,
.stTextInput input { background: #101e30; border-color: #2a3c52; border-radius: 10px; }
div[data-testid="stDataFrame"] { border: 1px solid #26384d; border-radius: 12px; overflow: hidden; }
.aegis-eyebrow { color: #55d6c2; text-transform: uppercase; letter-spacing: .16em; font-size: .74rem; font-weight: 800; }
.aegis-subtitle { color: #9fb1c8; font-size: 1.05rem; margin-top: -.6rem; margin-bottom: 1.25rem; }
.aegis-team {
  background: linear-gradient(120deg, rgba(17, 38, 57, .95), rgba(14, 28, 46, .9));
  border: 1px solid #29435a; border-radius: 16px; padding: 18px 20px; margin: 12px 0 22px;
  color: #dce8f5; line-height: 1.8;
}
.aegis-team span { color: #91a8bf; }
.aegis-alert { border-radius: 14px; padding: 17px 18px; font-weight: 650; line-height: 1.6; margin: 8px 0 14px; }
.alert-crit { background: rgba(127, 29, 29, .22); border: 1px solid #a83a48; color: #ffc4ca; }
.alert-warn { background: rgba(146, 91, 14, .2); border: 1px solid #a9792c; color: #ffe0a3; }
.alert-safe { background: rgba(13, 115, 91, .18); border: 1px solid #238c79; color: #a9f3dc; }
.aegis-section-note { color: #91a6bc; font-size: .9rem; margin-top: -.5rem; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="aegis-eyebrow">Edge AI · Worker safety · Privacy by design</div>', unsafe_allow_html=True)
st.title("🛡️ AegisVision")
st.markdown(
    '<div class="aegis-subtitle">Industrial safety command-center concept for fall events and restricted-zone scenarios.</div>',
    unsafe_allow_html=True,
)
st.warning(
    "DEMO MODE · All scenario events, event rows, and MQTT/JSON payloads are simulated. "
    "Live camera inference, privacy processing, MQTT delivery, and machinery control are not active."
)

st.markdown("""
<div class="aegis-team">
  <b>sync4ce</b> &nbsp;·&nbsp; <span>Participant CRA004</span><br>
  <span>Team</span> Namita Maruti Sherakhane · Naguru Kethan Kumar Reddy · Kuntimaddi Joshika · Manya Agarwal<br>
  <span>Track</span> CraftifAI PipeGen v0.5.1 · Perception / Edge Optimization concept &nbsp;·&nbsp; <span>Institution</span> PES University, Bengaluru
</div>
""", unsafe_allow_html=True)

st.markdown("### System overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Demo scenarios", "03", "Safe · intrusion · fall")
m2.metric("Event source", "Simulated", "No live inference")
m3.metric("Pipeline status", "Unverified", "DeepStream image download failed")
m4.metric("MQTT connection", "Offline", "Example payload only")

st.divider()

left_col, right_col = st.columns([1.12, 0.88], gap="large")

incidents = [
    {"Timestamp": "22:41:02", "Frame": 1410, "Track ID": "Worker #04", "Zone": "Hydraulic_Press_ROI_1", "Event": "Standing (safe)", "Hold": "0.0 s", "Privacy": "Planned", "Example action": "None (normal)"},
    {"Timestamp": "22:41:08", "Frame": 1455, "Track ID": "Worker #07", "Zone": "Robotic_Arm_ROI_2", "Event": "Zone boundary breach", "Hold": "0.4 s", "Privacy": "Planned", "Example action": "SLOW_MACHINERY_SPEED"},
    {"Timestamp": "22:41:11", "Frame": 1482, "Track ID": "Worker #07", "Zone": "Robotic_Arm_ROI_2", "Event": "Fall posture > 2.0 s", "Hold": "2.3 s", "Privacy": "Planned", "Example action": "EMERGENCY_RELAY_TRIP"},
]

with left_col:
    st.markdown("### 🧪 Scenario explorer")
    st.markdown('<div class="aegis-section-note">Choose an example to preview the intended operator experience.</div>', unsafe_allow_html=True)
    scenario = st.selectbox(
        "Select a demo scenario",
        [
            "Scenario 3 · Fall event (critical example)",
            "Scenario 2 · Restricted-zone intrusion",
            "Scenario 1 · Normal operation",
        ],
        label_visibility="collapsed",
    )

    if "Scenario 3" in scenario:
        active_inc = incidents[2]
        st.markdown(
            f"<div class='aegis-alert alert-crit'>🚨 SIMULATED CRITICAL EVENT<br><b>{active_inc['Track ID']} · {active_inc['Event']}</b><br>Zone: {active_inc['Zone']}<br>Example action: {active_inc['Example action']}</div>",
            unsafe_allow_html=True,
        )
    elif "Scenario 2" in scenario:
        active_inc = incidents[1]
        st.markdown(
            f"<div class='aegis-alert alert-warn'>⚠️ SIMULATED ZONE INTRUSION<br><b>{active_inc['Track ID']} · {active_inc['Event']}</b><br>Zone: {active_inc['Zone']}<br>Example action: {active_inc['Example action']}</div>",
            unsafe_allow_html=True,
        )
    else:
        active_inc = incidents[0]
        st.markdown(
            f"<div class='aegis-alert alert-safe'>✓ SIMULATED NORMAL OPERATION<br><b>{active_inc['Event']}</b><br>Zone: {active_inc['Zone']}<br>Example action: {active_inc['Example action']}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Event log")
    st.caption("Illustrative records only — not produced by a running inference pipeline.")
    st.dataframe(pd.DataFrame(incidents), use_container_width=True, hide_index=True)

    st.markdown("### Example alert payload")
    st.caption("JSON preview for integration planning. No message is being published.")
    payload = {
        "demo": True,
        "benchmark_status": "unverified",
        "participant_id": "CRA004",
        "team_name": "sync4ce",
        "frame_id_example": active_inc["Frame"],
        "worker_track_id_example": active_inc["Track ID"],
        "zone_example": active_inc["Zone"],
        "event_example": active_inc["Event"],
        "hold_time_example": active_inc["Hold"],
        "planned_mqtt_topic": "aegis/safety/alerts",
        "example_action_not_dispatched": active_inc["Example action"],
        "live_inference_latency_ms": None,
    }
    st.json(payload)

with right_col:
    st.markdown("### 🧩 Intended pipeline")
    st.markdown('<div class="aegis-section-note">Design sketch only · execution not verified</div>', unsafe_allow_html=True)
    st.code(
        "VIDEO SOURCE\n"
        "    ↓\n"
        "DECODE + STREAM MUX\n"
        "    ↓\n"
        "PERSON DETECTION (PGIE)\n"
        "    ↓\n"
        "MULTI-OBJECT TRACKING\n"
        "    ↓\n"
        "POSE ESTIMATION (SGIE)\n"
        "    ↓\n"
        "ZONE + TEMPORAL RULES\n"
        "    ↓\n"
        "PRIVACY REDACTION (planned)\n"
        "    ├── Video overlay\n"
        "    ├── Structured event JSON\n"
        "    └── MQTT alert (planned)",
        language="text",
    )

    st.markdown("### 📈 Reported optimization figures")
    st.caption("Claims from the project concept; not independently measured or verified in this environment.")
    perf_df = pd.DataFrame({
        "Precision": ["FP32 baseline", "FP16", "INT8 (reported)"],
        "Latency (ms)": [11.20, 6.10, 3.40],
        "Model FPS": [89.2, 163.9, 294.1],
        "Pipeline FPS": [61.4, 104.2, 142.8],
        "GPU power (W)": [42.0, 31.5, 21.8],
        "Accuracy claim": ["94.2% mAP@50", "94.1%", "93.6%"],
    })
    st.dataframe(perf_df, use_container_width=True, hide_index=True)
    st.info(
        "These are reported comparison figures, not results measured by this demo. "
        "Replace them with reproducible benchmark output once a pipeline runs successfully."
    )

    st.markdown("### 🔌 Integration status")
    st.markdown("""
    - **Streamlit scenario UI:** implemented
    - **Live camera / DeepStream:** not verified
    - **TensorRT benchmarks:** not verified
    - **MQTT broker:** not connected
    - **Real machinery commands:** not active
    """)

st.divider()
st.caption(
    "AegisVision · HackWithBangalore 4.0 · CRA004 · Prototype only. "
    "Do not use this demo to make real-world safety decisions or control machinery."
)
