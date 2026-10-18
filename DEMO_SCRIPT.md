# AegisVision — Judge Demo Script

**Duration:** 60–90 seconds  
**Important:** This is a scenario-based UI demo. The incident data and JSON are simulated; live camera inference, redaction, MQTT delivery, and machinery control are not active.

## 1. Opening (10 seconds)

“AegisVision is a privacy-conscious industrial-safety prototype exploring how edge-AI video analytics could surface potential falls and restricted-zone events as structured alerts for operators.”

## 2. Scenario 1 — Normal operation (10 seconds)

Select **Scenario 1 · Normal operation**.

“This establishes a baseline. The example shows normal standing and no proposed intervention.”

## 3. Scenario 2 — Restricted-zone intrusion (15 seconds)

Select **Scenario 2 · Restricted-zone intrusion**.

“Here, the example worker crosses a configured restricted-zone boundary. The interface highlights the event and shows a proposed response. This is a simulated action, not a command sent to equipment.”

## 4. Scenario 3 — Fall event (15 seconds)

Select **Scenario 3 · Fall event**.

“This example represents a fall-posture condition persisting beyond a two-second threshold. In a validated deployment, event rules would need testing against labelled video and reviewed site procedures.”

## 5. Show event log and JSON (15 seconds)

Point to the event table and JSON preview.

“The structured payload illustrates the information a future integration could carry: event type, zone, track identifier, and a proposed action. No MQTT message is published by this demo.”

## 6. Close with engineering honesty (10 seconds)

“Our next milestones are to verify the DeepStream/PipeGen runtime, run sample video end-to-end, validate privacy redaction, test delivery to a test MQTT broker, and publish reproducible benchmarks. We are not presenting the current dashboard as a validated safety system.”

## If judges ask what is actually implemented

- **Implemented:** Streamlit dashboard, scenario selector, illustrative event table, JSON preview, architecture sketch.
- **Not verified:** DeepStream/PipeGen runtime, live inference, privacy redaction, TensorRT benchmarks, MQTT delivery.
- **Safety boundary:** no real machinery is connected or controlled.
