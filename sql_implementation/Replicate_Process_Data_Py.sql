/* FILE: Replicate_Process_Data_Py.sql
   GOAL: Replicate the 'process_2024' function and the PC Name fill logic.
   LOGIC: Replaces Python's .groupby().rank() and .fillna().
*/

-- 1. CLEANING & RANKING (Replicating process_2024 function)
WITH Ranked_Data AS (
    SELECT 
        AC_No,
        AC_Name,
        PC_Name,
        Party,
        Votes_Secured_EVM AS Votes,
        -- Python equivalent: wb.groupby('AC NO')['VOTES'].rank()
        RANK() OVER (PARTITION BY AC_No ORDER BY Votes_Secured_EVM DESC) as Vote_Rank,
        SUM(Votes_Secured_EVM) OVER (PARTITION BY AC_No) as Total_AC_Votes
    FROM Raw_2024_Data
    WHERE State = 'West Bengal'
)

SELECT 
    AC_No,
    AC_Name,
    PC_Name,
    MAX(CASE WHEN Vote_Rank = 1 THEN Party END) as Winner_Party,
    MAX(CASE WHEN Vote_Rank = 1 THEN Votes END) as Winner_Votes,
    MAX(CASE WHEN Vote_Rank = 2 THEN Party END) as Runner_Party,
    MAX(CASE WHEN Vote_Rank = 2 THEN Votes END) as Runner_Votes,
    MAX(Total_AC_Votes) as Total_Votes,
    2024 as Year,
    'Lok Sabha' as Election_Type
FROM Ranked_Data
GROUP BY AC_No, AC_Name, PC_Name;

-- 2. FILLING MISSING PC NAMES (Replicating the .map() fillna logic)
/* In Python, you used a dictionary map from 2024 data to fill older missing PC names.
   In SQL, we use a Self-Join or a Join to a Reference Table with COALESCE.
*/

UPDATE History_Table h
SET PC_Name = m.PC_Name
FROM (
    -- Create the Mapping Dictionary from 2024 Data
    SELECT DISTINCT AC_No, PC_Name 
    FROM Raw_2024_Data 
    WHERE PC_Name IS NOT NULL
) m
WHERE h.AC_No = m.AC_No 
  AND h.PC_Name IS NULL; -- Only fill if currently empty