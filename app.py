import streamlit as st
import pandas as pd
import plotly.express as px
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #A8A8B3;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .segment-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #172B40;
        border: 1px solid #263E56;
        margin-bottom: 15px;
    }

    .segment-name {
        font-size: 21px;
        font-weight: 700;
    }

    .segment-description {
        color: #B8C1CC;
        font-size: 15px;
        margin-top: 5px;
    }

    .insight-box {
        padding: 18px;
        border-radius: 10px;
        background-color: #16283A;
        border-left: 4px solid #64B5F6;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .model-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #151922;
        border: 1px solid #30343D;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# PATH
# ============================================================

DATA_FILE = os.path.join(
    "dataset",
    "customer_segments_final.csv"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_FILE)

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Filters")

segments = [
    "All",
    "Emerging Customers",
    "Growth Customers",
    "Premium Customers"
]

selected_segment = st.sidebar.selectbox(
    "Select Customer Segment",
    segments
)


# ============================================================
# FILTER DATA
# ============================================================

if selected_segment == "All":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["Segment"] == selected_segment
    ].copy()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">👥 Customer Segmentation Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of customer behavior, spending patterns, '
    'purchase channels, and marketing response.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# CUSTOMER OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Customer Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Customers",
        f"{len(filtered_df):,}"
    )

with col2:

    st.metric(
        "Average Income",
        f"${filtered_df['Income'].mean():,.0f}"
    )

with col3:

    st.metric(
        "Average Spending",
        f"${filtered_df['TotalSpending'].mean():,.0f}"
    )

with col4:

    st.metric(
        "Average Purchases",
        f"{filtered_df['TotalPurchases'].mean():.1f}"
    )


st.divider()


# ============================================================
# SEGMENT OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Segment Overview</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Customer Distribution
# ------------------------------------------------------------

with col1:

    segment_counts = (
        df["Segment"]
        .value_counts()
        .reindex(
            [
                "Emerging Customers",
                "Growth Customers",
                "Premium Customers"
            ]
        )
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Customers"
    ]

    fig = px.bar(
        segment_counts,
        x="Segment",
        y="Customers",
        title="Customer Distribution by Segment",
        text="Customers"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Average Spending
# ------------------------------------------------------------

with col2:

    spending = (
        df.groupby("Segment")["TotalSpending"]
        .mean()
        .reindex(
            [
                "Emerging Customers",
                "Growth Customers",
                "Premium Customers"
            ]
        )
        .reset_index()
    )

    fig = px.bar(
        spending,
        x="Segment",
        y="TotalSpending",
        title="Average Spending by Segment",
        text_auto=".0f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CUSTOMER BEHAVIOR
# ============================================================

st.markdown(
    '<div class="section-title">Customer Behavior</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Income vs Spending
# ------------------------------------------------------------

with col1:

    fig = px.scatter(
        filtered_df,
        x="Income",
        y="TotalSpending",
        color="Segment",
        hover_data=[
            "Age",
            "TotalPurchases",
            "NumWebVisitsMonth"
        ],
        title="Income vs Total Spending"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Purchase Channels
# ------------------------------------------------------------

with col2:

    channel_data = pd.DataFrame({
        "Channel": [
            "Web",
            "Catalog",
            "Store"
        ],
        "Purchases": [
            filtered_df["NumWebPurchases"].sum(),
            filtered_df["NumCatalogPurchases"].sum(),
            filtered_df["NumStorePurchases"].sum()
        ]
    })

    fig = px.bar(
        channel_data,
        x="Channel",
        y="Purchases",
        title="Purchases by Channel",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PRODUCT PREFERENCES
# ============================================================

st.markdown(
    '<div class="section-title">Product Preferences</div>',
    unsafe_allow_html=True
)

product_data = pd.DataFrame({

    "Product": [
        "Wines",
        "Fruits",
        "Meat",
        "Fish",
        "Sweets",
        "Gold"
    ],

    "Spending": [

        filtered_df["MntWines"].sum(),

        filtered_df["MntFruits"].sum(),

        filtered_df["MntMeatProducts"].sum(),

        filtered_df["MntFishProducts"].sum(),

        filtered_df["MntSweetProducts"].sum(),

        filtered_df["MntGoldProds"].sum()
    ]
})


fig = px.bar(
    product_data,
    x="Product",
    y="Spending",
    title="Total Spending by Product Category",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CAMPAIGN ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Campaign Response</div>',
    unsafe_allow_html=True
)

campaign_data = (
    df.groupby("Segment")["Response"]
    .mean()
    .reindex(
        [
            "Emerging Customers",
            "Growth Customers",
            "Premium Customers"
        ]
    )
    .reset_index()
)

campaign_data["Response Rate (%)"] = (
    campaign_data["Response"] * 100
)

fig = px.bar(
    campaign_data,
    x="Segment",
    y="Response Rate (%)",
    title="Campaign Response Rate by Segment",
    text_auto=".1f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SELECTED SEGMENT DETAILS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Segment Details</div>',
    unsafe_allow_html=True
)


if selected_segment == "All":

    st.info(
        "Select a specific customer segment from the sidebar "
        "to view its detailed profile, business interpretation, "
        "and recommended strategy."
    )

else:

    segment_df = df[
        df["Segment"] == selected_segment
    ].copy()

    customer_count = len(segment_df)

    percentage = (
        customer_count / len(df)
    ) * 100

    avg_age = segment_df["Age"].mean()

    avg_income = segment_df["Income"].mean()

    avg_spending = segment_df["TotalSpending"].mean()

    avg_purchases = segment_df["TotalPurchases"].mean()

    response_rate = (
        segment_df["Response"].mean() * 100
    )


    # --------------------------------------------------------
    # Segment Header
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="segment-card">

            <div class="segment-name">
                {selected_segment}
            </div>

            <div class="segment-description">
                {customer_count:,} customers
                ({percentage:.1f}% of the customer base)
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Segment Metrics
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Average Age",
            f"{avg_age:.1f}"
        )

    with col2:

        st.metric(
            "Average Income",
            f"${avg_income:,.0f}"
        )

    with col3:

        st.metric(
            "Average Spending",
            f"${avg_spending:,.0f}"
        )

    with col4:

        st.metric(
            "Campaign Response",
            f"{response_rate:.1f}%"
        )


    st.markdown("### 🧠 Business Interpretation")


    # --------------------------------------------------------
    # Segment Interpretations
    # --------------------------------------------------------

    interpretations = {

        "Premium Customers":
            "High-value customers with the highest income and "
            "spending levels. They also demonstrate the strongest "
            "campaign response and purchasing activity.",

        "Growth Customers":
            "Moderate-to-high value customers with strong "
            "purchasing behavior. This group represents a strong "
            "opportunity for upselling and movement toward "
            "premium purchasing behavior.",

        "Emerging Customers":
            "The largest customer group, but with relatively low "
            "spending and purchasing activity. The key opportunity "
            "is converting these customers into more active buyers."
    }


    st.markdown(
        f"""
        <div class="insight-box">
            {interpretations[selected_segment]}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Recommended Strategy
    # --------------------------------------------------------

    st.markdown("### 💡 Recommended Strategy")


    recommendations = {

        "Premium Customers": [

            "Prioritize retention and loyalty programs.",

            "Provide premium and personalized offers.",

            "Use cross-selling and high-value product recommendations.",

            "Reward strong campaign engagement."

        ],

        "Emerging Customers": [

            "Focus on converting browsing activity into purchases.",

            "Use entry-level promotions and product bundles.",

            "Provide personalized product recommendations.",

            "Experiment with targeted digital campaigns."

        ],

        "Growth Customers": [

            "Encourage movement toward premium purchasing behavior.",

            "Use cross-selling and upselling strategies.",

            "Introduce loyalty incentives.",

            "Recommend premium products based on purchasing history."

        ]
    }


    for recommendation in recommendations[selected_segment]:

        st.write(
            f"• {recommendation}"
        )


# ============================================================
# MODEL INFORMATION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Model Information</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="model-box">

        <b>Algorithm:</b> K-Means Clustering<br><br>

        <b>Number of Clusters:</b> 3<br><br>

        <b>Customers:</b> 2,237<br><br>

        <b>Clustering Features:</b> 9<br><br>

        <b>Silhouette Score:</b> 0.2477<br><br>

        <b>PCA Explained Variance:</b> 58.21%

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Customer Segmentation Project | "
    "K-Means Clustering | Python + Scikit-learn + Streamlit"
)
