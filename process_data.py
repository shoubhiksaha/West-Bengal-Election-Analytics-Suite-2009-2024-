import pandas as pd
import numpy as np
import os

# --- CONFIGURATION ---
# MAKE SURE THESE MATCH YOUR FILE NAMES EXACTLY
FILE_2024 = '2024data.csv'
FILE_VS_HISTORY = 'TCPD_AE_West_Bengal_2025-12-7.csv'       # Vidhan Sabha (2011, 2016, 2021)
FILE_LS_HISTORY = 'TCPD_GA_West_Bengal_2025-12-12 (1).csv' # Lok Sabha Segments (2009, 2014, 2019)
OUTPUT_FILE = 'Final_Master_Dataset_2009_2024.csv'

def process_2024():
    print("Processing 2024 Data...")
    try:
        df = pd.read_csv(FILE_2024, header=1)
        wb = df[df['State/UT Name'] == 'West Bengal'].copy()
        wb['VOTES SECURED EVM'] = pd.to_numeric(wb['VOTES SECURED EVM'], errors='coerce').fillna(0)
        
        # Calculate Rank per AC
        wb['Rank'] = wb.groupby('AC NO')['VOTES SECURED EVM'].rank(method='first', ascending=False)
        
        # Winners & Runners
        winners = wb[wb['Rank'] == 1][['AC NO', 'AC NAME', 'PC NAME', 'PARTY', 'VOTES SECURED EVM']]
        winners.columns = ['AC_No', 'AC_Name', 'PC_Name', 'Winner_Party', 'Winner_Votes']
        
        runners = wb[wb['Rank'] == 2][['AC NO', 'VOTES SECURED EVM', 'PARTY']]
        runners.columns = ['AC_No', 'Runner_Votes', 'Runner_Party']
        
        total = wb.groupby('AC NO')['VOTES SECURED EVM'].sum().reset_index()
        total.columns = ['AC_No', 'Total_Votes']
        
        final = winners.merge(runners, on='AC_No').merge(total, on='AC_No')
        final['Year'] = 2024
        final['Election_Type'] = 'Lok Sabha'
        return final
    except Exception as e:
        print(f"Error in 2024: {e}")
        return pd.DataFrame()

def process_tcpd_file(filename, election_type, years):
    print(f"Processing {election_type} ({years})...")
    try:
        df = pd.read_csv(filename)
        # Filter Years
        df = df[df['Year'].isin(years)].copy()
        
        # TCPD Format: Position 1=Winner, 2=Runner
        winners = df[df['Position'] == 1].copy()
        runners = df[df['Position'] == 2].copy()
        
        # Rename Cols
        # Note: TCPD files usually use 'Constituency_No' and 'Constituency_Name'
        cols_map = {
            'Constituency_No': 'AC_No', 
            'Constituency_Name': 'AC_Name', 
            'Party': 'Winner_Party', 
            'Votes': 'Winner_Votes',
            'Valid_Votes': 'Total_Votes'
        }
        if 'PC_Name' in df.columns:
            cols_map['PC_Name'] = 'PC_Name'
            
        winners = winners.rename(columns=cols_map)
        
        # Keep only necessary columns
        keep_cols = ['AC_No', 'AC_Name', 'Year', 'Winner_Party', 'Winner_Votes', 'Total_Votes']
        if 'PC_Name' in winners.columns:
            keep_cols.append('PC_Name')
            
        winners = winners[keep_cols]
        
        # Process Runners
        runners = runners.rename(columns={'Constituency_No': 'AC_No', 'Party': 'Runner_Party', 'Votes': 'Runner_Votes'})
        runners = runners[['AC_No', 'Year', 'Runner_Party', 'Runner_Votes']]
        
        # Merge
        final = winners.merge(runners, on=['AC_No', 'Year'], how='left')
        final['Election_Type'] = election_type
        return final
        
    except Exception as e:
        print(f"Error in {election_type}: {e}")
        return pd.DataFrame()

# --- MAIN ---
if __name__ == "__main__":
    
    # 1. Process All 3 Sources
    df_2024 = process_2024()
    df_vs   = process_tcpd_file(FILE_VS_HISTORY, 'Vidhan Sabha', [2011, 2016, 2021])
    df_ls   = process_tcpd_file(FILE_LS_HISTORY, 'Lok Sabha', [2009, 2014, 2019])
    
    # 2. Combine
    print("Combining all datasets...")
    master = pd.concat([df_2024, df_vs, df_ls], ignore_index=True)
    
    # 3. Cleanup
    # Fill missing PC Names in VS data using the 2024 mapping
    if not df_2024.empty:
        pc_map = df_2024[['AC_No', 'PC_Name']].drop_duplicates().set_index('AC_No')['PC_Name'].to_dict()
        master['PC_Name'] = master['PC_Name'].fillna(master['AC_No'].map(pc_map))
    
    # Calculate Margins
    master['Margin_Votes'] = master['Winner_Votes'] - master['Runner_Votes']
    master['Margin_Percent'] = (master['Margin_Votes'] / master['Total_Votes']) * 100
    
    # Sort
    master.sort_values(['AC_No', 'Year'], inplace=True)
    
    # Save
    master.to_csv(OUTPUT_FILE, index=False)
    print(f"DONE! Saved to {OUTPUT_FILE}")
    print(f"Total Rows: {len(master)}")