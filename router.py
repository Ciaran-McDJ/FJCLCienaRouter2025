import subprocess
import sys
import time
import select

from simulation_win import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def process_cli_input(file_path, history, t):
    # Process CLI input here
     # replacing input with select to allow non-blocking CLI input
    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip()
        if user_input:
            command, *args = user_input.split()
            if command == "set":
                if len(args) !=2:
                    print("Invalid Input - Please use exactly 2 arguments")
                else:
                    try:
                        index = int(args[0]) - 1
                        value = int(args[1])
                        if index < 0 or index >3 :
                            print(f"Invalid Input - Index (first argument): {index + 1}, is out of bounds. Try a value between 1 and 4.")
                        else:
                            mutate_database(file_path, index, value)
                            history.append(f"{t} set {index} {value}")
                    except Exception as e:
                        print(f"Invalid Input - Error: {str(e)}")
            else:
                print(f"Unknown command: {command}")

def main():
    history = []
    t = 0


    while t < 60:
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1

        # Write Your Code Here Start
        if (t%10 == 0):
            print(t)
            print(read_hardware_state(file_path))
            state_values, control_values, signal_values = read_hardware_state(file_path)
            state_0 = state_values[0]
            state_1 = state_values[1]
            state_values[1] = state_0
            state_values[0] = state_1
            write_hardware_state(file_path,state_values, control_values, signal_values)
            
        process_cli_input(file_path, history, t)

        # CASE 2
        index = signal_values[0] - 1
        if (index <= 3 and index >= 0):
            value = signal_values[1]
            control_values[index] = value
        
        mutate_hardware(file_path, index, value)

        # Write Your Code Here End

        time.sleep(0.1)  # Wait for 1 second before polling again
    print(history)

if __name__ == '__main__':
    main()