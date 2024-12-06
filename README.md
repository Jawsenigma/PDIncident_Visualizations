# NormanPD Incident Visualizations

**Author**: Tanmay Saxena

## Overview

This project provides an interactive dashboard for visualizing incident reports from the Norman Police Department (NormanPD). The dashboard allows users to upload incident data from a PDF, process it, and visualize it in different forms, including location-time-incident type clustering, comparison of incident types, time series graph and geographic mapping of incidents.

## Features

### PDF Data Upload
- **Functionality**: Users can upload multiple incident data reports by entering URLs separated by comma or uploading pdf files to the server.
- **Process**: Extracted data is parsed and stored in a local SQLite database for analysis and visualization.
- **Benefit**: Provides a simple and efficient way to digitize and manage incident data.

### Incident Clustering: 

The cluster_with_evaluation function clusters incident data, evaluates the clustering quality, and visualizes the results.

- **Data Processing**: Combines location, nature, and time_numeric columns into a single text field for clustering.
- **Text Vectorization**: Uses TfidfVectorizer to convert the combined text data into a sparse matrix of TF-IDF features.
- **Dimensionality Reduction**: Applies TruncatedSVD followed by normalization to reduce the feature space to 100 components.
- **Clustering**: Performs K-Means clustering (true_k clusters) on the reduced data.
- **Evaluation**: Calculates clustering metrics:
- **Homogeneity**: Measures class purity within clusters.
- **Completeness**: Ensures all instances of a class belong to the same cluster.  
- **Silhouette Score**: Assesses cluster cohesion and separation.  
- **Cluster Analysis**: Identifies the top 10 terms for each cluster to interpret cluster characteristics.  
- **Visualization**: Uses PCA to reduce the data to 2D and creates a scatter plot, with clusters colored differently for easy analysis.

### Incident Type Bar Graph
- **Functionality**: Displays a bar graph comparing the frequency of different incident types.
- **Visualization**: Highlights the distribution and dominance of specific incident types.
- **Use Case**: Understand prevalent issues and prioritize responses.

### Geographical Map
- **Functionality**: Geocodes incident locations and plots them on a map centered on Oklahoma.
- **Visualization**: Interactive map shows geographic patterns and clustering of incidents.
- **Use Case**: Pinpoint high-risk areas for better patrol planning.

## Technologies Used

- **SQLite3**: A lightweight database to store and manage incident data.
- **Pandas**: For data manipulation and preparation for visualization.
- **Plotly**: For creating interactive visualizations such as scatter plots and maps.
- **Geopy**: To geocode street addresses into latitude and longitude coordinates for mapping.
- **Scikit-learn**: Used for clustering incidents by time (KMeans) and textual clustering (TF-IDF).
- **Streamlit**: Framework for creating the web interface of the dashboard.
- **Python**: Core programming language used in the development.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jawsenigma/cis6930fa24-project3.git
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. The application will launch in your default browser, allowing you to:

   - Upload incident data from multiple URLs or import several PDFs at once.
   - Visualize incidents in various ways, including:
   - Clustering of incident records.
   - Analysis of different incident types.
   - Time series graphs for tracking incidents over time.
   - Location-based incident reports to identify geographic patterns.


## Data Source

The incident data is expected to be in PDF format, containing reports with details such as incident type, location, and time. These reports are processed and stored in a local SQLite database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Dependencies

Make sure the following libraries are installed:

- `streamlit`
- `pandas`
- `plotly`
- `geopy`
- `scikit-learn`
- `sqlite3`

You can install these libraries by running:

```bash
pip install streamlit pandas plotly geopy scikit-learn sqlite3
```
