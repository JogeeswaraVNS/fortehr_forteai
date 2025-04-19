import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(layout="wide")
st.image("ForteAI Logo.png", use_container_width =True)

st.title("ForteHR - where talent meets recognition")
# Sidebar dropdown options
options = [
    "Startup Overview",
    "Problem Statement",
    "Solution Description",
    "Pitch Deck (PDF)"
]

selected = st.sidebar.selectbox("Select content to view", options)

if selected == "Startup Overview":
    st.header("Startup Overview")
    st.write("""
    Our startup harnesses the power of artificial intelligence to help organizations tackle the critical challenges of employee attrition and retention. 
    By analyzing performance data, engagement metrics, and behavioral patterns, our AI-driven platform identifies star performers and predicts employees at risk of leaving. 
    This empowers HR teams to take proactive, personalized actions to retain top talent, boost employee satisfaction, and reduce costly turnover. 
    With our innovative solution, companies can build a more engaged, productive, and loyal workforce, ensuring long-term success in today’s competitive business environment.
    """)

elif selected == "Problem Statement":
    st.header("Problem Statement")
    st.write("""
    The problem we are solving is the high employee attrition and the challenge of retaining top talent that organizations face today. 
    Many companies struggle to identify their star performers early enough and lack effective strategies to keep these valuable employees engaged and committed. 
    This leads to costly turnover, loss of critical skills, and disruption in productivity. 
    By leveraging AI techniques, our solution helps HR teams accurately identify high-performing employees and predict those at risk of leaving, enabling timely and personalized retention efforts that improve employee satisfaction and reduce attrition rates.
    """)

elif selected == "Solution Description":
    st.header("Solution Description")
    st.write("""
    Our startup leverages advanced AI techniques to empower HR teams with actionable insights, enabling them to identify star performers, predict attrition risks, and personalize retention strategies. 
    The platform integrates with existing HR systems to analyze performance, engagement, and communication data, providing timely alerts and recommendations. 
    This helps organizations reduce turnover costs, boost employee engagement, and maintain a competitive advantage by retaining their best talent.
    """)

elif selected == "Pitch Deck (PDF)":
    st.header("Pitch Deck")
    pdf_path = "Pitch Deck ForteHR.pdf"  # Update this path
    pdf_viewer(pdf_path, width=950, height=500)  # Adjust as needed
