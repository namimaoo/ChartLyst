import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="ChartLyst", layout="wide")


st.markdown("""
    <style>
    /* Clean Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Gradient Header */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: -webkit-linear-gradient(45deg, #FF6B8B, #FF8E53, #9B51E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    
    .subtitle {
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 24px;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
    }
    
    /* Smooth Button Corners */
    .stButton>button {
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">ChartLyst Data Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform raw datasets into structured tables, metrics, and visual analytics.</div>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### Data Source")
    uploaded_file = st.file_uploader(
        "Upload dataset", type=["csv", "xlsx", "json"], help="Supported formats: CSV, XLSX, JSON"
    )

    sample_choice = st.radio(
        "Would you like to use web/app data instead?", 
        options=["No", "Yes"], 
        index=0
    )
    use_sample = sample_choice == "Yes"

df = None


if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")

elif use_sample:
    # data 4 me
    df = pd.DataFrame(
        {
            "Page_Views": [1200, 1500, 900, 2400],
            "Bounce_Rate": [0.45, 0.38, 0.52, 0.31],
            "Device": ["Mobile", "Desktop", "Mobile", "Tablet"],
        }
    )

# main page
if df is not None:
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Rows", f"{df.shape[0]:,}")
    with k2:
        st.metric("Total Columns", f"{df.shape[1]}")
    with k3:
        st.metric("Missing Values", f"{df.isnull().sum().sum()}")
    with k4:
        numeric_count = len(df.select_dtypes(include=['float64', 'int64']).columns)
        st.metric("Numeric Metrics", f"{numeric_count}")

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Visualization Studio", "Data Table", "Statistical Summary"])

    # ui
    with tab1:
        with st.container(border=True):
            st.markdown("#### Chart Designer")
            
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            all_cols = df.columns.tolist()

            c1, c2, c3 = st.columns(3)
            with c1:
                chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Donut Chart"])
            with c2:
                x_axis = st.selectbox("X-Axis (Dimension)", all_cols)
            with c3:
                y_axis = st.selectbox("Y-Axis (Metric)", numeric_cols if numeric_cols else all_cols)

            color_by = st.selectbox("Group By (Optional)", [None] + categorical_cols)

            # coloring
            palette = px.colors.qualitative.Pastel

            fig = None
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_by, 
                             color_discrete_sequence=palette,
                             title=f"{y_axis} by {x_axis}")
            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, color=color_by, 
                              markers=True,
                              color_discrete_sequence=palette,
                              title=f"{y_axis} over {x_axis}")
            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, 
                                 size=numeric_cols[0] if numeric_cols else None,
                                 color_discrete_sequence=palette,
                                 title=f"{y_axis} vs {x_axis}")
            elif chart_type == "Donut Chart":
                fig = px.pie(df, names=x_axis, values=y_axis, 
                             hole=0.45,
                             color_discrete_sequence=palette,
                             title=f"Distribution of {y_axis} by {x_axis}")

            if fig:
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans", size=13),
                    margin=dict(t=50, l=20, r=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

    # making table
    with tab2:
        with st.container(border=True):
            st.markdown("#### Tabular View")
            st.dataframe(df, use_container_width=True)

    # Table summary
    with tab3:
        with st.container(border=True):
            st.markdown("#### Column Overview")
            summary_df = pd.DataFrame({
                "Column Name": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Null Values": df.isnull().sum().values,
                "Unique Values": df.nunique().values
            })
            st.dataframe(summary_df, use_container_width=True)
            
            st.markdown("#### Descriptive Statistics")
            st.dataframe(df.describe(), use_container_width=True)

else:
    with st.container(border=True):
        st.info("Open the left sidebar to upload a data file or select 'Yes' to explore web/app sample data.")
