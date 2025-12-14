import pandas as pd

# 1. Load your existing file
df = pd.read_csv('Final_Master_Dataset_2009_2024.csv')

# 2. Create a list to store the new "Long Format" data
new_rows = []

for index, row in df.iterrows():
    # --- Row for the Winner ---
    new_rows.append({
        'Year': row['Year'],
        'AC_Name': row['AC_Name'],
        'PC_Name': row['PC_Name'],  # Keep this for linking!
        'Party': row['Winner_Party'],
        'Votes': row['Winner_Votes'],
        'Position': 'Winner'
    })
    
    # --- Row for the Runner-Up ---
    new_rows.append({
        'Year': row['Year'],
        'AC_Name': row['AC_Name'],
        'PC_Name': row['PC_Name'],
        'Party': row['Runner_Party'],
        'Votes': row['Runner_Votes'],
        'Position': 'Runner-Up'
    })
    
    # --- Row for "Others" (The Third Front) ---
    # Logic: Total - (Winner + Runner)
    others_votes = row['Total_Votes'] - (row['Winner_Votes'] + row['Runner_Votes'])
    
    # Only add "Others" if there are actually votes left over
    if others_votes > 0:
        new_rows.append({
            'Year': row['Year'],
            'AC_Name': row['AC_Name'],
            'PC_Name': row['PC_Name'],
            'Party': 'Others',  # This groups INC/CPM/IND together
            'Votes': others_votes,
            'Position': 'Others'
        })

# 3. Convert to DataFrame and Save
candidate_master_df = pd.DataFrame(new_rows)

# Save it as the file you need
candidate_master_df.to_csv('All_Candidates_Master.csv', index=False)

print("Success! Created 'All_Candidates_Master.csv' with", len(candidate_master_df), "rows.")
