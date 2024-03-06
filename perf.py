import os
import subprocess
import time
import matplotlib.pyplot as plt
import datetime
import random


def set_and_print_env_vars():
    env_vars = {
        "STORJ_EXP_UPLINK_DOWNLOAD_PREFETCH_FORCE_READS": "false",
        "STORJ_EXP_UPLINK_DOWNLOAD_PREFETCH_BYTES_REMAINING": "2621440"
    }

    for var in env_vars:
        original_value = os.getenv(var, 'Not set')
        os.environ[var] = env_vars[var]
        updated_value = os.getenv(var)
        print(f"{var}: Before setting = {original_value}, After setting = {updated_value}")


def download_file(file_path, destination, log_dir):
    start_time = time.time()
    log_file_name = f"log{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(0, 100)}.txt"
    log_file_path = os.path.join(log_dir, log_file_name)
    try:
        subprocess.run([
            "uplink", "cp", "-p", "11", f"sj://perf/{file_path}", destination,
            "--upload-log-file", log_file_path
        ], check=True)
        end_time = time.time()
    finally:
        try:
            os.remove(destination)
        except OSError as e:
            print(f"An error occurred when removing the file: {e}")

    return end_time - start_time


def plot_download_times(download_times, plot_dir):
    run_numbers = range(1, len(download_times) + 1)
    plt.plot(run_numbers, download_times, marker='o', linestyle='-', color='b')
    plt.title('Download Time Variation Over Runs')
    plt.xlabel('Run Number')
    plt.ylabel('Download Time (s)')
    plt.xticks(run_numbers)
    plt.grid(True)

    # Save the plot to a file
    plot_file_name = f"download_times_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    plot_file_path = os.path.join(plot_dir, plot_file_name)
    plt.savefig(plot_file_path)
    print(f"Plot saved to {plot_file_path}")
    plt.close()  # Close the plot to free memory


def main():
    set_and_print_env_vars()

    log_dir = "download_logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create a specific directory for plot files
    plot_dir = "plot_graphs"
    os.makedirs(plot_dir, exist_ok=True)

    number_of_downloads = 10
    file_path = "test.AVI"
    destination_path = os.path.join("Downloads", file_path)
    download_times = []

    for _ in range(number_of_downloads):
        download_time = download_file(file_path, destination_path, log_dir)
        download_times.append(download_time)
        print(f"Download took {download_time} seconds.")

    if download_times:
        plot_download_times(download_times, plot_dir)
    else:
        print("No successful downloads to plot.")


if __name__ == "__main__":
    main()
