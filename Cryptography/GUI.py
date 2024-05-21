import string
import random
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from Genkey import XORCipher, Evaluator, Genome


def GeneticAlgorithm(encrypted_text, numGens, popsize, crossover_rate, mutation_rate, kval, progress_bar, progress_label, result_out, out_file=None):
    currPop = []
    bestKey = None
    eval = Evaluator(encrypted_text)
    update_label(progress_label, f"Initializing Population")
    root.update_idletasks()
        #initial Pop and sort
    for i in range(popsize):
        #ProgressBar(i, popsize-1, 50)
        g = Genome() #random key
        currPop.append(g)
        #get scores for currPop
        for g in currPop:
            g.getFitness(eval)
        # Update progress bar
        progress_bar['value'] = (i + 1) / popsize * 100
        root.update_idletasks()  # Refresh the GUI

    
    #sort the current population based on score
    currPop = sorted(currPop, key=lambda x: x.score)
    if out_file is not None:
        out_file.write(f"Gen 0  : {currPop[0].key}\t{currPop[0].score}\n")

    update_label(progress_label, f"Searching Keys")
    progress_bar['value'] = 0
    for i in range(numGens):
        selectedParents = []
        nextPop = []
        #ProgressBar(i, numGens-1, 50)

        #check for nones
        #for g in range(len(currPop)):
        #    if currPop[g] == None:
        #        print(f"currPop[{g}] is Null")
                #break 

            #move top 3 into selectedParents
        for j in range(2):
            selectedParents.append(currPop[j])

            #fill rest of selectedParents using tournament selection
        while len(selectedParents) < popsize:
            kGroup = random.sample(currPop, kval) 
            for k in kGroup:
                if k is None:
                    kGroup.remove(k)
            selectedParents.append(min(kGroup, key=lambda x: x.score))

        while len(nextPop) < popsize:
            parents = random.sample(selectedParents, 2)
                
            if random.random() <= crossover_rate:
                children = parents[0].crossover(parents[1])
            else:
                children = parents
                
                #apply mutation
            for j in range(len(children)):
                if random.random() <= mutation_rate:
                    if i >= numGens/2:
                        children[j].mutate(2)
                    else:
                        children[j].mutate()
                    
            nextPop.append(children[0])
            nextPop.append(children[1])

            #move next population to current
        currPop = nextPop

            #get scores for currPop
        for j in range(popsize):
            currPop[j].getFitness(eval)
            
            #sort the current population based on score
        currPop = sorted(currPop, key=lambda x: x.score)

        # Update progress bar
        progress_bar['value'] = (i + 1) / numGens * 100
        root.update_idletasks()  # Refresh the GUI

        if out_file is not None:
            out_file.write(f"Gen {i+1:<3}: {currPop[0].key}\t{currPop[0].score}\n")
        bestKey = currPop[0].key
        update_label(result_out, bestKey)
        ciph = XORCipher(bestKey)
        text = ciph.decrypt(encrypted_text=encrypted_text)
        update_decrypted_text(text)
        root.update_idletasks()
        
                    
    """ print(f"\nBEST KEY: {bestKey}\tSCORE: {currPop[0].score}\n")
    ciph = XORCipher(bestKey)
    text = ciph.decrypt(encrypted_text=encrypted_text)
    print(text) """


def update_label(label, text):
    label.config(text="")
    label.config(text=text)

def update_decrypted_text(text):
    decrypted_text_area.delete(1.0, tk.END)  # Clear the text area
    decrypted_text_area.insert(tk.END, text)  # Insert the new text

def start():
    passkey = entries[0].get()
    num_generations = int(entries[1].get())
    population_size = int(entries[2].get())
    crossover_rate = float(entries[3].get())
    mutation_rate = float(entries[4].get())
    k_value_selected = int(k_value.get())
    selected_file = file_entry.get()
    
    enc_cipher = XORCipher(passkey)
    with open(selected_file, "rb") as file:
        text = file.read()
    enc_text = enc_cipher.encrypt(text)
    update_decrypted_text(enc_text)
    progress_bar['value'] = 0
    GeneticAlgorithm(enc_text, numGens=num_generations, popsize=population_size, 
                     crossover_rate=crossover_rate, mutation_rate=mutation_rate, 
                     kval=k_value_selected, progress_bar=progress_bar, progress_label=progress_label,
                     result_out=best_key_output)
    progress_bar['value'] = 0


# Function to open file dialog
def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)
    with open(file_entry.get(), "r") as file:
        text = file.read()
        update_decrypted_text(text)



# Create the main window
root = tk.Tk()
root.title("Genetic Algorithm")
root.geometry("1100x500")


main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = tk.Frame(main_frame)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
output_frame = tk.Frame(main_frame)
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


# Define labels and entries
fields = [
    ("My Passkey", "ThisIsMyKey"),
    ("Number of Generations", 150),
    ("Population Size", 500),
    ("Crossover Rate", 0.85),
    ("Mutation Rate", 0.35)
]

entries = []

# Create and place the labels and text input fields
for i, (label, default_val) in enumerate(fields):
    tk.Label(input_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
    entry = tk.Entry(input_frame, width=40)
    entry.insert(0, default_val)
    entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
    entries.append(entry)

# Create and place the dropdown select for K Value
tk.Label(input_frame, text="K Value").grid(row=len(fields), column=0, padx=10, pady=5, sticky='e')
k_value = tk.StringVar()
k_dropdown = ttk.Combobox(input_frame, textvariable=k_value)
k_dropdown['values'] = (3, 4, 5)
k_dropdown.set(4)
k_dropdown.grid(row=len(fields), column=1, padx=10, pady=5, sticky='w')

#File select
tk.Label(input_frame, text="Select File").grid(row=len(fields) + 1, column=0, padx=10, pady=5, sticky='e')
file_entry = tk.Entry(input_frame, width=40)
file_entry.grid(row=len(fields) + 1, column=1, padx=10, pady=5, sticky='w')
browse_button = tk.Button(input_frame, text="Browse", command=browse_file)
browse_button.grid(row=len(fields) + 1, column=2, padx=10, pady=5, sticky='w')

# Create and place the Start button
start_button = tk.Button(input_frame, text="Start", width=25, padx=4, command=start)
start_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

progress_label = tk.Label(output_frame, text="")
progress_label.grid(row=0, column=0, columnspan=1, pady=2)

# Create and place the progress bar
progress_bar = ttk.Progressbar(output_frame, orient='horizontal', mode='determinate', length=400)
progress_bar.grid(row=0, column=1, columnspan=2, pady=5)

decrypted_text_area = tk.Text(output_frame, wrap=tk.WORD, width=40, height=20)
decrypted_text_area.grid(row=1, column=0, columnspan=3,padx=5, pady=5, sticky="nsew")

best_key_label = ttk.Label(output_frame, text="Best Key:")
best_key_label.grid(row=2, column=0, columnspan=1, pady=5)
best_key_output = ttk.Label(output_frame, text="")
best_key_output.grid(row=2, column=1, columnspan=2, pady=5)

# Run the application
root.mainloop()
