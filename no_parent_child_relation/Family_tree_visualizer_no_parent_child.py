import pandas as pd
from datetime import datetime
import pytz
import argparse
import os

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate a family tree HTML report.")
parser.add_argument(
    "--input",
    type=str,
    default="input.csv",
    help="Path to the input CSV file (default: input.csv)"
)
args = parser.parse_args()

# File path to the input CSV
file_path = args.input

# Check if the input file exists
if not os.path.isfile(file_path):
    print(f"Error: The input file '{file_path}' does not exist.")
    exit(1)

# Load the family data
df = pd.read_csv(file_path)

# Convert Date of Birth to datetime for sorting
df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], errors="coerce")

# Sort data by Date of Birth and Name to calculate Family Member Numbers
df = df.sort_values(by=["Date of Birth", "Name"]).reset_index(drop=True)

# Add the Family Member Number
df["Family Member Number"] = df.index + 1  # Assign a sequential number based on the sorted order

# Generate the current timestamp in EST
utc_now = datetime.now(pytz.utc)
est = pytz.timezone("US/Eastern")
timestamp = utc_now.astimezone(est).strftime("%Y-%m-%d %I:%M:%S %p %Z")  # Format includes AM/PM and timezone abbreviation

# Generate the HTML output
output_path = "family_tree.html"

try:
    with open(output_path, "w") as file:
        # Generate the HTML structure with injected timestamp
        file.write(f"""
<html>
<head>
<title>Familia Gómez-Cuétara</title>
<style>
    .group {{ display: none; }}
    .group-title {{ display: none; font-weight: bold; }}
    .highlight {{ background-color: yellow; font-weight: bold; }}
</style>
<script>
    // Toggle visibility of a specific group
    function toggleGroup(group) {{
        const elements = document.getElementsByClassName(group);
        for (let i = 0; i < elements.length; i++) {{
            elements[i].style.display = elements[i].style.display === 'none' ? 'block' : 'none';
        }}
    }}

    // Search for a name and highlight results
    function searchName() {{
        const query = document.getElementById('searchBox').value.toLowerCase().trim();
        const groups = document.getElementsByClassName('group');
        let found = false;

        // Toggle all checkboxes to checked and display all groups
        const checkboxes = document.querySelectorAll("input[type='checkbox']");
        checkboxes.forEach((checkbox) => {{
            checkbox.checked = true; // Check all checkboxes
            const groupClass = checkbox.getAttribute("onclick").match(/'(.*?)'/)[1];
            const groupElements = document.getElementsByClassName(groupClass);
            for (let i = 0; i < groupElements.length; i++) {{
                groupElements[i].style.display = 'block'; // Show all groups
            }}
        }});

        // Reset all highlights
        for (let i = 0; i < groups.length; i++) {{
            const items = groups[i].getElementsByTagName('li');
            for (let j = 0; j < items.length; j++) {{
                items[j].classList.remove('highlight');
            }}
        }}

        // Search for the name and highlight exact matches
        for (let i = 0; i < groups.length; i++) {{
            const items = groups[i].getElementsByTagName('li');
            for (let j = 0; j < items.length; j++) {{
                // Perform exact match check instead of partial match
                if (items[j].innerText.toLowerCase().trim() === query) {{
                    items[j].classList.add('highlight');
                    found = true;
                }}
            }}
        }}

        if (!found) {{
            alert("No matches found.");
        }}
    }}
</script>
</head>
<body>
<h1>Familia Gómez-Cuétara</h1>
<h2>Last Generated: {timestamp}</h2>

<!-- Search Box -->
<div>
    <input type="text" id="searchBox" placeholder="Search by name">
    <button onclick="searchName()">Search</button>
</div>
<br>
""")

        # Create checkboxes for each hierarchy level
        levels = df["Hierarchy Level"].unique()
        for level in levels:
            file.write(f"""
<label>
    <input type="checkbox" onclick="toggleGroup('{level.lower()}')" />
    {level.capitalize()}
</label><br>
""")

        # Sort by Hierarchy Level and then by Family Member Number
        for level in levels:
            level_data = df[df["Hierarchy Level"] == level]
            # Add a title with the same group class
            file.write(f'<div class="group-title {level.lower()}" style="display:none;">{level.capitalize()}</div>\n')
            file.write(f'<ul class="group {level.lower()}" style="display:none;">\n')

            # Write each person in this level
            for _, row in level_data.iterrows():
                # Determine if status needs to be displayed
                status = " ✝" if row["Alive"].strip().lower() == "no" else ""
                # Add individual as a list item with Family Member Number
                file.write(f"<li>#{row['Family Member Number']}: {row['Name']} (DOB: {row['Date of Birth'].date()}){status}</li>\n")

            file.write("</ul>\n")  # Close the group's list

        # Close the HTML structure
        file.write("</body>\n</html>")

    print(f"✅ Family tree saved to {output_path}")
except Exception as e:
    print(f"\n❌ Error: An error occurred while generating the HTML: {e}")
