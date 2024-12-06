import os
import sqlite3
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from geopy.geocoders import Nominatim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from project3.fetch import fetch_pdf
from project3.extract import extract_data_from_pdf
from project3.createdb import create_new_db, populate_new_db
from project3.status import generate_summary, remove_file
from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

DB_PATH = os.path.join(os.getcwd(), 'resources', 'normanpd.db')

def get_data_from_db():
    """Fetch data from the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM incident_reports"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def process_time_column(data):
    """Process the time column to convert time into numeric values (minutes)."""
    def convert_time(t):
        if pd.notnull(t) and isinstance(t, str):
            try:
                if len(t) == 5 and t[2] == ':' and t[:2].isdigit() and t[3:].isdigit():
                    return int(t[:2]) * 60 + int(t[3:])
                else:
                    return 0
            except ValueError:
                return 0
        return 0

    data['time_numeric'] = data['time'].apply(convert_time)
    return data


def cluster_with_evaluation(data, true_k=5):
    """Cluster incidents with evaluation metrics and visualization."""
    data = process_time_column(data)
    data['combined_text'] = data['location'] + " " + data['nature'] + " " + data['time_numeric'].astype(str)

    vectorizer = TfidfVectorizer(stop_words='english')
    combined_vectors = vectorizer.fit_transform(data['combined_text'])

    lsa = make_pipeline(TruncatedSVD(n_components=100, random_state=0), Normalizer(copy=False))
    reduced_vectors = lsa.fit_transform(combined_vectors)

    kmeans = KMeans(n_clusters=true_k, random_state=42)
    data['cluster'] = kmeans.fit_predict(reduced_vectors)

    homogeneity = metrics.homogeneity_score(data['cluster'], kmeans.labels_)
    completeness = metrics.completeness_score(data['cluster'], kmeans.labels_)
    silhouette = metrics.silhouette_score(reduced_vectors, kmeans.labels_)

    st.write(f"Homogeneity: {homogeneity:.3f}")
    st.write(f"Completeness: {completeness:.3f}")
    st.write(f"Silhouette Score: {silhouette:.3f}")

    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for i in range(true_k):
        st.write(f"Cluster {i}: ", ", ".join([terms[ind] for ind in order_centroids[i, :10]]))

    pca = PCA(n_components=2, random_state=42)
    reduced_data = pca.fit_transform(reduced_vectors)

    data['PCA1'] = reduced_data[:, 0]
    data['PCA2'] = reduced_data[:, 1]

    fig = px.scatter(
        data,
        x='PCA1',
        y='PCA2',
        color='cluster',
        hover_data=['location', 'nature', 'time'],
        title="Incident Clusters with Dimensionality Reduction",
        labels={'cluster': 'Cluster ID'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig


def generate_bar_graph(data):
    """Generate bar graph of incidents."""
    counts = data['nature'].value_counts().reset_index()
    counts.columns = ['nature', 'count']
    fig = px.bar(
        counts, x='nature', y='count',
        title="Incident Types Comparison", labels={'nature': 'Incident Type', 'count': 'Count'}
    )
    return fig

def visualize_incidents_by_actual_time_line(data):
    """
    Create a time-based line graph of incidents using actual datetime values.
    """
    try:
        data['time'] = pd.to_datetime(data['time'], format="%m/%d/%Y %H:%M")

        data['hour'] = data['time'].dt.hour

        hourly_data = data.groupby('hour').size().reset_index(name='count')

        fig = px.line(
            hourly_data,
            x='hour',
            y='count',
            title="Incident Frequency by Hour of Day",
            labels={'hour': 'Hour of Day', 'count': 'Number of Incidents'},
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        return fig
    except Exception as e:
        st.error(f"An error occurred while processing time data: {e}")
        return None


def geocode_location(location):
    """Geocode location (street) to latitude and longitude using Geopy."""
    geolocator = Nominatim(user_agent="incident_map")
    try:
        location = geolocator.geocode(location)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

def generate_location_map(data):
    """Generate a map of incidents by street, focused on Oklahoma."""
    latitudes = []
    longitudes = []
    locations = data['location'].unique()

    for loc in locations:
        lat, lon = geocode_location(loc)
        if lat and lon:
            latitudes.append(lat)
            longitudes.append(lon)
        else:
            latitudes.append(None)
            longitudes.append(None)

    location_data = pd.DataFrame({
        'location': locations,
        'latitude': latitudes,
        'longitude': longitudes
    })

    data_with_coords = data.merge(location_data, how='left', left_on='location', right_on='location')

    fig = go.Figure(go.Scattermapbox(
        lat=data_with_coords['latitude'],
        lon=data_with_coords['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        text=data_with_coords['location'],
        hoverinfo='text',
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 35.4676, "lon": -97.5164},  
        mapbox_zoom=7,  
        title="Incidents by Street in Oklahoma",
        title_x=0.5,
        geo=dict(scope='usa'),
        margin={"r":0,"t":40,"l":0,"b":0},
    )

    return fig

def main():
    """Streamlit app main function."""
    st.title("NormanPD Incident Visualizations")

    if not os.path.exists("temp"):
        os.makedirs("temp")

    st.header("Upload Incident Data via URL or File")
    pdf_urls = st.text_area("Enter one or more PDF URLs (separated by commas)")
    uploaded_files = st.file_uploader("Or upload PDF files", accept_multiple_files=True, type="pdf")

    if st.button("Process PDF URLs"):
        if pdf_urls.strip():
            urls = [url.strip() for url in pdf_urls.split(",")]
            try:
                for url in urls:
                    pdf_file_path = fetch_pdf(url)
                    records = extract_data_from_pdf(pdf_file_path)
                    create_new_db()
                    populate_new_db(records)
                st.success("PDF URLs processed successfully!")
            except Exception as e:
                st.error(f"Error processing URLs: {e}")
        else:
            st.warning("Please enter at least one URL.")

    if st.button("Process Uploaded PDFs"):
        if uploaded_files:
            try:
                for uploaded_file in uploaded_files:
                    temp_path = os.path.join("temp", uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.read())

                    records = extract_data_from_pdf(temp_path)
                    create_new_db()
                    populate_new_db(records)

                    os.remove(temp_path)

                st.success("Uploaded PDFs processed successfully!")
            except Exception as e:
                st.error(f"Error processing uploaded files: {e}")
        else:
            st.warning("Please upload at least one PDF file.")

    
    st.header("Visualizations")
    data = get_data_from_db()
    if not data.empty:        
        st.subheader("Incident Clustering")
        cluster_fig = cluster_with_evaluation(data)
        st.plotly_chart(cluster_fig)

        st.subheader("Incident Types Comparison")
        bar_fig = generate_bar_graph(data)
        st.plotly_chart(bar_fig)
        
        st.subheader("Incident Frequency by Time")
        time_fig = visualize_incidents_by_actual_time_line(data)
        if time_fig:
            st.plotly_chart(time_fig)
        
        st.subheader("Incident Map")
        location_map = generate_location_map(data)
        st.plotly_chart(location_map)
    else:
        st.warning("No data available for visualization.")

if __name__ == "__main__":
    main()
