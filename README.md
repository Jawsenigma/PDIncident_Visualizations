# NormanPD Incident Visualizations

**Author**: Tanmay Saxena

## Overview

This project provides an interactive dashboard for visualizing incident reports from the Norman Police Department (NormanPD). The dashboard allows users to upload incident data from a PDF, process it, and visualize it in different forms, including time-based clustering, comparison of incident types, and geographic mapping of incidents.

## Features

### **Data Upload**: 
      Users can upload incident data from a PDF by entering a URL to a hosted PDF. Users can enter multiple URLs in the text box in a comma-separated format or upload multiple PDFs for visualization. The data is then extracted and stored in a local SQLite database for further analysis.
### **Incident Clustering**: 
      The cluster_with_evaluation function clusters incident data, evaluates the clustering quality, and visualizes the results.

- *Data Processing*: Combines location, nature, and time_numeric columns into a single text field for clustering.
- *Text Vectorization*: Uses TfidfVectorizer to convert the combined text data into a sparse matrix of TF-IDF features.
- *Dimensionality Reduction*: Applies TruncatedSVD followed by normalization to reduce the feature space to 100 components.
- *Clustering*: Performs K-Means clustering (true_k clusters) on the reduced data.
- *Evaluation*: Calculates clustering metrics:
- *Homogeneity*: Measures class purity within clusters.
- *Completeness*: Ensures all instances of a class belong to the same cluster.  
- *Silhouette Score*: Assesses cluster cohesion and separation.  
- *Cluster Analysis*: Identifies the top 10 terms for each cluster to interpret cluster characteristics.  
- *Visualization*: Uses PCA to reduce the data to 2D and creates a scatter plot, with clusters colored differently for easy analysis.

- **Incident Types Comparison**: A bar graph displays the comparison of different incident types, helping to visualize the distribution of incidents.
- **Location Mapping**: Incidents are geocoded and visualized on an interactive map centered on Oklahoma. The map shows the location of each incident using geocoded coordinates derived from street names.

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

2. The application will open in your default browser. You will be able to:
   - Upload incident data from a URL or upload multiple pdfs.
   - Visualize incidents in different forms (by time, type, and location).
   - View the clustering of incidents over time and compare incident types.
   - See incidents on a map, centered on Oklahoma.

## Features Breakdown

### PDF Data Upload
- **Functionality**: Users can upload incident data by entering a URL to a hosted PDF file.
- **Process**: Extracted data is parsed and stored in a local SQLite database for analysis and visualization.
- **Benefit**: Provides a simple and efficient way to digitize and manage incident data.

### Time Clustering
- **Functionality**: Clusters incidents by hour and minute.
- **Visualization**: Scatter plot shows clustering patterns, helping analyze incident frequencies over time.
- **Use Case**: Identify peak times for incidents and optimize resource allocation.

### Incident Type Bar Graph
- **Functionality**: Displays a bar graph comparing the frequency of different incident types.
- **Visualization**: Highlights the distribution and dominance of specific incident types.
- **Use Case**: Understand prevalent issues and prioritize responses.

### Geographical Map
- **Functionality**: Geocodes incident locations and plots them on a map centered on Oklahoma.
- **Visualization**: Interactive map shows geographic patterns and clustering of incidents.
- **Use Case**: Pinpoint high-risk areas for better patrol planning.

### Textual Clustering and Visualization
- **Functionality**:
  - Combines the `location`, `nature`, and numeric time fields into a single column, `combined_text`, for unified text processing.
  - Transforms the text data into numerical feature vectors using `TfidfVectorizer`, which computes term frequency-inverse document frequency values while ignoring English stopwords.
  - Reduces the dimensionality of the feature vectors using Latent Semantic Analysis (LSA) via `TruncatedSVD`, making the data suitable for clustering and visualization.
  - Clusters the reduced feature vectors into a specified number of groups (default: 5) using KMeans.
  - Evaluates clustering quality using metrics like homogeneity, completeness, and silhouette scores, providing insights into the clustering effectiveness.
  - Extracts the top terms associated with each cluster, giving context to the groupings.
  - Reduces the clustered data to two dimensions using PCA for scatter plot visualization, making it easier to interpret clusters.
  - Combines `Location` and `Nature` fields into `combined_text`.
  - Uses TF-IDF for vectorization and KMeans for clustering.
  - Reduces dimensionality with PCA for 2D visualization.
- **Visualization**: The clusters are visualized in a Plotly scatter plot where:
  - Each point represents an incident, plotted using two principal components derived from PCA.
  - Points are color-coded based on their cluster assignment.
  - Hovering over a point reveals detailed information, including location, nature, and time, enhancing interpretability.
- **Use Case**: Group similar incidents for deeper analysis of patterns and trends.

### Detailed Clustering Steps

1. **Data Preparation**:
   - Combine `Location` and `Nature` fields into a single column, `combined_text`.

2. **Feature Extraction**:
   - Apply `TfidfVectorizer` to `combined_text` for term frequency-inverse document frequency vectorization.

3. **Clustering**:
   - Use KMeans to cluster data into 5 groups based on textual similarity.

4. **Dimensionality Reduction**:
   - Apply PCA to reduce TF-IDF vectors to 2D for plotting.

5. **Visualization**:
   - Create a Plotly scatter plot of PCA components, with clusters color-coded.

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
