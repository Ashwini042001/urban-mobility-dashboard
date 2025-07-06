import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import plotly.express as px

# --- Caching data load for speed ---
@st.cache_data(show_spinner=True)
def load_data():
    conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")
    df = pd.read_sql("SELECT * FROM trips LIMIT 10000", conn)
    conn.close()
    lookup_path = r"C:\Users\Ashwini\urban-mobility-dashboard\data\lookup\taxi_zone_lookup.csv"
    try:
        zone_lookup = pd.read_csv(lookup_path)
        df = df.merge(
            zone_lookup[['LocationID', 'Zone']],
            how='left',
            left_on='PULocationID',
            right_on='LocationID'
        ).rename(columns={'Zone': 'pickup_zone'}).drop(columns=['LocationID'])
    except Exception:
        df['pickup_zone'] = df['PULocationID'].astype(str)

    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['trip_duration_mins'] = (
        df['dropoff_datetime'] - df['pickup_datetime']
    ).dt.total_seconds() / 60
    df['weekday'] = df['pickup_datetime'].dt.weekday
    df['day_type'] = df['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    df['fare_per_mile'] = df['fare_amount'] / df['trip_distance'].replace(0, np.nan)
    df['speed_mph'] = df['trip_distance'] / (df['trip_duration_mins'] / 60).replace(0, np.nan)
    df['no_tip'] = df['tip_amount'] == 0
    df['trip_date'] = df['pickup_datetime'].dt.date
    return df

df = load_data()

st.set_page_config(
    page_title="NYC Taxi Dashboard - Industry Level",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🚕 NYC Yellow Taxi Trips Dashboard")

# ---------------- Sidebar ----------------
st.sidebar.header("🔍 Filters & Settings")

min_date, max_date = df['trip_date'].min(), df['trip_date'].max()
zones_all = sorted(df['pickup_zone'].dropna().unique())
max_passenger_count = int(df['passenger_count'].max())

if 'date_range' not in st.session_state:
    st.session_state.date_range = (min_date, max_date)
if 'hour_range' not in st.session_state:
    st.session_state.hour_range = (0, 23)
if 'min_passengers' not in st.session_state:
    st.session_state.min_passengers = 1
if 'selected_zones' not in st.session_state:
    st.session_state.selected_zones = zones_all.copy()

date_range_val = st.session_state.date_range
if isinstance(date_range_val, pd.Timestamp):
    date_range_val = (date_range_val, date_range_val)

selected_dates = st.sidebar.date_input(
    "Select Pickup Date Range",
    value=date_range_val,
    min_value=min_date,
    max_value=max_date,
    key='date_range'
)
if isinstance(selected_dates, pd.Timestamp):
    filter_start_date = filter_end_date = selected_dates
else:
    filter_start_date, filter_end_date = selected_dates

hour_range = st.sidebar.slider(
    "Select Hour Range", 0, 23,
    value=st.session_state.hour_range, key='hour_range'
)
min_passengers = st.sidebar.slider(
    "Min Passenger Count", 0, max_passenger_count,
    value=st.session_state.min_passengers, key='min_passengers'
)
selected_zones = st.sidebar.multiselect(
    "Filter by Pickup Zone",
    options=zones_all,
    default=st.session_state.selected_zones,
    key='selected_zones'
)

# ---------------- Data Filter ----------------
filtered_df = df[
    (df['trip_date'] >= filter_start_date) &
    (df['trip_date'] <= filter_end_date) &
    (df['hour'].between(hour_range[0], hour_range[1])) &
    (df['passenger_count'] >= min_passengers) &
    (df['pickup_zone'].isin(selected_zones))
].copy()

st.markdown(f"### Data Overview: Showing {len(filtered_df):,} trips after filtering")

# ---------------- Key Metrics ----------------
col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap="large")

fmt_money   = lambda x: f"${x:,.2f}".rjust(12)
fmt_percent = lambda x: f"{x:.2f}%".rjust(8)
fmt_number  = lambda x: f"{x:,}".rjust(10)

col1.markdown(f"**Total Trips**\n\n`{fmt_number(len(filtered_df))}`")
col2.markdown(f"**Median Fare ($)**\n\n`{fmt_money(filtered_df['fare_amount'].median())}`")
col3.markdown(f"**Total Revenue ($)**\n\n`{fmt_money(filtered_df['total_amount'].sum())}`")
col4.markdown(f"**Total Tips ($)**\n\n`{fmt_money(filtered_df['tip_amount'].sum())}`")

avg_tip_pct = ((filtered_df['tip_amount'] / filtered_df['fare_amount'])
               .replace([np.inf, -np.inf], 0).fillna(0)*100).mean()
col5.markdown(f"**Avg Tip %**\n\n`{fmt_percent(avg_tip_pct)}`")

no_tip_pct = filtered_df['no_tip'].mean()*100
col6.markdown(f"**Trips Without Tip (%)**\n\n`{fmt_percent(no_tip_pct)}`")

avg_speed = filtered_df['speed_mph'].replace([np.inf, -np.inf], np.nan).mean()
col7.markdown(f"**Avg Speed (mph)**\n\n`{fmt_money(avg_speed)}`")

st.markdown("---")

plotly_config = {
    'scrollZoom': True,
    'displayModeBar': True,
    'modeBarButtonsToAdd': ['pan2d'],
    'doubleClick': 'reset'
}

# ---------------- Tabs ----------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📍 Insights", "📥 Export"])

# ----- Overview Tab -----
with tab1:
    trip_counts_day = filtered_df.groupby('trip_date').size().reset_index(name='trip_count')
    st.plotly_chart(
        px.line(trip_counts_day, x='trip_date', y='trip_count',
                title="Daily Trip Counts Over Time",
                labels={'trip_date': 'Date', 'trip_count': 'Number of Trips'}),
        use_container_width=True, config=plotly_config
    )

    trip_hour_daytype = filtered_df.groupby(['hour', 'day_type']).size().reset_index(name='count')
    st.plotly_chart(
        px.bar(trip_hour_daytype, x='hour', y='count', color='day_type',
               title="Trips by Hour and Day Type",
               labels={'hour': 'Hour', 'count': 'Trips'}, barmode='stack'),
        use_container_width=True, config=plotly_config
    )

    st.plotly_chart(
        px.box(filtered_df, x='passenger_count', y='fare_amount', points="outliers",
               title="Fare Amount Distribution by Passenger Count",
               labels={'passenger_count': 'Passengers', 'fare_amount': 'Fare ($)'}),
        use_container_width=True, config=plotly_config
    )

    st.plotly_chart(
        px.histogram(filtered_df, x='fare_per_mile', nbins=40, marginal="box",
                     title="Fare per Mile Distribution",
                     labels={'fare_per_mile': 'Fare per Mile ($/mile)'}),
        use_container_width=True, config=plotly_config
    )

    # Revenue by Hour
    revenue_hour = filtered_df.groupby('hour')['total_amount'].sum().reset_index()
    st.plotly_chart(
        px.bar(revenue_hour, x='hour', y='total_amount',
               title="Total Revenue by Hour",
               labels={'hour': 'Hour', 'total_amount': 'Revenue ($)'}),
        use_container_width=True, config=plotly_config
    )

    # Passenger Count Distribution
    passenger_counts = filtered_df['passenger_count'].value_counts().sort_index()
    st.plotly_chart(
        px.bar(x=passenger_counts.index, y=passenger_counts.values,
               title="Passenger Count Distribution",
               labels={'x': 'Passenger Count', 'y': 'Trips'}),
        use_container_width=True, config=plotly_config
    )

# ----- Insights Tab -----
with tab2:
    st.markdown("### 🏙️ Top 10 Pickup Zones by Trip Count")
    st.bar_chart(filtered_df['pickup_zone'].value_counts().head(10))

    st.markdown("### 🎯 Top 10 Dropoff Locations by Trip Count")
    st.bar_chart(filtered_df['DOLocationID'].value_counts().head(10))

    st.markdown("### 📉 Fare vs Distance Scatter (first 1000 trips)")
    st.plotly_chart(
        px.scatter(filtered_df.head(1000), x='trip_distance', y='fare_amount',
                   title="Fare vs Distance",
                   labels={'trip_distance': 'Distance (miles)', 'fare_amount': 'Fare ($)'},
                   opacity=0.5),
        use_container_width=True, config=plotly_config
    )

    st.markdown("### 🚦 Trip Speed Distribution")
    st.plotly_chart(
        px.histogram(filtered_df.replace([np.inf, -np.inf], np.nan), x='speed_mph', nbins=50,
                     title="Speed Distribution (mph)", labels={'speed_mph': 'Speed (mph)'}),
        use_container_width=True, config=plotly_config
    )

    st.markdown("### 🔥 Heatmap: Trips by Hour and Pickup Zone")
    heatmap = filtered_df.groupby(['hour', 'pickup_zone']).size().unstack(fill_value=0)
    st.plotly_chart(
        px.imshow(heatmap.T, labels=dict(x="Hour", y="Pickup Zone", color="Trips"),
                  aspect="auto", title="Trips Heatmap (Hour vs Zone)"),
        use_container_width=True, config=plotly_config
    )

    # Tip vs Fare Scatter
    st.markdown("### 💸 Tip vs Fare")
    st.plotly_chart(
        px.scatter(filtered_df, x='fare_amount', y='tip_amount',
                   title="Tip vs Fare",
                   labels={'fare_amount': 'Fare ($)', 'tip_amount': 'Tip ($)'},
                   opacity=0.6),
        use_container_width=True, config=plotly_config
    )

    # Duration vs Distance with correlation
    corr = filtered_df[['trip_duration_mins', 'trip_distance']].corr().iloc[0, 1]
    st.markdown(f"**Correlation (Duration vs Distance):** {corr:.2f}")
    st.plotly_chart(
        px.scatter(filtered_df, x='trip_distance', y='trip_duration_mins',
                   title="Duration vs Distance",
                   labels={'trip_distance': 'Distance (miles)', 'trip_duration_mins': 'Duration (mins)'},
                   opacity=0.5),
        use_container_width=True, config=plotly_config
    )

    # Avg Revenue per Trip by Zone
    st.markdown("### 💰 Avg Revenue per Trip (Top 10 Zones)")
    rev_zone = (filtered_df.groupby('pickup_zone')['total_amount']
                .mean().sort_values(ascending=False).head(10))
    st.plotly_chart(
        px.bar(rev_zone, x=rev_zone.index, y=rev_zone.values,
               labels={'x': 'Pickup Zone', 'y': 'Avg Revenue ($)'},
               title="Avg Revenue per Trip by Zone"),
        use_container_width=True, config=plotly_config
    )

    # Weekday vs Weekend
    st.markdown("### 📅 Weekday vs Weekend Performance")
    d_rt = (filtered_df.groupby('day_type')
            .agg(revenue=('total_amount', 'sum'),
                 trips=('trip_date', 'count'))
            .reset_index())
    st.plotly_chart(
        px.bar(d_rt, x='day_type', y='revenue',
               title="Revenue: Weekday vs Weekend",
               labels={'day_type': 'Day', 'revenue': 'Revenue ($)'}),
        use_container_width=True, config=plotly_config
    )
    st.plotly_chart(
        px.bar(d_rt, x='day_type', y='trips',
               title="Trips: Weekday vs Weekend",
               labels={'day_type': 'Day', 'trips': 'Trips'}),
        use_container_width=True, config=plotly_config
    )

    # Fare Anomalies
    thresh = filtered_df['fare_per_mile'].quantile(0.99)
    anomalies = filtered_df[filtered_df['fare_per_mile'] > thresh]
    st.markdown(f"### ⚠️ Fare Anomalies (Fare/Mile > {thresh:.2f})")
    st.dataframe(anomalies[['pickup_datetime', 'pickup_zone',
                            'trip_distance', 'fare_amount', 'fare_per_mile']].head(10))

# ----- Export Tab -----
with tab3:
    st.markdown("### ⬇️ Download Data")
    st.download_button(
        "Filtered Trips CSV",
        filtered_df.to_csv(index=False).encode('utf-8'),
        "nyc_taxi_filtered_trips.csv",
        "text/csv"
    )
    summary_csv = filtered_df.describe(include='all').T.to_csv().encode('utf-8')
    st.download_button(
        "Data Summary CSV",
        summary_csv,
        "nyc_taxi_data_summary.csv",
        "text/csv"
    )
