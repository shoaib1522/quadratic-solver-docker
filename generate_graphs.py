import matplotlib.pyplot as plt
import pandas as pd
import re
import os

def create_cpu_graph(csv_file, output_png):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Convert timestamp to datetime for better plotting
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['cpu_percent'], marker='o', linestyle='-', color='b')
    plt.title('CPU Utilization During Load Test')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()
    print(f"CPU graph saved to {output_png}")

def create_response_time_graph(httperf_file, output_png):
    # Read the httperf output file
    with open(httperf_file, 'r') as f:
        content = f.read()
    
    # Extract the average response time from the line like:
    # "Reply time [ms]: response 21.4 transfer 0.0"
    match = re.search(r'Reply time \[ms\]: response ([\d.]+)', content)
    if match:
        avg_response_time = float(match.group(1))
    else:
        # Fallback: look for Connection time [ms]: avg
        match = re.search(r'Connection time \[ms\]: avg ([\d.]+)', content)
        if match:
            avg_response_time = float(match.group(1))
        else:
            # If still not found, use a default or raise an error
            print("Warning: Could not extract response time from httperf output. Using 0.")
            avg_response_time = 0.0
    
    # Create a bar graph
    plt.figure(figsize=(8, 6))
    plt.bar(['Average Response Time'], [avg_response_time], color='g')
    plt.title('Average Response Time per Request')
    plt.ylabel('Time (ms)')
    plt.ylim(0, avg_response_time * 1.2 if avg_response_time > 0 else 10)  # Add some headroom
    # Add value on top of the bar
    plt.text(0, avg_response_time, f'{avg_response_time:.1f} ms', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()
    print(f"Response time graph saved to {output_png}")

if __name__ == "__main__":
    # Define file paths
    cpu_csv = "cpu_usage.csv"
    httperf_txt = "httperf_output.txt"
    graphs_dir = "graphs"
    
    # Ensure graphs directory exists
    os.makedirs(graphs_dir, exist_ok=True)
    
    # Create CPU graph
    cpu_graph_path = os.path.join(graphs_dir, "cpu_utilization_graph.png")
    create_cpu_graph(cpu_csv, cpu_graph_path)
    
    # Create response time graph
    response_time_graph_path = os.path.join(graphs_dir, "response_time_graph.png")
    create_response_time_graph(httperf_txt, response_time_graph_path)
    
    print("Graph generation complete.")