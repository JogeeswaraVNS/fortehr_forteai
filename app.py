import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import plotly.graph_objects as go
import itertools
import pandas as pd

# --- DATA PREPARATION ---
levels = ['Low', 'Medium', 'High']
sentiments = ['Negative', 'Neutral', 'Positive']
level_to_num = {'Low': 0, 'Medium': 1, 'High': 2}
sentiment_to_num = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
combinations = list(itertools.product(levels, levels, sentiments))
df = pd.DataFrame(combinations, columns=['Potential', 'Performance', 'Sentiment'])
df['Potential_num'] = df['Potential'].map(level_to_num)
df['Performance_num'] = df['Performance'].map(level_to_num)
df['Sentiment_num'] = df['Sentiment'].map(sentiment_to_num)

def classify(row):
    p, f, s = row['Potential_num'], row['Performance_num'], row['Sentiment_num']
    mapping = {
        (0, 0, 0): ('Layoff Risk', '#FF0000'), (0, 0, 1): ('Exit Risk', '#FF0000'), (0, 0, 2): ('Disengaged Talent', '#FFA500'),
        (0, 1, 0): ('Low Fit / At Risk', '#FF0000'), (0, 1, 1): ('Coach / Evaluate', '#FFA500'), (0, 1, 2): ('Upskill Opportunity', '#FFFF00'),
        (0, 2, 0): ('High Performer, Flight Risk', '#FF0000'), (0, 2, 1): ('Misaligned Star', '#FFA500'), (0, 2, 2): ('Upskill & Retain', '#90EE90'),
        (1, 0, 0): ('Unmotivated / Poor Fit', '#FF0000'), (1, 0, 1): ('Support Needed', '#FFA500'), (1, 0, 2): ('Develop Potential', '#FFFF00'),
        (1, 1, 0): ('Stuck / Watch Closely', '#FFA500'), (1, 1, 1): ('Monitor & Coach', '#FFFF00'), (1, 1, 2): ('Growing Talent', '#90EE90'),
        (1, 2, 0): ('Critical Risk', '#FF0000'), (1, 2, 1): ('Sustain Performance', '#FFA500'), (1, 2, 2): ('Promotion Ready', '#008000'),
        (2, 0, 0): ('Lost Potential', '#FF0000'), (2, 0, 1): ('Reassign / Coaching', '#FFA500'), (2, 0, 2): ('Coachable Star', '#FFFF00'),
        (2, 1, 0): ('Retention Risk', '#FFA500'), (2, 1, 1): ('Develop Strategically', '#90EE90'), (2, 1, 2): ('Leadership Track', '#008000'),
        (2, 2, 0): ('Top Talent, Critical Flight Risk', '#FF0000'), (2, 2, 1): ('Monitor for Promotion', '#90EE90'), (2, 2, 2): ('Mentor / Promote', '#008000')
    }
    return mapping[(p, f, s)]

df[['Label', 'Color']] = df.apply(lambda row: pd.Series(classify(row)), axis=1)

# --- CUBE DRAWING FUNCTION ---
def cube_faces(x, y, z, size, color):
    faces = []
    v = [
        [x, y, z], [x+size, y, z], [x+size, y+size, z], [x, y+size, z],
        [x, y, z+size], [x+size, y, z+size], [x+size, y+size, z+size], [x, y+size, z+size]
    ]
    X, Y, Z = zip(*v)
    quads = [
        (0,1,2,3), (4,5,6,7), (0,1,5,4),
        (2,3,7,6), (1,2,6,5), (3,0,4,7)
    ]
    for quad in quads:
        i, j, k, l = quad
        face = go.Mesh3d(
            x=[X[i], X[j], X[k], X[l]], y=[Y[i], Y[j], Y[k], Y[l]], z=[Z[i], Z[j], Z[k], Z[l]],
            i=[0], j=[1], k=[2],
            color=color, opacity=1.0, hoverinfo='skip', showscale=False
        )
        face2 = go.Mesh3d(
            x=[X[i], X[k], X[l], X[i]], y=[Y[i], Y[k], Y[l], Y[i]], z=[Z[i], Z[k], Z[l], Z[i]],
            i=[0], j=[1], k=[2],
            color=color, opacity=1.0, hoverinfo='skip', showscale=False
        )
        faces.extend([face, face2])
    return faces

# --- PLOTLY FIGURE ---
fig = go.Figure()
size = 0.95
for _, row in df.iterrows():
    x, y, z = row['Potential_num'], row['Performance_num'], row['Sentiment_num']
    color = row['Color']
    faces = cube_faces(x, y, z, size, color)
    for f in faces:
        fig.add_trace(f)

fig.update_layout(
    scene=dict(
        xaxis=dict(title='Potential', tickvals=[0.5, 1.5, 2.5], ticktext=levels),
        yaxis=dict(title='Performance', tickvals=[0.5, 1.5, 2.5], ticktext=levels),
        zaxis=dict(title='Sentiment', tickvals=[0.5, 1.5, 2.5], ticktext=sentiments),
        aspectmode='cube'
    ),
    margin=dict(l=10, r=10, b=10, t=50),
    height=750,
    showlegend=False
)

st.set_page_config(layout="wide")
st.image("ForteAI Logo.png", use_container_width =True)

st.title("ForteHR - where talent meets recognition")
# Sidebar dropdown options
options = [
    "Startup Overview",
    "Problem Statement",
    "Solution Description",
    "Founding Team",
    "Pitch Deck (PDF)",
    "USP"
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

elif selected == "Founding Team":
    st.header("Founding Team")
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        st.subheader("P. Jogeeswara. V. N. S")
        st.write("**Co-Founder**")
        st.write(
            "Phone No. 9063316737"
        )
        st.write(
            "Gmail. jogeeswarapuvvala@gmail.com"
        )

    with col2:
        st.subheader("A. Sai Karthik")
        st.write("**Co-Founder**")
        st.write(
            "Phone No. 8008085533"
        )
        st.write(
            "Gmail. saikarthik.sa@gmail.com"
        )

    st.write(
        "Together, we combine deep domain expertise and technical innovation to solve critical challenges in employee retention."
    )

elif selected == "Pitch Deck (PDF)":
    st.header("Pitch Deck")
    pdf_path = "Pitch Deck ForteHR.pdf"  # Update this path
    pdf_viewer(pdf_path, width=950, height=500)  # Adjust as needed

elif selected == "USP":
    
    st.title("PPS 3D Cube + Visual Insights")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
        st.image("PPS.png", caption="PPS (Potential-Performance-Sentiment)", use_container_width =True)
    with col2:
        st.image("PPS_2D_Negative.png", caption="Sentiment: Negative", use_container_width =True)
    with col3:
        st.image("PPS_2D_Neutral.png", caption="Sentiment: Neutral", use_container_width =True)
    with col4:
        st.image("PPS_2D_Positive.png", caption="Sentiment: Positive", use_container_width =True)


    st.markdown("### Interactive 3D PPS Cube")
    st.plotly_chart(fig, use_container_width=True)