from flask import Flask, render_template
from dashboard import *

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch and parse log data
    log_lines = fetch_log_data()
    df = parse_log_data(log_lines)

    # Compute statistics
    ip_counts, hourly_counts, top_ips, top_hours = compute_statistics(df)

    # Generate histograms using Plotly
    ip_histogram = generate_plotly_figure(ip_counts[:15], "Occurrences", "IP Address", "Top 10 IP Addresses", "h", "Occurrences")
    hourly_histogram = generate_plotly_figure(hourly_counts, "Hour", "Visitors", "Hourly Traffic", "v", "Visitors")
    top_ips_histogram = generate_plotly_figure(top_ips[:15], "Occurrences", "IP Address", "IPs Contributing 85% of Traffic", "h", "Occurrences")
    top_hours_histogram = generate_plotly_figure(top_hours, "Hour", "Visitors", "Hours Contributing 70% of Traffic", "v", "Visitors")

    return render_template("dashboard.html",
                           ip_histogram=ip_histogram,
                           hourly_histogram=hourly_histogram,
                           top_ips_histogram=top_ips_histogram,
                           top_hours_histogram=top_hours_histogram)

if __name__ == '__main__':
    app.run(debug=True)
