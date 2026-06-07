
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="IIoT CyberShield Pro", layout="wide")

st.markdown("""
<style>
.main {
    background-color:#0f172a;
}
h1,h2,h3 {
    color:#38bdf8;
}
div[data-testid="stMetric"] {
    border:1px solid #334155;
    padding:10px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

DB="iiot_pro.db"

conn=sqlite3.connect(DB, check_same_thread=False)
cur=conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS devices(
id INTEGER PRIMARY KEY,
name TEXT,
dtype TEXT,
location TEXT,
firmware TEXT,
risk INTEGER,
level TEXT,
date TEXT
)""")
conn.commit()

st.title("🛡️ IIoT CyberShield Pro")
st.subheader("Industrial IoT Cyber Security & Asset Management Platform")

st.markdown("""
### Developed By
- Muhammad Sameer Niaz (25-ME-151)
- Muhammad Shahbaz Malik (25-ME-155)
- Zain Abbas (25-ME-159)
""")

tabs = st.tabs([
"Dashboard","Asset Inventory","Risk Assessment","Compliance",
"Threat Center","Maintenance","Reports"
])

with tabs[1]:
    st.header("Industrial Asset Inventory")
    name=st.text_input("Device Name")
    dtype=st.selectbox("Type",["PLC","Sensor","Gateway","SCADA","HMI","Robot"])
    location=st.text_input("Location")
    firmware=st.text_input("Firmware Version")

    if st.button("Add Device"):
        cur.execute(
            "INSERT INTO devices(name,dtype,location,firmware,risk,level,date) VALUES(?,?,?,?,?,?,?)",
            (name,dtype,location,firmware,0,"Low",str(datetime.now()))
        )
        conn.commit()
        st.success("Device Added")

    df=pd.read_sql_query("SELECT * FROM devices",conn)
    st.dataframe(df,use_container_width=True)

with tabs[2]:
    st.header("Cyber Risk Assessment")

    weak=st.checkbox("Weak Passwords")
    unenc=st.checkbox("Unencrypted Traffic")
    outdated=st.checkbox("Outdated Firmware")
    ports=st.checkbox("Open Ports")
    segment=st.checkbox("No Segmentation")

    if st.button("Calculate Risk"):
        score=sum([20 if x else 0 for x in [weak,unenc,outdated,ports,segment]])

        if score<=30:
            level="Low"
        elif score<=70:
            level="Medium"
        else:
            level="High"

        st.metric("Risk Score",score)
        st.metric("Risk Level",level)

        st.subheader("Recommendations")
        recs=[
            "Enable MFA",
            "Use TLS Encryption",
            "Update Firmware",
            "Close Unused Ports",
            "Apply Network Segmentation"
        ]
        for r in recs:
            st.write("✅",r)

with tabs[0]:
    st.header("Executive Dashboard")
    df=pd.read_sql_query("SELECT * FROM devices",conn)

    total=len(df)
    avg=round(df["risk"].mean(),1) if total else 0

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Assets",total)
    c2.metric("Avg Risk",avg)
    c3.metric("Factories",df["location"].nunique() if total else 0)
    c4.metric("Security Status","Active")

    if total:
        fig,ax=plt.subplots()
        df["dtype"].value_counts().plot(kind="bar",ax=ax)
        ax.set_title("Asset Distribution")
        st.pyplot(fig)

with tabs[3]:
    st.header("Compliance Checker")
    st.checkbox("IEC 62443 Compliance")
    st.checkbox("ISO 27001 Compliance")
    st.checkbox("NIST Framework")
    st.success("Compliance Review Module")

with tabs[4]:
    st.header("Threat Intelligence Center")
    st.info("Suspicious Login Detection")
    st.info("Malware Monitoring")
    st.info("Anomaly Detection")
    st.info("Network Intrusion Alerts")

with tabs[5]:
    st.header("Predictive Maintenance")
    st.write("Equipment Health Score")
    st.progress(85)

with tabs[6]:
    st.header("Reports")
    df=pd.read_sql_query("SELECT * FROM devices",conn)
    csv=df.to_csv(index=False).encode()
    st.download_button("Download Asset Report",csv,"iiot_report.csv","text/csv")

st.sidebar.title("Platform Features")
st.sidebar.markdown("""
1. Asset Inventory
2. Risk Assessment
3. Security Dashboard
4. Compliance Checker
5. Threat Intelligence
6. Predictive Maintenance
7. CSV Reports
8. Multi-Factory Monitoring
9. Firmware Tracking
10. Security Recommendations
11. Device Classification
12. Executive KPIs
13. Anomaly Detection Module
14. Intrusion Alerts
15. Industrial Cybersecurity Awareness
""")
