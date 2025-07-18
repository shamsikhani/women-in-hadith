import networkx as nx
import pandas as pd
from pyvis.network import Network
import pathlib

def analyze_and_visualize_network():
    """Builds a network of female narrators, calculates centrality, 
    updates the metadata file, and creates an interactive visualization.
    """
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    raw_data_dir = base_dir / 'data' / 'raw'
    processed_data_dir = base_dir / 'data' / 'processed'
    docs_dir = base_dir / 'docs'
    docs_dir.mkdir(exist_ok=True)

    # Define paths
    isnad_data_dir = raw_data_dir / 'isnad-datasets' / 'data'
    hadiths_file = isnad_data_dir / 'hadiths.csv'
    metadata_file = processed_data_dir / 'muhaddithat_metadata.csv'
    output_html = docs_dir / 'muhaddithat_network.html'

    # Check for required files
    if not all([hadiths_file.exists(), metadata_file.exists()]):
        print("Required data not found. Please run scripts 01 and 03 first.")
        return

    print("Building and analyzing network...")

    # 1. Load data and build the full graph
    meta = pd.read_csv(metadata_file)
    hadiths = pd.read_csv(hadiths_file)
    
    # Parse hadiths.csv to create an edge list
    edges = []
    for index, row in hadiths.iterrows():
        isnad_ids = [int(i.strip()) for i in str(row['isnad']).split(',') if i.strip().isdigit()]
        if len(isnad_ids) > 1:
            for i in range(len(isnad_ids) - 1):
                edges.append({'from': isnad_ids[i+1], 'to': isnad_ids[i]})
    
    edge_df = pd.DataFrame(edges)
    G = nx.from_pandas_edgelist(edge_df, 'from', 'to', create_using=nx.DiGraph)

    # 2. Create subgraph with only female nodes
    female_ids = set(meta['narrator_id'])
    Gf = G.subgraph([node for node in G.nodes() if node in female_ids])

    # 3. Set node attributes
    nx.set_node_attributes(Gf, meta.set_index('narrator_id')['name'].to_dict(), 'label')

    # 4. Calculate PageRank and update metadata
    print("Calculating PageRank...")
    pagerank = nx.pagerank(Gf)
    meta['pagerank'] = meta['narrator_id'].map(pagerank)
    meta.to_csv(metadata_file, index=False) # Update the file
    print(f"Updated metadata file with PageRank at {metadata_file}")

    # 5. Create interactive HTML visualization
    print("Generating interactive network visualization...")
    vis = Network(height='750px', width='100%', directed=True, notebook=False, cdn_resources='remote')
    vis.from_nx(Gf)
    
    # Add some physics options for better layout
    vis.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)

    vis.save_graph(str(output_html))
    print(f"Network visualization saved to {output_html}")

if __name__ == '__main__':
    analyze_and_visualize_network()
