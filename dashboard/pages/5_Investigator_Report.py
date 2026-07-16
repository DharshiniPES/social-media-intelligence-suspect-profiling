import streamlit as st
from database.db_manager import DatabaseManager

st.set_page_config(page_title="Investigator Report", layout="wide")
st.title("Generate Case Report")
st.caption("Export actionable intelligence for law enforcement or security teams")

st.divider()

db = DatabaseManager()
comparisons = db.get_comparisons()

if not comparisons:
    st.warning("Run an investigation first to generate a report.")
else:
    st.subheader("Automated Case Package")
    
    # Build the report string
    report_text = "SOCMINT FORENSIC REPORT\n"
    report_text += "="*40 + "\n\n"
    
    high_confidence = [row for row in comparisons if row[11] >= 0.70]
    
    report_text += f"Total Comparisons Logged: {len(comparisons)}\n"
    report_text += f"High Confidence Matches: {len(high_confidence)}\n\n"
    
    for row in high_confidence:
        report_text += f"TARGET PAIR: {row[1]} <---> {row[2]}\n"
        report_text += f"CONFIDENCE: {round(row[11]*100, 2)}%\n"
        report_text += f"EXPLANATION: {row[12]}\n"
        report_text += "-"*30 + "\n"
        
    st.text_area("Report Preview", report_text, height=350)
    
    st.download_button(
        label="Download Report as TXT",
        data=report_text,
        file_name="socmint_investigation_report.txt",
        mime="text/plain",
        use_container_width=True
    )