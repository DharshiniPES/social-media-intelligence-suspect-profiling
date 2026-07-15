# SOCMINT Suspect Profiling System (Project P1)

## 1. Executive Summary
This project, **"Design and Implementation of a Social Media Intelligence (SOCMINT) Based Suspect Profiling System,"** presents an automated, multi-modal pipeline designed to correlate digital footprints across disparate platforms. By integrating custom scraping engines with a proprietary **Adaptive Fusion Engine**, the system bridges the gap between raw data collection and high-confidence identity resolution, providing a systematic approach to lawful suspect profiling in OSINT environments.

## 2. System Architecture
The system is built upon a layered architecture to ensure scalability and forensic integrity:

*   **Data Acquisition Layer:** Implements asynchronous scraping modules (GitHub/Web) that normalize multi-platform data into a unified `EvidenceProfile` JSON schema.
*   **Feature Engineering Layer:** Transforms raw metadata into structured numerical features across 8 dimensions.
*   **Fusion Intelligence Layer:** The "brain" of the operation, utilizing **Reliability Masking** and **Pivot-Boost** heuristics to compute identity linkage probabilities.
*   **Presentation Layer:** A `Streamlit`-based analytical dashboard allowing investigators to visualize connection clusters and generate evidence reports.

## 3. Technical Methodology

### 3.1. The Adaptive Fusion Engine
A core innovation of this project is the **Adaptive Fusion Engine**. Standard identity resolution tools often suffer from "Zero-Padding Penalties" when platforms lack shared data. Our implementation solves this via:

1.  **Reliability Masking:** The engine performs a real-time assessment of evidence density for each platform. It calculates the final similarity confidence by averaging only those feature modules that contain sufficient, non-zero data, preventing missing fields from artificially deflating the confidence score.
2.  **Pivot-Based Boosting:** A heuristic module identifies "Hard Links"—verified shared identifiers such as identical email addresses or linked portfolio domains. Upon detecting these, the engine applies a logarithmic confidence boost to the final fusion score, shifting the output from "Similarity-Based Prediction" to "Evidence-Based Linkage".

### 3.2. Feature Engineering Modules
*   **String/Semantic Analysis:** Combines Levenshtein distance for usernames and BERT-based vectorization for profile biographies.
*   **Behavioral & Temporal Fingerprinting:** Maps the frequency of interactions and temporal activity windows to determine if two accounts share a common biological "rhythm".
*   **Bot Risk Classification:** A Random Forest-based classifier that analyzes network topology and activity frequency to flag non-human account behavior.
*   **Network Graph Analysis:** Uses `NetworkX` to generate community clusters, mapping the social graph of potential suspects.

## 4. Evaluation & Validation
The system’s performance has been rigorously validated:
*   **Benchmark:** 100 diverse profiles were curated, resulting in 4,950 unique cross-platform comparison points.
*   **Sensitivity Analysis:** Threshold sensitivity was performed to balance Type I and Type II errors.
*   **ROC Analysis:** ROC curves were constructed to determine the optimal "Identity Linkage Threshold," ensuring a high True Positive Rate in forensic applications.

## 5. Directory Structure
```text
/
├── app.py                  # Main Streamlit dashboard
├── core/
│   └── evidence_model.py   # Schema definitions for EvidenceProfile
├── modules/
│   ├── scrapers/           # Platform-specific scraping logic
│   ├── comparison_engine.py# Core Fusion engine logic
│   └── pivot_boost.py      # Hard-link association module
├── pipeline/
│   └── intelligence_pipeline.py # Normalization and ingestion flow
├── requirements.txt        # System dependencies
└── README.md               # Project documentation
```

## 6. Project Acknowledgements
This internship and the resulting SOCMINT profiling system were conducted as a formal research project within the Department of Computer Science at PES University.

* **Research Interns:** 
    * Dharshini V (PES1UG24AM428)
    * Tanmayi Nagabhairava (PES1UG24CS493)
* **Project Mentor:** Dr. Sapna V M, Dept. of Computer Science, PES University
* **Institutional Support:** We extend our gratitude to the Department of Computer Science at PES University for providing the computational resources and guidance necessary to develop this research project.

## 7. Research Scope & Ethical Disclaimer
The system is developed exclusively for the lawful correlation of open-source OSINT information. It is intended for use in academic and investigative research contexts to demonstrate the feasibility of automated social media intelligence. The project strictly adheres to the boundaries of publicly accessible data and does not engage in unauthorized access, privacy infringement, or illegal data retrieval methods.

---
*Documentation last updated: July 2026*
