import pandas as pd
from pyvis.network import Network

# Load the family data
file_path = "input.csv"  # Update with your file path
df = pd.read_csv(file_path)

# Helper function to assign levels recursively
def assign_levels(data, root_name=None, current_level=0):
    if root_name is None:
        # Top-level nodes (no parent)
        top_level = data[data["Parent"].isna()]
        data.loc[top_level.index, "Level"] = current_level
        for _, row in top_level.iterrows():
            assign_levels(data, root_name=row["Name"], current_level=current_level + 1)
    else:
        # Find children of the current root
        children = data[data["Parent"] == root_name]
        data.loc[children.index, "Level"] = current_level
        for _, row in children.iterrows():
            assign_levels(data, root_name=row["Name"], current_level=current_level + 1)

# Initialize level column
df["Level"] = -1
assign_levels(df)

# Sort within levels by Date of Birth and Name (for tie-breaking)
df["Date of Birth"] = pd.to_datetime(df["Date of Birth"])
df.sort_values(by=["Level", "Date of Birth", "Name"], inplace=True)

# Assign level-based numbers (e.g., grandchild number) and overall family number
df["Level Number"] = df.groupby("Level").cumcount() + 1
df["Overall Number"] = range(1, len(df) + 1)

# Create the family network graph
family_net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")

# Add nodes with additional information
for _, row in df.iterrows():
    title = (
        f"Level: {int(row['Level'])}<br>"
        f"Level Number: {row['Level Number']}<br>"
        f"Overall Number: {row['Overall Number']}<br>"
        f"DOB: {row['Date of Birth'].date()}<br>"
        f"Email: {row['Email']}"
    )
    family_net.add_node(row["Name"], title=title)

# Add edges (relationships)
for _, row in df.iterrows():
    if pd.notna(row["Parent"]):  # Ensure there's a parent column
        family_net.add_edge(row["Parent"], row["Name"])

# Save the visualization as an HTML file
output_path = "family_tree.html"
family_net.write_html(output_path)

print(f"Family tree saved to {output_path}")

# Save the updated DataFrame with Level and Numbering to a CSV file
output_csv_path = "family_data_with_numbers.csv"
df.to_csv(output_csv_path, index=False)
print(f"Updated family data saved to {output_csv_path}")
