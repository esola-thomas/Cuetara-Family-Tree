import pandas as pd

# File path to the input CSV
file_path = "input.csv"

# Load the family data
df = pd.read_csv(file_path)

# Convert Date of Birth to datetime for sorting
df["Date of Birth"] = pd.to_datetime(df["Date of Birth"])

# Sort data by Hierarchy Level, Date of Birth, and Name
df = df.sort_values(by=["Hierarchy Level", "Date of Birth", "Name"]).reset_index(drop=True)

# Generate the HTML output
output_path = "family_tree.html"

with open(output_path, "w") as file:
    file.write("<html>\n<head>\n<title>Family Tree</title>\n</head>\n<body>\n")
    file.write("<h1>Family Tree</h1>\n")
    current_level = None

    # Loop through the data and create a pyramid-style layout
    for _, row in df.iterrows():
        if row["Hierarchy Level"] != current_level:
            if current_level is not None:
                file.write("</ul>\n")  # Close the previous level's list
            current_level = row["Hierarchy Level"]
            file.write(f"<h2>{current_level.capitalize()}</h2>\n<ul>")  # Start a new list for the hierarchy level
        
        # Add individual as a list item
        file.write(f"<li>{row['Name']} (DOB: {row['Date of Birth'].date()})</li>\n")
    
    file.write("</ul>\n</body>\n</html>")  # Close the final list and HTML document

print(f"Family tree saved to {output_path}")
