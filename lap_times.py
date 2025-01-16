import os
import sys
from collections import defaultdict
from tabulate import tabulate
import matplotlib.pyplot as plt

# Menu Functionality
def show_main_menu():
    """Show a simple menu with options to choose from."""
    print("\n*** Race Results Menu ***")
    print("1. Show Fastest Lap Times")
    print("2. Show Slowest Lap Times")
    print("3. Show Overall Fastest Driver")
    print("4. Show Overall Slowest Driver")
    print("5. Show Average Lap Time Overall")
    print("6. Show Driver Averages")
    print("7. Show How Many Laps Each Driver Did")
    print("8. Show Driver Info")
    print("9. Exit")
    
    choice = input("\nPick an option (1-9) or type 'exit' to quit: ").strip().lower()

    while choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'exit']:
        print("Hmm, that doesn't seem right. Try again.")
        choice = input("\nPick an option (1-9) or type 'exit' to quit: ").strip().lower()
    
    return choice

# File and Data Reading Functions
def check_file_exists(file_path):
    """Checks if the given file exists and is accessible."""
    if not os.path.exists(file_path):
        print(f"Oops! The file '{file_path}' doesn't exist.")
        return False
    return True

def read_race_data(file_path):
    """Reads the content of the race data file and returns it line by line."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if not lines:
            print("Whoops, looks like the file is empty.")
            return None
        return lines
    except Exception as e:
        print(f"Oops, something went wrong while reading the file: {e}")
        return None

def get_race_name(lines):
    """Extracts the name of the race from the first line."""
    return lines[0].strip()

def get_lap_times_from_file(lines):
    """Extracts the lap times and associates them with each driver."""
    driver_laps = defaultdict(list)
    for line in lines[1:]:
        line = line.strip()
        if len(line) < 6:  # Skip lines that don't have enough data
            continue
        driver_code = line[:3]  # Get the driver's code (e.g., 'VER' for Verstappen)
        try:
            lap_time = float(line[3:])  # Try to convert lap time to a float
            driver_laps[driver_code].append(lap_time)
        except ValueError:
            print(f"Skipping invalid lap time entry: {line}")
    return driver_laps

def load_driver_info(file_path):
    """Load detailed information about drivers (name, team, etc.)."""
    driver_info = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(", ")
                if len(parts) < 4:
                    print(f"Warning: Incomplete details on this driver: {line}")
                    continue
                driver_code = parts[0].split(":")[0]  # Extract the driver code (e.g., 'VER')
                driver_name = parts[0].split(":")[1].strip()  # Extract the driver's name
                team = parts[1]
                nationality = parts[2]
                car_number = parts[3].strip("#")
                driver_info[driver_code] = {
                    'name': driver_name,
                    'team': team,
                    'nationality': nationality,
                    'car_number': car_number
                }
    except Exception as e:
        print(f"Oops, something went wrong with the driver details: {e}")
    return driver_info

# Calculation Functions
def get_fastest_lap_times(driver_laps):
    """Find the fastest lap times for each driver."""
    fastest = []
    for driver, laps in driver_laps.items():
        if not laps:
            continue
        fastest_lap = min(laps)  # Get the fastest lap time for this driver
        fastest.append((driver, fastest_lap))
        
    fastest.sort(reverse=True, key=lambda x: x[1])  # Sort fastest laps in descending order
    return fastest

def get_slowest_lap_times(driver_laps):
    """Find the slowest lap times for each driver."""
    slowest = []
    for driver, laps in driver_laps.items():
        if not laps:
            continue
        slowest_lap = max(laps)  # Get the slowest lap time for this driver
        slowest.append((driver, slowest_lap))
    slowest.sort(key=lambda x: x[1])  # Sort slowest laps in ascending order
    return slowest

def calculate_average_lap_time(driver_laps):
    """Calculate the overall average lap time."""
    all_times = [time for laps in driver_laps.values() for time in laps]
    if all_times:
        avg_time = sum(all_times) / len(all_times)
        print(f"\nOverall Average Time: {avg_time:.3f} seconds\n")
    else:
        print("No lap times available to calculate the average.")

def calculate_driver_averages(driver_laps):
    """Calculate the average lap time for each driver."""
    averages = {}
    for driver, laps in driver_laps.items():
        if laps:
            avg_time = sum(laps) / len(laps)
            averages[driver] = avg_time
    return averages

def show_driver_lap_counts(driver_laps):
    """Show how many laps each driver completed."""
    lap_counts = {driver: len(laps) for driver, laps in driver_laps.items()}
    return lap_counts

# Display Functions
def display_fastest_laps(fastest_laps):
    """Display the fastest lap times in a table and plot them."""
    headers = ["Driver", "Fastest Lap (seconds)"]
    print("\nFastest Laps (in descending order):")
    print(tabulate(fastest_laps, headers=headers, tablefmt="fancy_grid"))
    show_graph = input("\nWould you like to see a graph of the fastest laps? (y/n): ").strip().lower()
    if show_graph == 'y':
        plot_fastest_laps(fastest_laps)

def display_slowest_laps(slowest_laps):
    """Display the slowest lap times in a table and plot them."""
    headers = ["Driver", "Slowest Lap (seconds)"]
    print("\nSlowest Laps (in ascending order):")
    print(tabulate(slowest_laps, headers=headers, tablefmt="fancy_grid"))
    show_graph = input("\nWould you like to see a graph of the slowest laps? (y/n): ").strip().lower()
    if show_graph == 'y':
        plot_slowest_laps(slowest_laps)

def plot_fastest_laps(fastest_laps):
    """Plot the fastest lap times in a vertical bar chart."""
    drivers = [driver for driver, _ in fastest_laps]
    times = [time for _, time in fastest_laps]
    plt.bar(drivers, times, color='lightblue')  # Changed to vertical bar chart
    plt.ylabel('Fastest Lap (seconds)')
    plt.xlabel('Driver')
    plt.title('Fastest Laps by Driver')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.show()

def plot_slowest_laps(slowest_laps):
    """Plot the slowest lap times in a vertical bar chart."""
    drivers = [driver for driver, _ in slowest_laps]
    times = [time for _, time in slowest_laps]
    plt.bar(drivers, times, color='salmon')  # Changed to vertical bar chart
    plt.ylabel('Slowest Lap (seconds)')
    plt.xlabel('Driver')
    plt.title('Slowest Laps by Driver')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.show()

def display_driver_averages(driver_averages):
    """Display average lap times for all drivers."""
    if driver_averages:
        data = [(driver, avg_time) for driver, avg_time in driver_averages.items()]
        data.sort(key=lambda x: x[1], reverse=True)
        print("\nDriver Averages (sorted by average lap time):")
        headers = ["Driver", "Average Lap Time (seconds)"]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No averages available.")

def display_driver_lap_counts(lap_counts):
    """Display how many laps each driver completed."""
    if lap_counts:
        data = [(driver, laps) for driver, laps in lap_counts.items()]
        data.sort(key=lambda x: x[1], reverse=True)
        print("\nLaps Completed by Each Driver:")
        headers = ["Driver", "Laps Completed"]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No lap counts available.")

def display_driver_info(driver_info, driver_laps):
    """Show driver details along with their lap times."""
    data = []
    for driver, laps in driver_laps.items():
        if driver in driver_info:
            details = driver_info[driver]
            fastest_lap = min(laps) if laps else None
            avg_lap_time = sum(laps) / len(laps) if laps else None
            if fastest_lap and avg_lap_time:
                data.append([ 
                    details['name'], details['team'], details['nationality'], details['car_number'],
                    f"{fastest_lap:.3f}", f"{avg_lap_time:.3f}"
                ])
    if data:
        data.sort(key=lambda x: float(x[4]), reverse=True)  
        print("\nDriver Information(sorted in Descending order by fastest lap):")
        headers = ["Driver", "Team", "Nationality", "Car Number", "Fastest Lap (seconds)", "Average Lap Time (seconds)"]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No driver information to display.")

def get_overall_fastest_driver(driver_laps):
    """Find the overall fastest driver and their fastest lap time."""
    fastest_driver = None
    fastest_time = float('inf')
    for driver, laps in driver_laps.items():
        if laps:
            driver_fastest = min(laps)
            if driver_fastest < fastest_time:
                fastest_driver = driver
                fastest_time = driver_fastest
    return fastest_driver, fastest_time

def get_overall_slowest_driver(driver_laps):
    """Find the overall slowest driver and their slowest lap time."""
    slowest_driver = None
    slowest_time = float('-inf')
    for driver, laps in driver_laps.items():
        if laps:
            driver_slowest = max(laps)
            if driver_slowest > slowest_time:
                slowest_driver = driver
                slowest_time = driver_slowest
    return slowest_driver, slowest_time

def main():
    race_file = input("Enter the race data file path: ")
    driver_details_file = input("Enter the driver details file path: ")

    if not check_file_exists(race_file) or not check_file_exists(driver_details_file):
        sys.exit(1)

    driver_info = load_driver_info(driver_details_file)
    lines = read_race_data(race_file)
    if not lines:
        sys.exit(1)

    race_name = get_race_name(lines)
    driver_laps = get_lap_times_from_file(lines)
    print(f"\nRace: {race_name}")

    while True:
        choice = show_main_menu()

        if choice == '1':
            fastest_laps = get_fastest_lap_times(driver_laps)
            display_fastest_laps(fastest_laps)

        elif choice == '2':
            slowest_laps = get_slowest_lap_times(driver_laps)
            display_slowest_laps(slowest_laps)
        
        elif choice == '3':
            fastest_driver, fastest_time = get_overall_fastest_driver(driver_laps)
            if fastest_driver:
                print(f"\nOverall Fastest Driver: {fastest_driver} with a lap time of {fastest_time:.3f} seconds.")
            else:
                print("\nNo lap data available to determine the fastest driver.")

        elif choice == '4':
            slowest_driver, slowest_time = get_overall_slowest_driver(driver_laps)
            if slowest_driver:
                print(f"\nOverall Slowest Driver: {slowest_driver} with a lap time of {slowest_time:.3f} seconds.")
            else:
                print("\nNo lap data available to determine the slowest driver.")
        
        elif choice == '5':
            calculate_average_lap_time(driver_laps)
        
        elif choice == '6':
            driver_averages = calculate_driver_averages(driver_laps)
            display_driver_averages(driver_averages)

        elif choice == '7':
            lap_counts = show_driver_lap_counts(driver_laps)
            display_driver_lap_counts(lap_counts)

        elif choice == '8':
            display_driver_info(driver_info, driver_laps)
        
        elif choice == '9' or choice == 'exit':
            print("Exiting... Goodbye!")
            break

if __name__ == "__main__":
    main()
