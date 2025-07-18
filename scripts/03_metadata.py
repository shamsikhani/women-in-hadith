import pandas as pd
import networkx as nx
import pathlib
import zipfile

def create_metadata_table():
    """Loads raw data, filters for female narrators, calculates network stats,
    and saves the result to a CSV file.
    """
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    isnad_data_dir = base_dir / 'data' / 'raw' / 'isnad-datasets' / 'data'
    processed_data_dir = base_dir / 'data' / 'processed'
    processed_data_dir.mkdir(exist_ok=True)

    # Define paths to the correct source files
    narrators_file = isnad_data_dir / 'variousnarrators.csv'
    hadiths_file = isnad_data_dir / 'hadiths.csv'
    output_csv = processed_data_dir / 'muhaddithat_metadata.csv'

    if not all([narrators_file.exists(), hadiths_file.exists()]):
        print(f"Required data files not found in {isnad_data_dir}")
        return

    print("Creating metadata table...")

    # 1. Load narrators and filter for females
    nodes = pd.read_csv(narrators_file)
    meta = nodes[nodes['gender'] == 'female'].copy()
    meta = meta.rename(columns={'id': 'narrator_id', 'displayname': 'name'})

    # 2. Parse hadiths.csv to create an edge list
    hadiths = pd.read_csv(hadiths_file)
    edges = []
    for index, row in hadiths.iterrows():
        # Clean and split the isnad string into a list of narrator IDs
        isnad_ids = [int(i.strip()) for i in str(row['isnad']).split(',') if i.strip().isdigit()]
        # Create edges from the chain (e.g., A->B->C becomes B->A, C->B)
        if len(isnad_ids) > 1:
            # The chain is typically listed from student to the Prophet,
            # so the transmission is from right to left in the list.
            # e.g., for [C, B, A], edges are (A, B) and (B, C)
            for i in range(len(isnad_ids) - 1):
                edges.append({'from': isnad_ids[i+1], 'to': isnad_ids[i]})
    
    if not edges:
        print("Warning: No edges could be parsed from hadiths.csv.")
        return

    edge_df = pd.DataFrame(edges)

    # 3. Build graph and calculate counts
    G = nx.from_pandas_edgelist(edge_df, 'from', 'to', create_using=nx.DiGraph)

    meta['teacher_count'] = meta['narrator_id'].apply(lambda n: G.in_degree(n) if n in G else 0)
    meta['student_count'] = meta['narrator_id'].apply(lambda n: G.out_degree(n) if n in G else 0)
    meta['hadith_count'] = 0  # Placeholder

    # 4. Select and order columns
    # Use columns available in variousnarrators.csv and add calculated ones
    final_cols = ['narrator_id', 'name', 'teacher_count', 'student_count', 'hadith_count']
    available_cols = [col for col in meta.columns if col in nodes.columns and col not in ['id', 'displayname']]
    final_meta = meta[final_cols + available_cols]

    # 5. Save to CSV
    final_meta.to_csv(output_csv, index=False)
    print(f"Metadata table saved to {output_csv}")

if __name__ == '__main__':
    create_metadata_table()
