# Importing the module needed
from time import sleep
import numpy as np
import simpleaudio as sa
from tkinter import *
from tkinter import ttk
import random
from tkinter import filedialog


#----------Function Part----------#

# initialisation of the variable
f = "partitions.txt"
f_note = 'notes.txt'
f_frequency = "frequencies.txt"
figures = ["c", "n", "b", "r"]
d0 = 125
silence_duration = {"Z": -1}
value = 0
color = ["#fc5c65", "#fd9644", "#fed330", "#26de81", "#2bcbba", "#eb3b5a", "#fa8231", "#f7b731", "#20bf6b", "#0fb9b1",
         "#45aaf2", "#4b7bec", "#a55eea", "#778ca3", "#2d98da", "#3867d6", "#8854d0", "#a5b1c2", "#4b6584"]


# give a random color for the button in the graphic interface
def random_color():
    nbr = random.randint(0, len(color) - 1)  #have a random number 
    return color[nbr]                        #return the random color


# creat the list "notes" who have all the note
def create_list_note():
    notes = []
    file = open(f_note, "r")
    line = file.readline()
    while line != "":          #read all the lines
        notes.append(line[:-1])
        line = file.readline() #read the file line
    print(notes)
    return notes                #return a list of all the notes


# creat the list "frequencies" who have all the frequency 
def create_frequencies_list():
    frequencies = []
    file = open(f_frequency, "r")
    line = file.readline()
    while line != "":
        frequencies.append(line[:-1])
        line = file.readline()
    print(frequencies)
    return frequencies        #return a list of all the frequencies


# Find the music chosen by the users 
def find_line_file(f, choice): #f is the name of the file , choice is the "#" + number choose by the user
    file = open(f, "r")
    line = file.readline()
    num = 0                    #initialing variable
    music_number = ""        
    if type(choice) == str:    #if only one music is choose 
        while line != "":
            if num < 18:
                music_number = line[:2]  #recovered only the number of the music
                print(music_number)
                if music_number == choice:
                    print(line)
                    return num
                line = file.readline()
            elif num > 18:
                music_number = line[:3]  #recovered only the number of the music
                print(music_number)
                if music_number == choice:
                    print(line)
                    return num - 1
                line = file.readline()
            num = num + 1
        return num  #return the number of the lign who are the partition choose

    elif type(choice) == list:      #if serval music are choosed
        list_num = []
        print(choice)
        for hashtag in choice:
            print(hashtag)
            while line != "":
                if num < 18:
                    music_number = line[:2]  #recovered only the number of the music
                    print(music_number)
                    if music_number == hashtag:
                        print(line)
                        list_num.append(num)
                        break
                    line = file.readline()
                elif num > 18:
                    music_number = line[:3]  #recovered only the number of the music
                    print(music_number)
                    if music_number == hashtag:
                        print(line)
                        list_num.append(num - 1)
                        break
                    line = file.readline()
                num = num + 1
        print(list_num)
        return list_num    #return a list of number of the lign who are the name choose


# create a list with all the music present in the file
def get_music_name():
    music_list = []
    file = open(f, "r",encoding="UTF-8") #open the file in reading mode in UTF-8 for have (accent)
    line = file.readline()
    while line != "":
        if line[:1] == "#": 
            line = line[:-1]
            music_list.append(line)
        line = file.readline()
    print(music_list)
    return music_list                # return the list of all the music 


# Find the partition the user choose with the number of the line name
def read_line_file(f, num):
    if type(num) == str or type(num) == int:  #check if the number (only one music choose) is alone or not
        file = open(f, "r")
        lines = file.readlines()
        return lines[num + 1]           #return the line after the music name
    elif type(num) == list:
        list_line = []
        for number in num:
            file = open(f, "r")
            lines = file.readlines()
            list_line.append(lines[number + 1])
        return list_line                #return the lines (in list) after the music name


# create a dictionary with the frequencies
def calc_frequency(notes, frequencies):
    calc = {}
    for i in range(len(notes)):
        calc[notes[i]] = frequencies[i]
    return calc


# create a dictionary with the duration
def calc_duration(figures, d0):
    calc = {}
    d1 = 2 * d0
    d2 = 2 * d1
    d3 = 2 * d2
    durations = [d0, d1, d2, d3]
    for n in range(len(figures)):
        calc[figures[n]] = durations[n]
    return calc


# Find the duration and the frequencies of each note
def create_music_list(chosen_partition_list):
    note_partition = []
    temps_note = ""                             #initialise variable
    chosen_partition = ""
    for partition in chosen_partition_list:
        chosen_partition = chosen_partition + partition   #creat a variable with the partition
    print(chosen_partition)

    for d in chosen_partition:
        temps_note = temps_note + d
        if d == " " or d == "\n":
            note_partition.append(temps_note)
            temps_note = ""                   #transform the variable in a list 

    list_partition = []                       
    for k in note_partition:
        note = [k[:-2], k[-2]]              #separate the duration and the note beaucause the partition is : NOTEduration ...
        list_partition.append(note)     

    print(list_partition)
    return list_partition, note             #return a 2D list of the notes separate and duration too


# This function is used to convert the partition the user chose to something the sound function can understand
def read_sheet(list_partition, duration, frequency, note):  #a partition , dictionnary duration and frequency and note
    freq_seq = []
    duration_seq = []
    for q in range(len(list_partition)):    
        for x in range(len(note)):
            carac = list_partition[q][x]     #recive the string in the list of the principal list (path 2D list)
            if carac == "Z":
                freq_seq.append(-1)
            if carac == "p":
                before = float(duration_seq[-1])
                duration_seq[-1] = before + before / 2
            for keys, values in frequency.items():
                if keys == carac:                  #find the frequency equal to the note in the dictionnary
                    freq_seq.append(values)
            for key, value in duration.items():
                if key == carac and list_partition[q][x - 1] == "Z":
                    duration_seq.append(-1 * value)
                elif key == carac:                   #find the duration equal to the note in the dictionnary
                    duration_seq.append(value)

    return freq_seq, duration_seq               #return a list of freq and a list of duration for play the music


# converts a list into a list of floats
def floatl(list):
    for s in range(len(list)):
        list[s] = float(list[s])
    return list


# create a list of only note with a partition
def do_list_of_note(partition):
    list_notes_partition = []
    for q in range(len(partition)):
        for x in range(len(partition[q])):
            carac = partition[q][x]
            for i in notes:
                if carac == i:
                    list_notes_partition.append(carac)
    return list_notes_partition                 #return a list of note


#the start of the markovs chains
def markovs_chain_initialisation(f, list, frame_menu_computer_create,entrychamp): 
    # update the list
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    reslist = []
    list_selection = []
    size = entrychamp.get()
    #gestion of exception if the user don't enter number
    try :
        size = int(size)
    except:
        success = Label(frame_menu_computer_create, text=" This is not a number ", font=("Kikuri", 40),bg="#FFFFFF", fg="#1BFF00")
        success.pack(expand=YES)
        return False

    #recive the user choose
    selection = list.curselection()
    for i in selection:
        entry = list.get(i)
        reslist.append(entry)
    for val in reslist:
        list_selection.append(val)
    choose = ""
    letter = ""
    choose_list = []

    #creat a list of music choose by user
    for name_mus in list_selection:
        for letter in name_mus:
            if letter == " ":
                break
            else:
                choose = choose + letter
        choose_list.append(choose)
        choose = ""
    matrix = []
    dic = {}
    #creat the matrice
    for i in notes:
        matrix.append(i)
        for x in notes:
            dic[x] = 0
        matrix.append(dic)
        dic = {}

    return choose_list, matrix, size    #return the choose music list , size choose of the user and the matrix 


# the first markov function without occurrence
def markovs_chain_1(f, list, frame_menu_computer_create,entrychamp): #file name, frame of the menu markovs , the choose of user
    # update the list
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    choose_list, matrix, size = markovs_chain_initialisation(f, list, frame_menu_computer_create,entrychamp)
    print(choose_list)
    #recive variable
    num_list = find_line_file(f, choose_list)
    chosen_partition_list = read_line_file(f, num_list)
    list_partition, note = create_music_list(chosen_partition_list)
    list_notes_partition = do_list_of_note(list_partition)
    #fill the matrix
    for a in range(len(list_notes_partition)):
        note = list_notes_partition[a]
        for keys in range(len(matrix)):
            if matrix[keys] == note:
                for key, value in (matrix[keys + 1]).items():
                    if key == list_notes_partition[a - 1]:
                        print(value)
                        (matrix[keys + 1])[key] = value + 1

    new_partition = ["SOL"]  #Choose the first note 
    success = []

    for i in range(size):
        for a in range(len(new_partition)):
            note = new_partition[a]
            for keys in range(len(matrix)):    #parcours the matrix
                if matrix[keys] == note:
                    for key, value in (matrix[keys + 1]).items():
                        if value > 0:
                            success.append(key)
        nbr = random.randint(0, (len(success) - 1))  #Choose a random note among these successors
        new_partition.append(success[nbr])
        success = []

    markovs_chain_add_partition(new_partition, frame_menu_computer_create, list)

# the second markov function with occurrence
def markovs_chain_2(f, list, frame_menu_computer_create,entrychamp):  #file name, frame of the menu markovs , the choose of user
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    choose_list, matrix,size = markovs_chain_initialisation(f, list, frame_menu_computer_create,entrychamp)
    num_list = find_line_file(f, choose_list)
    chosen_partition_list = read_line_file(f, num_list)
    list_partition, note = create_music_list(chosen_partition_list)
    total = {}
    new_partition = []
    for note in notes:
        total[note] = 0
    list_notes_partition = do_list_of_note(list_partition)
    for a in range(len(list_notes_partition)):
        note = list_notes_partition[a]
        for key in total:
            if key == note:
                i = +1
                total[key] = total[key] + i
            i = 0

    max = 0
    for key, value in (total).items():
        if value > max:
            max = value

    for key, value in (total).items():
        if (total[key]) == max:
            new_partition.append(key)       #Choose as the first note the one with the highest number of occurrences
            print(new_partition)

    #fill the matrix
    for a in range(len(list_notes_partition)):
        note = list_notes_partition[a]
        print(note)
        for keys in range(len(matrix)):
            if matrix[keys] == note:
                for key, value in (matrix[keys + 1]).items():
                    if key == list_notes_partition[a - 1]:
                        (matrix[keys + 1])[key] = value + 1

    success = []
    for i in range(size):
        note = new_partition[-1]
        for keys in range(len(matrix)):                 #parcours the matrix
            if matrix[keys] == note:
                for key, value in (matrix[keys + 1]).items():
                    if value > 0:
                        for v in range(value):
                            success.append(key)
        nbr = random.randint(0, (len(success) - 1))      #Choose a random note among these successors
        new_partition.append(success[nbr])
        success = []

    print(new_partition)
    markovs_chain_add_partition(new_partition, frame_menu_computer_create, list)


#creat a partition readable bry the program (with duration and silence)
def markovs_chain_add_partition(new_partition, frame_menu_computer_create, list):  #the note choose , frame of the menu markovs
    figures = ["c", "n", "b", "r"]
    n_partition = ""
    for note in new_partition:
        nbr = random.randint(0, (len(figures) - 1))
        duration = figures[nbr]
        n_partition = n_partition + note + duration + " " + "Zc" + " "  #generate the partition 

    print(n_partition)
    enter_music("markov chain", n_partition, len(music_list), f)
    success = Label(frame_menu_computer_create, text=" your music are successfully added ", font=("Kikuri", 40),bg="#FFFFFF", fg="#1BFF00")
    success.pack(expand=YES)
    refresh_list_music(list)    
    frame_menu_computer_create.pack()


def refresh_list_music(list):
    list.delete(0, END)
    # update the list
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    for title in range(nbr_partitions):
        list.insert(title, music_list[title])
    list.pack()

def refresh_list_note(list):
    list.delete(0, END)
    # update the list
    notes = create_list_note()
    for nbr_note in range(len(notes)):
        list.insert(nbr_note, notes[nbr_note])
    list.pack()


# find longest title size to have a sufficient block size
def longest_title(music_list):
    title_size_max = 0
    nbr_letter = 0
    for title in music_list:
        for letter in title:
            nbr_letter = nbr_letter + 1
        if nbr_letter > title_size_max:
            title_size_max = nbr_letter
        nbr_letter = 0
    return title_size_max    #return the size of the bigest music title


def enter_music(name_music,content_music,music_list,f):
    music_list = get_music_name()
    nbr_partitions=str(len(music_list) + 1) #as we are adding a music, we add 1 to the current number of musics
    with open(f, 'r') as file: #we open the files in "read" mode
        data = file.readlines() #here i'm using a list because it's easier to add data to it
    l = len(data)
    x = 0
    while x < l: #here i had to use a while as when the program deletes a line in data, the for wouldn't be updated and then the if would give an out of range error
        if data[x] == "\n":
            data.remove("\n") #this is done to try to remove the unecessary line jumps
            l = l - 1 #and as we remove a line we need to substract 1 to the while
        x = x + 1
    data.append("\n" + "#" + nbr_partitions + " " + name_music + "\n")
    data.append(content_music)
    l = len(data)
    x = 0
    while x < l: #the main purpose of this while is to remove the spaces at the end of the partitions which prevent them from being played
        temp_data=data[x]
        if temp_data[-1] == " ":
            temp_data=temp_data[:-1]
            del data[x]
            data.append(temp_data)
            l = l - 1 #same problem as before as i delete a line i need to remove 1 to the while
        x = x + 1
    file = open(f, "w") #and here we add the new partition to the database
    file.writelines(data)
    file.close()

def add_partition_inverse_transposed(partition, list_changed):
    i = 0
    new_partition = []
    for q in range(len(partition)):
        for x in range(len(partition[q])):
            carac = partition[q][x]
            for note_nbr in range (len(notes)):
                note = notes[note_nbr]
                if carac == note:
                    new_partition.append(list_changed[i])
                    i = i+1
                    add = True
            if add == False :
                new_partition.append(carac)              #creat the list with the silence and duration from the starting one and the changed note
            add = False

    print(new_partition)

    new_list = []
    a = 0
    for i in range(len(new_partition)):
        for j in range(len(notes)):
            if new_partition[i] == notes[j]:
                temp = new_partition[i] + new_partition[i+1]
                new_list.append(temp)
        if new_partition[i] == "p":
            temp = new_partition[i]
            new_list.append(temp)
        if new_partition[i] == "Z":
            temp = new_partition[i] + new_partition[i+1]
            new_list.append(temp)

    n_partition = ""
    for element in new_list:
        n_partition = n_partition + element + " "
    return n_partition              #return a string with a partition playable by the program


# use transposition
def transposition(f, list, frame_menu_transposition_inversion,entrychamp): #file name, listbox, frame of menu with transposition, user choose
    k =entrychamp.get()
    #gestion of the error if the user don't enter number
    try :
        k = int(k)
    except:
        echec = Label(frame_menu_transposition_inversion, text=" it's not a number ", font=("Kikuri", 20))
        echec.pack(expand=YES)
        return False
    #update list
    list_placement_note = []
    list_transposed = []
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    #recive user choose
    line = list.curselection()[0]
    item = list.get(line)
    selected_item = item
    print(selected_item)
    choose = ""
    letter = ""
    for letter in selected_item:
        print(letter)
        if letter == " ":
            break
        else:
            choose = choose + letter

    num = find_line_file(f, choose)
    chosen_partition = read_line_file(f, num)
    list_partition, note = create_music_list(chosen_partition)
    partition = list_partition

    for q in range(len(partition)):
        for x in range(len(partition[q])):
            carac = partition[q][x]
            for note_nbr in range(len(notes)):
                note = notes[note_nbr]
                if carac == note:
                    list_placement_note.append(note_nbr) #find the placement of the note in the musical scale

    for nbr in list_placement_note:
        if (nbr + k) <= len(notes):
            note = nbr + k
            list_transposed.append(note)
        else:
            note = (nbr + k) % len(notes)               #if the note + decalage > L we use the modulo to know how many the number depasse
            list_transposed.append(note)
    trans_partition = []
    for nbr in list_transposed:
        trans_partition.append(notes[nbr - 1])  #add the note transposed in a list

    n_partition = add_partition_inverse_transposed(partition, trans_partition)

    enter_music("transposition", n_partition, nbr_partitions, f)
    success = Label(frame_menu_transposition_inversion, text=" your music are successfully added ", font=("Kikuri", 20),bg="#FFFFFF", fg="#1BFF00")
    success.pack(expand=YES)
    refresh_list_music(list)
    frame_menu_transposition_inversion.pack()


# use inversion
def inversion(f, list, frame_menu_transposition_inversion): #file name, listbox, frame of menu with inversion, user choose
    list_placement_note = []
    list_reversed = []
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    line = list.curselection()[0]
    item = list.get(line)
    selected_item = item
    print(selected_item)
    choose = ""
    letter = ""
    for letter in selected_item:
        print(letter)
        if letter == " ":
            break
        else:
            choose = choose + letter

    print(choose)
    num = find_line_file(f, choose)
    chosen_partition = read_line_file(f, num)
    list_partition, note = create_music_list(chosen_partition)
    partition = list_partition

    for q in range(len(partition)):
        for x in range(len(partition[q])):
            carac = partition[q][x]
            for note_nbr in range(len(notes)):
                note = notes[note_nbr]
                if carac == note:
                    list_placement_note.append(note_nbr)    #find the placement of the note in the musical scale

    for nbr in list_placement_note:
        list_reversed.append(notes[-nbr])                   #inverse the notes and save it in list

    n_partition = add_partition_inverse_transposed(partition, list_reversed)
    enter_music("inversion", n_partition, nbr_partitions, f)
    success = Label(frame_menu_transposition_inversion, text=" your music are successfully added ", font=("Kikuri", 40),bg="#FFFFFF", fg="#1BFF00")
    success.pack(expand=YES)
    refresh_list_music(list)
    frame_menu_transposition_inversion.pack()



# this function is used when a user is trying to load a new partition form a txt file
def read_new_file(new_file_name):
    with open(new_file_name, 'r') as file:
        new_data = file.readlines() #here we store the data of the new file into a list
    l = len(new_data)
    x = 0
    while x < l: #here i had to use a while as when the program deletes a line in data, the for wouldn't be updated and then the if would give an out of range error
        if new_data[x] == "\n":
            new_data.remove("\n") #this is done to try to remove the unecessary line jumps
            l = l - 1 #and as we remove a line we need to substract 1 to the while
        x = x + 1
    y = 0
    o = 1
    while y < len(new_data): #here the while is necessary in case someone wants to load serval partitions in one file
        name_music = new_data[y]
        name_music = name_music.replace('\n','') #we replace any line breaks so that the enter_music function can work properly
        y = y + 2 #this is needed as in a partition file one line is the name and the other is the actual partition
        content_music = new_data[o]
        content_music = content_music.replace('\n','') #same here we replace any potential line breaks
        o = o + 2
        enter_music(name_music, content_music, nbr_partitions, f) #and we utilize the enter_music function to add the new data to the main database


# browse a file for the user to add to the database
def browseFiles(frame_menu_browse_partition):
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File",filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    # Change label contents
    read_new_file(filename)
    label_file_explorer = Label(frame_menu_browse_partition, text="File Opened: " + filename)
    label_file_explorer.pack(expand=YES)
    frame_menu_browse_partition(expand=YES)


# this function deletes a music from the database
def delete_partition(f, choice):
    with open(f, 'r') as file:
        data = file.readlines()
    file = open(f, "r")
    line = file.readline()
    num = 0
    while line != "":
        if num < 18: #we try to find the music to delete
            music_number = line[:2]
            if music_number == choice:
                del data[num - 1] #we need to delete two lines as there is the name of the partition and the actual partition
                del data[num - 1]
            line = file.readline()
        elif num > 18: #over #9, the number of caracter used to name the music goes to 3
            music_number = line[:3]
            if music_number == choice:
                del data[num - 1] #we need to delete two lines as there is the name of the partition and the actual partition
                del data[num - 1]
            line = file.readline()
        num = num + 1
    with open(f, 'r') as file:
        file = open(f, "w") #and we write the new data to the database
    file.writelines(data)


# deletes a note from the notes.txt file
def delete_note(f, note_name):
    with open(f, 'r') as file:
        data = file.readlines()
    file = open(f, "r")
    line = file.readline()
    num = 0
    while line != "":
        if line == note_name:
            del data[num]
        line = file.readline()
        num = num + 1
    with open(f, 'r') as file:
        file = open(f, "w")
    file.writelines(data)


# deletes a frequencies from the frequencies.txt file
def delete_freq(f, chosen_freq):
    with open(f, 'r') as file:
        data = file.readlines()
    file = open(f, "r")
    line = file.readline()
    num = 0
    while line != "":
        if line == chosen_freq:
            del data[num]
        line = file.readline()
        num = num + 1
    with open(f, 'r') as file:
        file = open(f, "w")
    file.writelines(data)


# delete notes and frequencies and this is called into another function to tidy up the code
def delete_noteandfreq(f_frequency, f_note, chosen_freq, note_name, frame_menu_delete_note):
    delete_note(f_note, note_name)
    delete_freq(f_frequency, chosen_freq)
    success = Label(frame_menu_delete_note, text=" the note has been successfully removed ", font=("Kikuri", 40),
                    bg="#FFFFFF", fg="#1BFF00")
    success.pack(expand=YES)
    frame_menu_delete_note.pack()


# adds a note to the notes.txt file
def add_note(f, note_name):
    with open(f, 'r') as file:
        data = file.readlines()
    file = open(f, "r")
    data.append(note_name)
    with open(f, 'r') as file:
        file = open(f, "w")
    print(data)
    file.writelines(data)

#adds a freq to the frequencies.txt file
def add_freq(f, chosen_freq):
    with open(f, 'r') as file:
        data = file.readlines()
    file = open(f, "r")
    data.append(chosen_freq)
    with open(f, 'r') as file:
        file = open(f, "w")
    print(data)
    file.writelines(data)

#this is done into another function to tidy up the code
def add_note_and_freq(choose_note, choose_freq, frame_menu_add_note):
    add_freq(f_frequency, choose_freq + "\n")
    add_note(f_note, choose_note + "\n")
    success = Label(frame_menu_add_note, text=" your note is successfully added ", font=("Kikuri", 40), bg="#FFFFFF",
                    fg="#1BFF00")
    success.pack(expand=YES)


# play the sound
def sound(freq, duration):
    print(freq, ",", duration)
    # get timesteps for each sample, "duration" is note duration in seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    # generate sine wave tone
    tone = np.sin(freq * t * (2) * np.pi)
    tone2 = np.sin(freq * t * (2) * np.pi)
    tone3 = np.sin(freq * t * (2) * np.pi)
    tone *= (1*son) * (8388607 / np.max(np.abs(tone)))
    tone2 *= (0.7*son) * (8388607 / np.max(np.abs(tone2)))
    tone3 *= (0.3*son) * (8388607 / np.max(np.abs(tone3)))
    # convert to 32−bit data
    tone = tone.astype(np.int32)
    tone2 = tone2.astype(np.int32)
    tone3 = tone3.astype(np.int32)
    # convert from 32−bit to 24−bit by building a new byte buffer,
    # skipping every fourth bit
    # note : this also works for 2−channel audio
    i = 0
    a = 0
    j = 0
    byte_array = []
    for b in tone.tobytes():
        if i % 4 != 3:
            byte_array.append(b)
        i += 1
    for c in tone2.tobytes():
        if a % 4 != 3:
            byte_array.append(c)
        a += 1
    for d in tone3.tobytes():
        if j % 4 != 3:
            byte_array.append(d)
        j += 1
    audio = bytearray(byte_array)
    # start playback
    play_obj = sa.play_buffer(audio, 1, 3, sample_rate)
    # wait for playback to finish before exiting
    play_obj.wait_done()




# ------Tkinter Part---------

# Generation the window with the resolution of the computer
window = Tk()
window.title("Musico 3000")
l_window = (window.winfo_screenwidth())
h_window = (window.winfo_screenheight())
size = str(l_window) + "x" + str(h_window)
window.geometry(size)
window.iconbitmap("ico.ico")
window.config(background="#FFFFFF")

#sub menu play
def menu_play_music(frame_menu,frame_menu2):
    frame_menu2.pack_forget()
    frame_menu.pack_forget()
    frame_menu_play_music = Frame(window, bg = "white")
    color_button = random_color()
    button_play_piano = Button(frame_menu_play_music, bd = 0 , text = "Piano to play a music",fg = "#FFFFFF",font = ("Kikuri", 30) , bg = color_button,command = lambda : play_piano(frame_menu_play_music) )
    button_play_piano.pack(pady = 25,fill = X)
    color_button = random_color()
    button_play = Button(frame_menu_play_music, bd = 0 , text = "Play a partition",fg = "#FFFFFF",font = ("Kikuri", 30) , bg = color_button,command = lambda : menu_play(frame_menu_play_music) )
    button_play.pack(pady = 25,fill = X)
    menu = Button(frame_menu_play_music , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_play_music))
    menu.pack(side = BOTTOM)
    frame_menu_play_music.pack(expand = YES)

#menu play partition
def menu_play(before_window):
    #update the list
    music_list = get_music_name()
    nbr_partitions = len(music_list)

    menu_piano.grid_forget()
    before_window.pack_forget()
    frame_menu_play = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    txt = Label(frame_menu_play, text = "\n Choose the music you want \n",font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    txt.pack(expand=YES)
    list = Listbox(frame_menu_play,font = ("Kikuri", 30), width = longest_title_size )
    #generate display of music list
    for title in range(nbr_partitions):
        list.insert(title, music_list[title] )
    list.pack()
    color_button = random_color()
    receive_value = Button(frame_menu_play ,bd = 0 , text = "Validate " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: selected_element(list,frame_menu_play))
    receive_value.pack(pady = 25)
    color_button = random_color()
    menu = Button(frame_menu_play, bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_play))
    menu.pack(side = BOTTOM)
    frame_menu_play.pack(expand = YES)


def selected_element(list,frame): #listbox , frame
    #find the choose of the user
    line = list.curselection()[0]
    item = list.get(line)
    selected_item = item
    choose = ""
    letter = ""
    for letter in selected_item:
        print(letter)
        if letter == " ":
            break
        else :
            choose = choose + letter
    play(f,choose,frame) #play the music


#create menu create music
def menu_create_music(frame_menu,frame_menu2):
    frame_menu2.pack_forget()
    frame_menu.pack_forget()
    frame_menu_create_music = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    create_music = Button(frame_menu_create_music,bd = 0, text = "let the computer create music",font = ("Kikuri", 30),fg = "#FFFFFF", bg = color_button, command = lambda : menu_computer_create_music(frame_menu_create_music))
    create_music.pack(pady = 25,fill = X)
    color_button = random_color()
    upload_music = Button(frame_menu_create_music,bd = 0, text = "upload a music",fg = "#FFFFFF",font = ("Kikuri", 30), bg = color_button, command = lambda : browse_music(frame_menu_create_music))
    upload_music.pack(pady = 25,fill = X)
    color_button = random_color()
    space2 = Label(frame_menu_create_music , text = " \n " , font = ("Kikuri", 2) , bg = "#FFFFFF", fg = color_button)
    space2.pack()
    inv_trans = Button(frame_menu_create_music,bd = 0, text = "use inversion or transposition",font = ("Kikuri", 30),fg = "#FFFFFF", bg = color_button, command = lambda : menu_transposition_inversion(frame_menu_create_music))
    inv_trans.pack(pady = 25,fill = X)
    color_button = random_color()
    space3 = Label(frame_menu_create_music , text = " \n " , font = ("Kikuri", 2) , bg = "#FFFFFF", fg = color_button)
    space3.pack()
    color_button = random_color()
    menu = Button(frame_menu_create_music , text = "Menu " ,bd = 0,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_create_music))
    menu.pack(side = BOTTOM)
    frame_menu_create_music.pack(expand = YES)

#create menu of inversion and transposition
def menu_transposition_inversion(frame_menu_create_music):
    frame_menu_create_music.pack_forget()
    frame_menu_transposition_inversion = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    txt = Label(frame_menu_transposition_inversion, text = "\n Choose the music you want \n",font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    txt.pack(expand=YES)
    color_button = random_color()
    #generate display of music list
    list = Listbox(frame_menu_transposition_inversion,font = ("Kikuri", 20), width = longest_title_size )
    for title in range(nbr_partitions):
        list.insert(title, music_list[title] )
    list.pack()
    color_button = random_color()
    enter = Label(frame_menu_transposition_inversion, text = "\n Choose how much you want to shift the music if you choose transposition \n",font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    enter.pack(pady = 25)
    entrychamp1 = Entry(frame_menu_transposition_inversion)
    entrychamp1.pack(pady = 25)
    button_transposition = Button(frame_menu_transposition_inversion, bd = 0, font = ("Kikuri", 20),text = "Transposition",fg = "#FFFFFF", bg = color_button,command = lambda : transposition(f,list,frame_menu_transposition_inversion,entrychamp1) )
    button_transposition.pack(expand = YES)
    color_button = random_color()
    button_inversion = Button(frame_menu_transposition_inversion, bd = 0 ,font = ("Kikuri", 20), text = "Inversion",fg = "#FFFFFF", bg = color_button, command = lambda : inversion(f,list,frame_menu_transposition_inversion))
    button_inversion.pack(expand = YES)
    color_button = random_color()
    menu = Button(frame_menu_transposition_inversion , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_transposition_inversion))
    menu.pack(side = BOTTOM)

    frame_menu_transposition_inversion.pack(expand = YES)


#creat the piano for the animation when a music is played
piano = Frame(window)
color_button = random_color()
menu_piano = Button(piano , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(piano))
DO = Button(piano,padx=0, height=20,width=12, pady=0,bd=3,text="DO", bg="white",fg="black" )
DO.grid(row = 0, column = 1,padx=5,pady=5,sticky = "ns")
RE = Button(piano,padx=0, height=1,width=12, pady=0,bd=3,text="RE", bg="white",fg="black" )
RE.grid(row = 0, column = 2,padx=5,pady=5,sticky = "ns")
MI = Button(piano,padx=0, height=1,width=12, pady=0,bd=3,text="MI", bg="white",fg="black" )
MI.grid(row = 0, column = 3,padx=5,pady=5,sticky = "ns")
FA = Button(piano,padx=0, height=1,width=12, pady=0,bd=3,text="FA", bg="white",fg="black" )
FA.grid(row = 0, column = 4, padx=5,pady=5,sticky = "ns")
SOL = Button(piano,padx=0, height=1,width=12, pady=0,bd=3,text="SOL", bg="white",fg="black" )
SOL.grid(row = 0, column = 5,padx=5,pady=5, sticky = "ns")
LA = Button(piano,padx=0, height=1,width=12, pady=0,bd=3,text="LA", bg="white",fg="black" )
LA.grid(row = 0, column = 6,padx=5,pady=5, sticky = "ns")
SI = Button(piano,padx=0, height=1,width=12, pady=0,bd=3,text="SI", bg="white",fg="black" )
SI.grid(row = 0, column = 7,padx=5,pady=5, sticky = "ns")

#play a music
def play(f,choose,window2):
    #initialise variable
    num = find_line_file(f, choose)
    chosen_partition = read_line_file(f, num)
    frequency = calc_frequency(notes, frequencies)
    duration = calc_duration(figures, d0)
    list_partition,note = create_music_list(chosen_partition)
    freq_seq, duration_seq = read_sheet(list_partition,duration, frequency,note)
    freq_seq = floatl(freq_seq)
    duration_seq  = floatl(duration_seq)
    window2.pack_forget()
    #generate the image for the animation
    WIDTH = 300
    HEIGHT = 200
    canvas = Canvas(window,width=WIDTH,height=HEIGHT)
    canvas.pack()
    photo_image = PhotoImage(file='note.png')
    my_image = canvas.create_image(0,0,image=photo_image,anchor=NW)
    piano.pack(expand = YES)
    window2.pack_forget()

    for nb in range(len(freq_seq)):
        print(nb)
        if duration_seq[nb] > 0 and freq_seq[nb] > 0:
            #color the note plaid
            if freq_seq[nb] == 264:
                DO.config(bg = "#ff4d4d")
                window.update()
            elif freq_seq[nb] == 297:
                RE.config(bg = "#ff4d4d")
                window.update()
            elif freq_seq[nb] == 330:
                MI.config(bg = "#ff4d4d")
                window.update()
            elif freq_seq[nb] == 352:
                FA.config(bg = "#ff4d4d")
                window.update()
            elif freq_seq[nb] == 396:
                SOL.config(bg = "#ff4d4d")
                window.update()
            elif freq_seq[nb] == 440:
                LA.config(bg = "#ff4d4d")
                window.update()
            elif freq_seq[nb] == 495:
                SI.config(bg = "#ff4d4d")
                window.update()
            sound((freq_seq[nb] * tone) , duration_seq[nb] / 3000)
            #ramdom move the image of note
            x = random.uniform(-10,20)
            y = random.uniform(-10,10)
            canvas.move(my_image,x,y)

        elif duration_seq[nb] < 0 and freq_seq[nb] < 0:
            window.update()
            sleep(-1 * (duration_seq[nb] / 500))
            #ramdom move the image of note
            x = random.uniform(-10,10)
            y = random.uniform(-10,10)
            canvas.move(my_image,x,y)
        #reset the color of the piano
        DO.config(bg = "white")
        RE.config(bg = "white")
        MI.config(bg = "white")
        FA.config(bg = "white")
        SOL.config(bg = "white")
        LA.config(bg = "white")
        SI.config(bg = "white")
    #return to the menu
    piano.pack_forget()
    canvas.pack_forget()
    window2.pack()

#creat the menu for the creating music by the computer
def menu_computer_create_music(frame_menu_create_music):
    frame_menu_create_music.pack_forget()
    frame_menu_computer_create_music = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    txt = Label(frame_menu_computer_create_music, text = "\n Choose the music you want \n",font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    txt.pack(expand=YES)
    color_button = random_color()
    #generate display of music list
    list = Listbox(frame_menu_computer_create_music,font = ("Kikuri", 20), selectmode=MULTIPLE, width = longest_title_size)
    for title in range(nbr_partitions):
        list.insert(title, music_list[title] )
    list.pack()
    size = Label(frame_menu_computer_create_music, text = "\n Choose the size of the music \n",font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    size.pack()
    entrychamp1 = Entry(frame_menu_computer_create_music)
    entrychamp1.pack()
    espace = Label(frame_menu_computer_create_music, text = " ",font = ("Kikuri", 20), bg = "#FFFFFF" )
    espace.pack()
    color_button = random_color()
    charchov1 = Button(frame_menu_computer_create_music, bd = 0 , font = ("Kikuri", 20),text = "markov methode one",fg = "#FFFFFF", bg = color_button,command = lambda : markovs_chain_1(f,list,frame_menu_computer_create_music,entrychamp1) )
    charchov1.pack()
    color_button = random_color()
    charchov2 = Button(frame_menu_computer_create_music, bd = 0 ,font = ("Kikuri", 20), text = "markov methode two",fg = "#FFFFFF", bg = color_button, command = lambda : markovs_chain_2(f,list,frame_menu_computer_create_music,entrychamp1))
    charchov2.pack()
    color_button = random_color()
    menu = Button(frame_menu_computer_create_music , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_computer_create_music))
    menu.pack(side = BOTTOM)

    frame_menu_computer_create_music.pack(expand = YES)


#creat menu for browse a new partition
def browse_music(frame_menu_upload_music):
    frame_menu_upload_music.pack_forget()
    frame_menu_browse_partition = Frame(window,bg='#FFFFFF')
    # create a File Explorer label
    color_button = random_color()
    label_file_explorer = Label( frame_menu_browse_partition,  text = "File Explorer using Tkinter", font = ("Kikuri", 30), bg = "white" )
    color_button = random_color()
    button_explore = Button(frame_menu_browse_partition, bd = 0 ,  text = "Browse Files",fg = "#FFFFFF",font = ("Kikuri", 30), bg = color_button, command = lambda : browseFiles(frame_menu_browse_partition))
    label_file_explorer.pack(pady = 25,fill = X)
    button_explore.pack(pady = 25,fill = X)
    color_button = random_color()
    menu = Button(frame_menu_browse_partition , bd = 0 , text = "Menu " ,font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_browse_partition))
    menu.pack(side = BOTTOM)
    frame_menu_browse_partition.pack(expand = YES)

#creat the piano to play music
def play_piano(window_before):
    window_before.pack_forget()
    DO.config(command = lambda : sound(264,0.2))
    RE.config(command = lambda : sound(297,0.2))
    MI.config(command = lambda : sound(330,0.2))
    FA.config(command = lambda : sound(352,0.2))
    SOL.config(command = lambda : sound(396,0.2))
    LA.config(command = lambda : sound(440,0.2))
    SI.config(command = lambda : sound(495,0.2))
    menu_piano.grid(sticky = N)
    piano.pack()

#creat the menu of the settings
def menu_settings(frame_menu2):
    frame_menu2.pack_forget()
    frame_menu_settings = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    volume = Label(frame_menu_settings, text = " Volume" , font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    volume.pack(pady = 25,fill = X)
    color_button = random_color()
    button_sound_more = Button(frame_menu_settings, bd = 0 , font = ("Kikuri", 20), text = " + ",fg = "#FFFFFF", bg = color_button, command = lambda :sound_more()  )
    button_sound_more.pack(pady = 25,fill = X)
    color_button = random_color()
    button_sound_less = Button(frame_menu_settings, bd = 0 , font = ("Kikuri", 20), text = " - ",fg = "#FFFFFF", bg = color_button, command = lambda :sound_less()  )
    button_sound_less.pack(pady = 25,fill = X)
    octave = Label(frame_menu_settings, text = " Octave" , font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    octave.pack(pady = 25,fill = X)
    color_button = random_color()
    button_classic_tone = Button(frame_menu_settings, bd = 0 , font = ("Kikuri", 20), text = " high tone",fg = "#FFFFFF", bg = color_button, command = lambda :high_tone()  )
    button_classic_tone.pack(pady = 25,fill = X)
    color_button = random_color()
    button_deep_tone = Button(frame_menu_settings, bd = 0 , font = ("Kikuri", 20), text = "deep tone",fg = "#FFFFFF", bg = color_button, command = lambda :deep_tone()  )
    button_deep_tone.pack(pady = 25,fill = X)
    color_button = random_color()
    button_classic_tone = Button(frame_menu_settings, bd = 0 , font = ("Kikuri", 20), text = "classic tone",fg = "#FFFFFF", bg = color_button, command = lambda :classic_tone()  )
    button_classic_tone.pack(pady = 25,fill = X)
    color_button = random_color()
    menu = Button(frame_menu_settings , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_settings))
    menu.pack(side = BOTTOM)
    frame_menu_settings.pack(expand = YES)

#creat the settings functions
def sound_base():
    global son
    son = 1.0
def sound_more():
    global son
    if son < 1.0:
        son = son / 0.15
    sound(264,0.2)
def sound_less():
    global son
    if son > 0.05:
        son = son * 0.15
    sound(264,0.2)
def high_tone():
    global tone
    tone = 2
def deep_tone():
    global tone
    tone = (1/2)
def classic_tone():
    global tone
    tone = 1

def menu_enter_note(frame_delete_create_note):
    frame_delete_create_note.pack_forget()
    frame_menu_add_note = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    enter_name = Label(frame_menu_add_note, text = " Enter a name for the note BETWEEN 1 AND 10 CARACTERS " , font = ("Kikuri", 40) , bg = "#FFFFFF", fg = color_button)
    enter_name.pack(pady = 25)
    color_button = random_color()
    entrychamp1 = Entry(frame_menu_add_note)
    entrychamp1.pack()
    color_button = random_color()
    enter_partition = Label(frame_menu_add_note, text = " Enter a frequency (number) " , font = ("Kikuri", 40) , bg = "#FFFFFF", fg = color_button)
    enter_partition.pack(pady = 25)
    entrychamp2 = Entry(frame_menu_add_note)
    entrychamp2.pack()
    color_button = random_color()
    ok2 = Button(frame_menu_add_note, bd = 0 , text = "Enter",fg = "#FFFFFF", font = ("Kikuri", 20), bg = color_button, command = lambda : receive_note(entrychamp1, entrychamp2,frame_menu_add_note) )
    ok2.pack(pady = 25)
    color_button = random_color()
    menu = Button(frame_menu_add_note , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_add_note))
    menu.pack(side = BOTTOM)
    frame_menu_add_note.pack(expand = YES)


#receive the note of the user
def receive_note(entrychamp1,entrychamp2,frame_menu_add_note):
    #recive name and freq of note add by the user
    name_note = entrychamp1.get()
    freq_note = entrychamp2.get()
    #gestion of the error size or not enter number
    try :
        freq_note = int(freq_note)
    except:
        failure = Label(frame_menu_add_note, text = " error, freq is not a number or the name is not between 1 and 10 caracters " , font = ("Kikuri", 20) , bg = "#FFFFFF", fg = "#eb3b5a")
        failure.pack(expand = YES)
        return False
    is_between = len(name_note) in range(1,10)
    if is_between == False:
        failure = Label(frame_menu_add_note, text = " error, the name is not between 1 and 10 caracters " , font = ("Kikuri", 20) , bg = "#FFFFFF", fg = "#eb3b5a")
        failure.pack(expand = YES)
        return False
    freq_note = str(freq_note)
    add_note_and_freq(name_note,freq_note,frame_menu_add_note)
    frame_menu_add_note.pack(expand = YES)

#sub menu create or delete note
def delete_create_note(frame_menu2):
    frame_menu2.pack_forget()
    frame_delete_create_note = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    create_not= Button(frame_delete_create_note , bd = 0 , text = "create a new note " ,font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda: menu_enter_note(frame_delete_create_note))
    create_not.pack(pady = 25,fill =X)
    color_button = random_color()
    delete_not = Button(frame_delete_create_note , bd = 0 , text = "Delete a note",font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda: menu_delete_note(frame_delete_create_note))
    delete_not.pack(pady = 25,fill =X)
    color_button = random_color()
    menu = Button(frame_delete_create_note , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_delete_create_note))
    menu.pack(side = BOTTOM)
    frame_delete_create_note.pack(expand = YES)

#creat menu delete music
def menu_delete_partition(frame_menu2):
    frame_menu2.pack_forget()
    frame_menu_delete_partition = Frame(window, bg = "#FFFFFF")
    music_list = get_music_name()
    nbr_partitions = len(music_list)
    color_button = random_color()
    txt = Label(frame_menu_delete_partition, text = "\n Choose the music you want \n",font = ("Kikuri", 20) , bg = "#FFFFFF", fg = color_button)
    txt.pack(expand=YES)
    #generate display of the music list
    list = Listbox(frame_menu_delete_partition,font = ("Kikuri", 30), width = longest_title_size )
    for title in range(nbr_partitions):
        list.insert(title, music_list[title] )
    list.pack()
    color_button = random_color()
    receive_value = Button(frame_menu_delete_partition , bd = 0 , text = "Validate " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: selected_element2(list,frame_menu_delete_partition))
    receive_value.pack(pady = 25)
    color_button = random_color()
    menu = Button(frame_menu_delete_partition , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_delete_partition))
    menu.pack(side = BOTTOM)
    frame_menu_delete_partition.pack()

def selected_element2(list,frame_menu_delete_partition):
    #recive the choose of the user
    line = list.curselection()[0]
    item = list.get(line)
    selected_item = item
    print(selected_item)
    choose = ""
    letter = ""
    for letter in selected_item:
        if letter == " ":
            break
        else :
            choose = choose + letter

    delete_partition(f,choose)
    #update list
    refresh_list_music(list)
    success = Label(frame_menu_delete_partition , text = " the partition is successfully removed " , font = ("Kikuri", 20) , bg = "#FFFFFF", fg = "#26de81")
    success.pack(expand = YES)
    frame_menu_delete_partition.pack()


#creat menu delete a note
def menu_delete_note(frame_delete_create_note):
    notes = create_list_note()
    frame_delete_create_note.pack_forget()
    frame_menu_delete_note = Frame(window,bg='#FFFFFF')
    #generate the display of the list note
    list = Listbox(frame_menu_delete_note,font = ("Kikuri", 30), width = longest_title_size )
    for nbr_note in range(len(notes)):
        list.insert(nbr_note, notes[nbr_note] )
    list.pack()
    color_button = random_color()
    receive_value = Button(frame_menu_delete_note , bd = 0 , text = "Validate " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: selected_element3(list,frame_menu_delete_note))
    receive_value.pack(pady = 25)
    color_button = random_color()
    menu = Button(frame_menu_delete_note , bd = 0 , text = "Menu " ,font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu_delete_note))
    menu.pack(side = BOTTOM)
    frame_menu_delete_note.pack()


def selected_element3(list,frame_menu_delete_note):
    #recive the note choose by the user
    line = list.curselection()[0]
    item = list.get(line)
    selected_item = item
    print(selected_item)
    choose = ""
    letter = ""
    for letter in selected_item:
        print(letter)
        if letter == " ":
            break
        else :
            choose = choose + letter

    freq_note = calc_frequency(notes,frequencies)
    chosen_freq = choose
    chosen_freq = str(chosen_freq) + "\n"
    choose = choose + "\n"
    print(chosen_freq,choose)
    delete_noteandfreq(f_frequency,f_note,chosen_freq,choose,frame_menu_delete_note)
    #refresh the list of note
    refresh_list_note(list)


#generate the main menu of the program
def principal_menu(window2):
    window2.pack_forget()
    frame_menu2 = Frame(window,bg='#FFFFFF')
    color_button = random_color()
    title2 = Label(frame_menu2 , text = " Musico 3000 , choose an action " , font = ("Kikuri", 40) , bg = "#FFFFFF", fg = color_button)
    title2.pack(pady = 25,fill =X)
    color_button = random_color()
    play_music = Button(frame_menu2 , bd = 0 , text = "Play a music " ,font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda: menu_play_music(frame_menu,frame_menu2))
    play_music.pack(pady = 25,fill =X)
    color_button = random_color()
    create_music = Button(frame_menu2 , bd = 0 , text = "Add a music",font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda: menu_create_music(frame_menu,frame_menu2))
    create_music.pack(pady = 25,fill =X)
    color_button = random_color()
    create_note = Button(frame_menu2 , bd = 0 , text = "Create or delete a note",font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda : delete_create_note(frame_menu2) )
    create_note.pack(pady = 25,fill =X)
    color_button = random_color()
    delete = Button(frame_menu2 , bd = 0 , text = "Delete a music",font = ("Kikuri", 30) , bg = color_button, fg = "#FFFFFF", command = lambda : menu_delete_partition(frame_menu2) )
    delete.pack(pady = 25,fill =X)
    color_button = random_color()
    settings = Button(frame_menu2 , bd = 0 , text = "Settings",font = ("Kikuri", 20) , bg = color_button, fg = "#FFFFFF", command = lambda : menu_settings(frame_menu2) )
    settings.pack(side = BOTTOM)
    frame_menu2.pack(expand = YES)


#create variable
music_list = get_music_name()
nbr_partitions = len(music_list)
longest_title_size = longest_title(music_list)
notes = create_list_note()
frequencies = create_frequencies_list()
classic_tone()
sound_base()

#generate the home (first menu of the program)
width = 300
height = 300
height2 = 600
frame_menu = Frame(window,bg='#FFFFFF')
image = PhotoImage(file ="image.png").zoom(30).subsample(32)
canvas = Canvas(frame_menu, width=width , height = height,background = "#FFFFFF", bd =0 , highlightthickness = 0)
#creat a canvas with the image
canvas.create_image(width/2 , height/2 , image=image)
canvas.pack()
title = Label(frame_menu , text = " Welcome to Musico 3000, the music for the all family " , font = ("Kikuri", 30) , bg = "#FFFFFF", fg = "#f7b731")
title.pack(pady = 25,fill =X)
color_button = random_color()
menu_p = Button(frame_menu , bd = 0 , text = "Menu " ,font = ("Kikuri", 25) , bg = color_button, fg = "#FFFFFF", command = lambda: principal_menu(frame_menu))
menu_p.pack(pady = 25,fill =X)
image2 = PhotoImage(file ="image2.png").zoom(30).subsample(32)
canvas = Canvas(frame_menu, width=width , height = height2,background = "#FFFFFF", bd =0 , highlightthickness = 0)
canvas.create_image(width/2 , height/2 , image=image2)
canvas.pack()
#creation of the button quit
quit = Button(window , bd = 0 , text = "Quit",font = ("Kikuri", 20) , bg = "#eb3b5a", fg = "#FFFFFF", command = window.quit )
quit.pack(side = BOTTOM)
frame_menu.pack(expand = YES)

#tkinter loop
window.mainloop()











