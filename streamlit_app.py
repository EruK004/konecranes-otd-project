import streamlit as st
import pandas as pd
import random
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Konecranes OTD Optimizer", layout="wide")
st.title("🏗️ Konecranes Strategic Logistics OTD Optimizer")
st.markdown("""
This tool is based on the **Advanced OTD Accountability Framework**. 
It simulates real-world logistics disruptions and compares data accuracy between the Legacy System and the Proposed Framework.
""")

# 2. Sidebar for Simulation Parameters
st.sidebar.header("⚙️ Simulation Settings")
num_orders = st.sidebar.slider("Total Shipments to Simulate", 50, 1000, 300)
delay_prob = st.sidebar.slider("Projected Delay Probability (%)", 10, 80, 25)
run_btn = st.sidebar.button("🚀 Run Stress Test")

# 3. Core Logic: Root Cause Scenarios based on [cite: 5-35]
# Defined by: Supplier, Logistics, Konecranes, Force Majeure
scenarios = [
    {"cat": "Supplier", "event": "Production Capacity Shortage", "rate": 500, "note": "Goods not ready by confirmed date [cite: 11]"},
    {"cat": "Supplier", "event": "Quality Inspection Failure", "rate": 450, "note": "Rework or replacement required [cite: 12]"},
    {"cat": "Logistics", "event": "Port Congestion / Vessel Delay", "rate": 200, "note": "Delayed during transit after timely handover [cite: 23, 26]"},
    {"cat": "Logistics", "event": "Customs Clearance Bottleneck", "rate": 150, "note": "External administrative delay [cite: 22]"},
    {"cat": "Konecranes", "event": "Late Freight Booking (FCA)", "rate": 250, "note": "Internal planning/process failure [cite: 31]"},
    {"cat": "Konecranes", "event": "Warehouse Receiving Backlog", "rate": 100, "note": "Internal operational constraint [cite: 33]"},
    {"cat": "Force Majeure", "event": "Extreme Weather / Typhoon", "rate": 0, "note": "Act of God - Contractual exemption [cite: 24]"}
]

if run_btn:
    data = []
    for i in range(num_orders):
        is_delayed = random.random() < (delay_prob / 100)
        order_id = f"KC-PO-{5000 + i}"
        
        if is_delayed:
            s = random.choice(scenarios)
            days = random.randint(1, 15)
            penalty = days * s['rate']
            
            # Data Mapping: Comparing Old vs New [cite: 7, 72-73]
            data.append({
                "Order ID": order_id,
                "Delay Event": s['event'],
                "Accountable Party": s['cat'],
                "Delay (Days)": days,
                "Penalty ($)": penalty,
                "Logical Evidence": s['note'],
                "Legacy System Status": "Supplier Delay", # Faulty Default [cite: 7]
                "Proposed Framework": f"{s['cat']} Delay"
            })
    
    df = pd.DataFrame(data)

    # 4. Analytics Dashboard [cite: 48-51]
    st.header("📊 Simulation Analytics Report")
    
    # Key Performance Indicators (KPIs)
    kpi1, kpi2, kpi3 = st.columns(3)
    total_delayed = len(df)
    supplier_fault_new = len(df[df['Accountable Party'] == 'Supplier'])
    
    kpi1.metric("Total Delayed Shipments", total_delayed)
    kpi2.metric("Legacy: Supplier Faults", total_delayed, help="Legacy system defaults all delays to Supplier [cite: 7]")
    kpi3.metric("New: Actual Supplier Faults", supplier_fault_new, 
               delta=f"-{total_delayed - supplier_fault_new} (False Positives Removed)", delta_color="normal")

    st.markdown("---")

    # Visualizations
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Root Cause Distribution (Corrected)")
        fig_pie = px.pie(df, names='Accountable Party', color='Accountable Party',
                         color_discrete_map={'Supplier':'#EF553B', 'Logistics':'#636EFA', 'Konecranes':'#00CC96', 'Force Majeure':'#AB63FA'})
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_right:
        st.subheader("Financial Value Drain by Party ($)")
        fig_bar = px.bar(df, x='Accountable Party', y='Penalty ($)', color='Accountable Party')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed Audit Log
    st.subheader("📋 Detailed Audit Log (For SAP Data Correction)")
    st.dataframe(df, use_container_width=True)
    
    st.success("💡 **Conclusion:** By implementing the new framework, we eliminate unfair penalization of suppliers and identify internal process bottlenecks (e.g., FCA bookings)[cite: 66, 73, 75].")
else:
    st.info("👈 Adjust parameters and click 'Run Stress Test' to begin.")
