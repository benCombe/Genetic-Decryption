import sys, os


def ProgressBar(curr, total, size, thread_id, title=None, status=None):
    status_msg = "RUNNING..."

    # Calculate the percentage
    if total == 0:
        raise ZeroDivisionError("Total must be greater than 0")
    percent = (curr / total) * 100

    pb_title = title if title is not None else thread_id

    if status is not None:
        status_msg = status
    elif int(percent) == 100:
        status_msg = "DONE"
    
    # Calculate the number of '#' to display in the progress bar
    num_blocks = int(size * (percent / 100))
    # Create the progress bar string
    progress_bar = '[' + '#' * num_blocks + '-' * (size - num_blocks) + ']'

        # Get the current line for the thread
    #current_line = thread_lines.get(thread_id, None) #TODO SET GENERIC LINE ASSIGNMENT

    #stdout_lock.acquire() #TODO WHEN THREADING

    # Move the cursor to the appropriate line
    #if current_line is not None:
    #    sys.stdout.write(f"\033[{current_line}H")  # Move cursor to thread's line
    #else:
    #   sys.stdout.write(f"\n")  # Move to a new line if no current line
    #   current_line = len(thread_lines) + 2

    # Display the progress bar and percentage
    sys.stdout.write(f"\r{thread_id+1:<2}. {pb_title:<25}\t{progress_bar}\t{round(percent, 1)}%\t{status_msg:<12}")
    sys.stdout.flush()

    #stdout_lock.release()

    # Save the current line for the thread
    #thread_lines[thread_id] = current_line  # Store thread ID