import streamlit as st
import pandas as pd

st.title("📋 Investigation Results")

if "results" not in st.session_state:

    st.warning(
        "Run an investigation first."
    )

    st.stop()

results = st.session_state["results"]
target = st.session_state["target"]
best = results[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Target",
        target
    )

with c2:
    st.metric(
        "Candidates",
        len(results)
    )

with c3:
    st.metric(
        "Top Platform",
        best["candidate"].platform
    )

with c4:
    st.metric(
        "Best Fusion",
        f"{best['fusion_score']*100:.1f}%"
    )
rows = []

for i, r in enumerate(results, start=1):

    rows.append({

        "Rank": i,

        "Username": r["candidate"].username,

        "Platform": r["candidate"].platform,

        "Fusion": round(
            r["fusion_score"]*100,
            2
        )

    })

df = pd.DataFrame(rows)

st.dataframe(
    df,
    use_container_width=True
)
selected = st.selectbox(

    "Inspect Candidate",

    range(len(results)),

    format_func=lambda i:
        f"{results[i]['candidate'].platform} | {results[i]['candidate'].username}"

)

candidate = results[selected]
from modules.decision_engine import DecisionEngine

confidence = DecisionEngine.classify(
    candidate["fusion_score"]
)
st.metric(
    "Confidence",
    confidence
)
st.subheader("Evidence Breakdown")

left, right = st.columns(2)

with left:

    st.metric(
        "Username",
        f"{candidate['username_score']*100:.1f}%"
    )

    st.metric(
        "Bio",
        f"{candidate['bio_score']*100:.1f}%"
    )

    st.metric(
        "Stylometry",
        f"{candidate['stylometry_score']*100:.1f}%"
    )

with right:

    st.metric(
        "Behaviour",
        f"{candidate['behaviour_score']*100:.1f}%"
    )

    st.metric(
        "Temporal",
        f"{candidate['temporal_score']*100:.1f}%"
    )

    st.metric(
        "Hyperlinks",
        f"{candidate['hyperlink_score']*100:.1f}%"
    )
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Fusion",
        f"{candidate['fusion_score']*100:.1f}%"
    )

with c2:
    st.metric(
        "Confidence",
        confidence
    )

with c3:
    st.metric(
        "Platform",
        candidate["candidate"].platform
    )

with c4:
    st.metric(
        "Username",
        candidate["candidate"].username
    )
