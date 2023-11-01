import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from users_activity_log.csv and device_details.csv
user_activity_log = pd.read_csv("D:/Projects_Exp/Product_Device_Analysis/users_activity_log_modified.csv")
device_details = pd.read_csv("D:/Projects_Exp/Product_Device_Analysis/device_details.csv")

# Merge the user activity log and device details data using device_id
merged_data = user_activity_log.merge(device_details, on=["device_id","os_version"], how="left")

# 1. Analyze problems found across all users
# Count the occurrences of different event_names to identify issues
user_issues = merged_data.groupby("event_name")["user_id"].count().reset_index()
user_issues = user_issues.rename(columns={"user_id": "issue_count"})

# 2. Analyze problems at the OS level, OS version level, and device level
os_level_issues = merged_data.groupby("os")["event_name"].value_counts().unstack(fill_value=0)
os_version_level_issues = merged_data.groupby(["os", "os_version"])["event_name"].value_counts().unstack(fill_value=0)
device_level_issues = merged_data.groupby("name")["event_name"].value_counts().unstack(fill_value=0)

# Create a summary DataFrame
summary_data = {
    "Event": user_issues["event_name"],
    "Issue Count": user_issues["issue_count"]
}

# Create a DataFrame from the summary_data dictionary
summary_df = pd.DataFrame(summary_data)

# Save the summary DataFrame to a CSV file
summary_df.to_csv("D:/Projects_Exp/Product_Device_Analysis/user_search_issues_summary.csv", index=False)

# Generate stacked bar chart and pie charts for OS level, OS version level, and device level analysis
def generate_stacked_bar_chart(data, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    data.plot(kind="bar", stacked=True, colormap="tab20", ax=plt.gca())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)

def generate_pie_chart(data, title, filename):
    plt.figure(figsize=(6, 6))
    plt.pie(data, labels=data.index, autopct="%1.1f%%", startangle=140)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)

# Generate and save visualizations
generate_stacked_bar_chart(os_level_issues, "OS Level Issues", "OS", "Issue Count", "D:/Projects_Exp/Product_Device_Analysis/os_level_issues.png")
generate_pie_chart(os_level_issues.sum(), "OS Analysis", "D:/Projects_Exp/Product_Device_Analysis/os_pie_chart.png")

generate_stacked_bar_chart(os_version_level_issues, "OS Version Level Issues", "OS Version", "Issue Count", "D:/Projects_Exp/Product_Device_Analysis/os_version_level_issues.png")
generate_pie_chart(os_version_level_issues.sum(), "OS Version Analysis", "D:/Projects_Exp/Product_Device_Analysis/os_version_pie_chart.png")

generate_stacked_bar_chart(device_level_issues, "Device Level Issues", "Device", "Issue Count", "D:/Projects_Exp/Product_Device_Analysis/device_level_issues.png")
generate_pie_chart(device_level_issues.sum(), "Device Analysis", "D:/Projects_Exp/Product_Device_Analysis/device_pie_chart.png")

# Show the visualizations
plt.show()