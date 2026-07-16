import streamlit as st
from database.db_manager import DatabaseManager

st.set_page_config(page_title="Timeline Analysis", layout="wide")
st.title("Investigation Timeline")
st.caption("Chronological view of cross-platform activity")

st.divider()
st.info("Cross-Modal Temporal Data is actively scanning in the backend Ranking Pipeline.")

db = DatabaseManager()
comparisons = db.get_comparisons()

if not comparisons:
    st.warning("No investigation data found. Run a search first.")
else:
    st.write("### Recent Temporal Matches")
    found_temporal = False
    
    # Loop through recent comparisons to find timeline matches
    for row in comparisons[-10:]: 
        # row[1] = p1, row[2] = p2, row[11] = fusion_score, row[12] = explanation
        if row[12] and "temporal pattern" in str(row[12]).lower():
            found_temporal = True
            st.success(f"Temporal Link between **{row[1]}** and **{row[2]}**")
            st.write(f"**Confidence:** {round(row[11]*100, 2)}%")
            st.write(f"**Reason:** {row[12]}")
            st.divider()
            
    if not found_temporal:
        st.caption("No accounts with identical posting cadences detected yet.")