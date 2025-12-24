/* FILE: Replicate_Candidates_Py.sql
   GOAL: Replicate the Python 'Wide-to-Long' transformation.
   LOGIC: In Python, you looped through rows and appended 'Winner' and 'Runner' separately.
          In SQL, we use UNION ALL to stack these results vertically.
*/

-- Step 1: Create the "Winner" Rows
SELECT 
    Year, 
    AC_Name, 
    PC_Name, 
    Winner_Party AS Party, 
    Winner_Votes AS Votes, 
    'Winner' AS Position
FROM Final_Master_Dataset

UNION ALL

-- Step 2: Create the "Runner-Up" Rows
SELECT 
    Year, 
    AC_Name, 
    PC_Name, 
    Runner_Party AS Party, 
    Runner_Votes AS Votes, 
    'Runner-Up' AS Position
FROM Final_Master_Dataset

UNION ALL

-- Step 3: Create the "Others" Rows
-- Logic: Total Votes - (Winner + Runner)
SELECT 
    Year, 
    AC_Name, 
    PC_Name, 
    'Others' AS Party, 
    (Total_Votes - (Winner_Votes + Runner_Votes)) AS Votes, 
    'Others' AS Position
FROM Final_Master_Dataset
WHERE (Total_Votes - (Winner_Votes + Runner_Votes)) > 0; -- Only if others exist