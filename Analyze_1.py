import pandas as pd

# Load the data from users_activity_log.csv
user_activity_log = pd.read_csv("D:/Projects_Exp/Product_Device_Analysis/users_activity_log.csv")

# 1. In what percent of sessions is search being used?
# Filter for search activities and calculate the percentage of sessions with search
search_sessions = user_activity_log[user_activity_log['event_name'].str.startswith('query_result_')]
total_sessions = user_activity_log['user_id'].nunique()
search_sessions_percentage = (search_sessions['user_id'].nunique() / total_sessions) * 100
print(f"1. In {search_sessions_percentage:.2f}% of sessions, search is being used.")

# 2. Are users able to find what they search for?
# Calculate the click-through rate for search results
search_result_clicks = user_activity_log[user_activity_log['event_name'].str.startswith('query_result_')]
total_clicks = search_result_clicks.shape[0]
total_search_queries = user_activity_log[user_activity_log['event_name'] == 'run_query'].shape[0]
if total_search_queries > 0:
    ctr = (total_clicks / total_search_queries) * 100
else:
    ctr = 0
print(f"2. Users are able to find what they search for with a click-through rate of {ctr:.2f}%.")

# 3. Does the ordering algorithm of search results need tuning?
# Calculate the average position of clicked search results
clicked_positions = search_result_clicks['event_name'].str.extract(r'query_result_(\d+)').astype(int)
average_clicked_position = clicked_positions.mean().iloc[0]  # Extract the scalar value
print(f"3. The average position of clicked search results is {average_clicked_position:.2f}.")

# 4. Are users able to search at all? Is the search button working fine?
# Check if users are using the search feature
search_queries = user_activity_log[user_activity_log['event_name'] == 'run_query']
if search_queries.empty:
    print("4. Users may not be using the search feature.")
else:
    print("4. The search button appears to be working fine.")

# 5. Do users face any errors after running a search query?
# Check for search errors
search_errors = user_activity_log[user_activity_log['event_name'] == 'query_result_0']
if search_errors.empty:
    print("5. Users do not seem to be facing search errors.")
else:
    print("5. Users are facing search errors, and further investigation may be required.")

# 6. Are the autocomplete suggestions helpful for users?
# Calculate the click-through rate for autocomplete suggestions
autocomplete_events = user_activity_log[user_activity_log['event_name'] == 'autocomplete_engine']
total_autocomplete_clicks = autocomplete_events.shape[0]
total_autocomplete_suggestions = len(autocomplete_events['event_name'])
if total_autocomplete_suggestions > 0:
    autocomplete_ctr = (total_autocomplete_clicks / total_autocomplete_suggestions) * 100
else:
    autocomplete_ctr = 0
print(f"6. Autocomplete suggestions have a click-through rate of {autocomplete_ctr:.2f}%.")

# Create a DataFrame to store your findings
findings = pd.DataFrame({
    "Question": ["1. In what percent of sessions is search being used?",
                 "2. Are users able to find what they search for?",
                 "3. Does the ordering algorithm of search results need tuning?",
                 "4. Are users able to search at all? Is the search button working fine?",
                 "5. Do users face any errors after running a search query?",
                 "6. Are the autocomplete suggestions helpful for users?"],
    "Answer": [f"{search_sessions_percentage:.2f}%",
               f"{ctr:.2f}%",
               f"{average_clicked_position:.2f}",
               "Users may not be using the search feature." if search_queries.empty else "The search button appears to be working fine.",
               "Users do not seem to be facing search errors." if search_errors.empty else "Users are facing search errors, and further investigation may be required.",
               f"{autocomplete_ctr:.2f}%"]
})

# Save the findings to a CSV file
findings.to_csv("D:/Projects_Exp/Product_Device_Analysis/findings.csv", index=False)