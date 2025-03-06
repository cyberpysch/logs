import plotly.express as px
import plotly.io as pio
import requests
import re
import pandas as pd

# Constants
LOG_URL = "https://support.netgables.org/apache_combined.log"
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d+) (?P<size>\S+)'
)

def fetch_log_data():
    response = requests.get(LOG_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch log file. Status code: {response.status_code}")
    return response.text.splitlines()

def parse_log_data(log_lines):
    log_entries = [match.groupdict() for line in log_lines if (match := LOG_PATTERN.match(line))]
    df = pd.DataFrame(log_entries)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce")
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    return df

def compute_statistics(df):
    selected_date = df["date"].max()
    daily_logs = df[df["date"] == selected_date]
    print(selected_date)
    ip_counts = daily_logs["ip"].value_counts().reset_index()
    ip_counts.columns = ["IP Address", "Occurrences"]
    
    hourly_counts = daily_logs["hour"].value_counts().sort_index().reset_index()
    hourly_counts.columns = ["Hour", "Visitors"]
    
    top_ips = ip_counts
    top_hours = hourly_counts
    
    return ip_counts, hourly_counts, top_ips, top_hours

def generate_plotly_figure(df, x_col, y_col, title, orientation="v", color_col=None):
    if df.empty:
        return "<p>No data available for visualization.</p>"
    
    fig = px.bar(df, x=x_col, y=y_col, orientation=orientation, title=title, color=color_col)
    return pio.to_html(fig, full_html=False)
