import pandas as pd
import streamlit as st
import plotly.express as px

# main page title
st.set_page_config(page_title="ChartLyst - Interactive Studio", layout="wide")

# style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: -webkit-linear-gradient(45deg, #FF6B8B, #FF8E53, #9B51E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .subtitle {
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# function
st.markdown('<div class="main-title">ChartLyst Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create, customize, and export interactive charts from your own data in seconds.</div>', unsafe_allow_html=True)

#table manual
if "manual_df" not in st.session_state:
    st.session_state.manual_df = pd.DataFrame({
        "Category": ["Marketing", "Sales", "Development", "Design"],
        "Budget": [5000, 12000, 18000, 7500],
        "Quarter": ["Q1", "Q1", "Q1", "Q1"]
    })

# Step 1: Input Data Front & Center
with st.container(border=True):
    st.markdown("### Step 1: Add Your Data")
    
    input_method = st.radio(
        "Choose how you want to add data:",
        ["Upload File (CSV, Excel)", "Type / Edit Table Manually", "Use Demo Data"],
        horizontal=True
    )

    df = None

    if input_method == "Upload File (CSV, Excel)":
        uploaded_file = st.file_uploader(
            "Drag and drop your dataset here", 
            type=["csv", "xlsx", "json"]
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)
                elif uploaded_file.name.endswith(".json"):
                    df = pd.read_json(uploaded_file)
                st.success("File uploaded successfully!")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    elif input_method == "Type / Edit Table Manually":
        st.write("Edit cells directly, click the bottom `+` row to add rows, or use the bar below to add custom columns:")
        
        #column
        col_bar1, col_bar2, col_bar3, col_bar4 = st.columns([2, 1, 1, 1])
        with col_bar1:
            new_col_name = st.text_input("New Column Name", placeholder="e.g. Profit, Year, Region", label_visibility="collapsed")
        with col_bar2:
            new_col_type = st.selectbox("Type", ["Number", "Text"], label_visibility="collapsed")
        with col_bar3:
            if st.button("Add Column", use_container_width=True):
                col_name_clean = new_col_name.strip()
                if col_name_clean and col_name_clean not in st.session_state.manual_df.columns:
                    default_value = 0 if new_col_type == "Number" else ""
                    st.session_state.manual_df[col_name_clean] = default_value
                    st.rerun()
        with col_bar4:
            if st.button("Reset Table", use_container_width=True):
                st.session_state.manual_df = pd.DataFrame({
                    "Item": ["A", "B", "C"],
                    "Value": [10, 20, 30]
                })
                st.rerun()

        # sss
        edited_table = st.data_editor(
            st.session_state.manual_df, 
            num_rows="dynamic", 
            use_container_width=True
        )
        st.session_state.manual_df = edited_table
        df = edited_table

    elif input_method == "Use Demo Data":
        df = pd.DataFrame({
            "Page_Views": [1200, 1500, 900, 2400],
            "Bounce_Rate": [0.45, 0.38, 0.52, 0.31],
            "Device": ["Mobile", "Desktop", "Mobile", "Tablet"]
        })
        st.info("Loaded demo dataset.")

# custom chart
if df is not None and not df.empty:
    with st.container(border=True):
        st.markdown("### Step 2: Build & Customize Your Chart")

        # colum again
        numeric_cols = df.select_dtypes(include=['float64', 'int64', 'int32', 'float32']).columns.tolist()
        all_cols = df.columns.tolist()

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            chart_type = st.selectbox(
                "Chart Type",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Donut Chart", "Area Chart"]
            )
        with c2:
            x_axis = st.selectbox("X-Axis (Horizontal)", all_cols)
        with c3:
            y_axis = st.selectbox("Y-Axis (Values)", numeric_cols if numeric_cols else all_cols)
        with c4:
            color_choice = st.selectbox(
                "Color Theme",
                ["Pastel", "Prism", "Bold", "Vivid", "Sunset"]
            )

        #color
        color_maps = {
            "Pastel": px.colors.qualitative.Pastel,
            "Prism": px.colors.qualitative.Prism,
            "Bold": px.colors.qualitative.Bold,
            "Vivid": px.colors.qualitative.Vivid,
            "Sunset": px.colors.sequential.Sunset
        }
        selected_palette = color_maps[color_choice]

        #chart
        fig = None
        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, color_discrete_sequence=selected_palette, title=f"{y_axis} by {x_axis}")
        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, markers=True, color_discrete_sequence=selected_palette, title=f"{y_axis} over {x_axis}")
        elif chart_type == "Area Chart":
            fig = px.area(df, x=x_axis, y=y_axis, color_discrete_sequence=selected_palette, title=f"Cumulative {y_axis} by {x_axis}")
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, color_discrete_sequence=selected_palette, title=f"{y_axis} vs {x_axis}")
        elif chart_type == "Donut Chart":
            fig = px.pie(df, names=x_axis, values=y_axis, hole=0.45, color_discrete_sequence=selected_palette, title=f"Distribution of {y_axis}")

        if fig:
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans", size=13),
                margin=dict(t=50, l=20, r=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    # finallllll
    with st.expander("View Data Table & Statistics"):
        t1, t2 = st.tabs(["Full Table", "Statistical Summary"])
        with t1:
            st.dataframe(df, use_container_width=True)
        with t2:
            st.dataframe(df.describe(), use_container_width=True)

else:
    st.info("Please upload a file or choose an input method above to begin generating your charts.")
