###################################LIBRERIE E DEFINIZIONE FINESTRA PRINCIPALE ###########################

import re
import tkinter as tk
from tkinter.font import Font
from tkinter import simpledialog
import sys 

window = tk.Tk()
window.title("The zoning tool")
window.geometry("")
window.resizable(False, False)

############################################ FUNZIONI PRINCIPALI ########################################

def start():

    begin = get_input()
    correction = ['"Your vSAN_ID"', '"Your Initiator"', '"Your Target"', '"Your Zoneset"']
    values = []
    mex = ""
    check = all(ele != "" for ele in begin)
    
    if not begin[0].isnumeric():

        mex = f'Please insert a correct vSAN ID. \nUser defined vSANs are available from 2 to 4096.'
        tk.messagebox.showerror("Input error", mex)
    
    if begin[0].isnumeric() and check == True:
        
        T.config(state="normal")
        create_zoning(begin)

    else:

        for x in range(len(begin)):
        
            if begin[x] == "":

                values.append(x)
        
        for y in range(len(values)):
    
            index = values[y]
            mex = f'Empty fields are not allowed! \nPlease check the following field: {correction[index]}'
            tk.messagebox.showerror("Input error", mex) 
     
        clear_single_box(T)

def test_input(a, label):

    #a = e1.get(1.0, tk.END)
    array = a.splitlines()
    array_splitted = [i.split() for i in array]
    x = 0
    wwpn_list = []

    while x != len(array_splitted):

        if len(array_splitted[x]) <= 1 or len(array_splitted[x]) >= 3:

            str0 = " ".join(array_splitted[x])
            invalid = f'Invalid Format in field {label} \nPlease check: "{str0}"  \n\nUse the following format: \n"<Device alias> <pwwn>'
            tk.messagebox.showerror("Input error", invalid)
            clear_single_box(T)
            case = 1

        elif not re.match("([0-9a-f]{2}:){7}[0-9a-f]{2}", str(array_splitted[x][1])):
            
            str0 = (array_splitted[x][1])
            invalid = f'Invalid PWWN in field {label} \nPlease check: "{str0}" \n\nMake sure your PWWN is in the format: \n"AZ09:AZ09:AZ09:AZ09:AZ09:AZ09:AZ09" \ncheck the field {label}'
            tk.messagebox.showerror("Input error", invalid)
            clear_single_box(T)
            case = 1

        else:
            
            wwpn_list.append(array_splitted[x])
            case = 0
                               
        x += 1
    return  wwpn_list, case
    #tk.messagebox.showinfo("Output", wwpn_list)   

def get_input():

    clear_single_box(T)
    e0_input = e0.get(1.0,"end-1c")
    e1_input = e1.get(1.0, "end-1c")
    e2_input = e2.get(1.0, "end-1c")
    e3_input = e3.get(1.0, "end-1c")
    
    check_input = [e0_input, e1_input, e2_input, e3_input]
        
    return check_input

def create_alias(array):

    str0 = ""

    for x in range(len(array)):

        alias = array[x][0]
        pwwn = array[x][1]
        str0 = f' {str0} \n device-alias name {alias} pwwn {pwwn}'
       
    command = f'configure \ndevice alias database {str0} \n device-alias commit'
    return command

def create_zone(alias_initiator, array_target, id):

    str0 = f'\n member device-alias {alias_initiator}'
    str1 = ""

    for t in range(len(array_target)):

        alias_target = array_target[t][0]
        str0 = f'{str0} \n member device-alias {alias_target}' 
        str1 = f'{str1}_{alias_target}'

    zone_name = f'{alias_initiator}{str1}'
    command = f'\n\nconfigure \nzone name {zone_name} vsan {id} {str0}'
                
    return command, zone_name

def print_output(out):
    
    out = str(out)
    T.config(state="normal", bg="#32cd32", fg="White")
    T.insert(tk.INSERT, out)

def clear_single_box(x):

    x.delete(1.0, tk.END)
    x.config(state="disabled", bg="white")   
    
def create_zoning(start_list):

    vsan_id = start_list[0]
    initiators = start_list[1]
    target = start_list[2] 
    zoneset = start_list[3]
    
    zone_list = []
    output_zone = ""
    word1 = '"Your Initiator"'
    word2 = '"Your Target"'
    initiators, check_1 = test_input(initiators, word1)
    target, check_2 = test_input(target, word2)

    if check_1 == 0 and check_2 == 0:

        all_wwpn = initiators + target

        for i in range(len(initiators)):

            zone_config, zone = create_zone(initiators[i][0], target, vsan_id)
            output_zone = f'{output_zone} {zone_config}'
            zone_list.append(zone)

        output_zoneset = add_zone_to_zoneset(zone_list, zoneset, vsan_id)
        output_wwpn = create_alias(all_wwpn)
        output_zoneset = add_zone_to_zoneset(zone_list, zoneset, vsan_id)

        print_output(output_wwpn)
        print_output(output_zone)
        print_output(output_zoneset)

def add_zone_to_zoneset(array_zone, zsname, vs_id):

    member = ""
    command = ""

    for z in range(len(array_zone)):

        member = f'{member} \n member {array_zone[z]}'
        command = f'\n\nzoneset name {zsname} vsan {vs_id} {member} \n\nzoneset activate name {zsname} vsan {vs_id}'

    return command

def create_smartzoning():

    tk.messagebox.showerror("Input error", "The feature will be developed as soon as possible... :(")
        
def clear_all():

    e0.config(state="normal", bg="white")
    e0.delete(1.0, tk.END)
    e1.config(state="normal", bg="white")
    e1.delete(1.0, tk.END)
    e2.config(state="normal", bg="white")
    e2.delete(1.0, tk.END)
    e3.config(state="normal", bg="white")
    e3.delete(1.0, tk.END)
    T.config(state="normal", bg="white")
    T.delete(1.0, tk.END)

def print_help():

    mex = f'Insert Valid initiator and target in format: \n<Device Alias> <PWWN> \n\nExample: \n"LMI647_Slot8_vHBA_A 20:00:00:25:b5:99:aa:00"'
    tk.messagebox.showinfo(title="Welcome Help", message=mex)
    mex =  f'Below you will find an example of correct use of the tool!'
    tk.messagebox.showinfo(title="Welcome Help", message=mex)
    mex = f'Use the "Clear all textbox" button to delete the sample text.'
    tk.messagebox.showinfo(title="Welcome Help", message=mex)
    e0.insert(tk.INSERT, 10)
    e1.insert(tk.INSERT, "TEST_DEVICE_ALIAS_01 20:00:00:25:b5:99:aa:01")
    e1.insert(tk.INSERT, "\nTEST_DEVICE_ALIAS_02 20:00:00:25:b5:99:aa:02")
    e2.insert(tk.INSERT, "TEST_DEVICE_ALIAS_03 50:00:00:25:b5:99:aa:03")
    e2.insert(tk.INSERT, "\nTEST_DEVICE_ALIAS_04 50:00:00:25:b5:99:aa:04")
    e3.insert(tk.INSERT, "ZONESET_NAME_TEST")
    start()

############################################ Main Code ##################################################
############################################ LABEL DI TESTO #############################################

label0 = tk.Label(window, text="Your vSAN ID:", font=("Arial", 12))
label0.grid(row=0, column=0, padx=10, pady=5)
label1 = tk.Label(window, text="Your Initiator:", font=("Arial", 12))
label1.grid(row=1, column=0, padx=10, pady=5)
label2 = tk.Label(window, text="Your Target:", font=("Arial", 12))
label2.grid(row=2, column=0, padx=10, pady=5)
label3 = tk.Label(window, text="Your Zoneset:", font=("Arial", 12))
label3.grid(row=3, column=0, padx=10, pady=5)

############################################ TEXTBOX ####################################################

e0 = tk.Text(window, height=3, width=70)
e0.grid(row=0, column=1, columnspan=1, padx=50, pady=5)
e0.config(state="normal", bg="white")
e1 = tk.Text(window, height=3, width=70)
e1.grid(row=1, column=1, columnspan=1, padx=50, pady=5)
e1.config(state="normal", bg="white")
e2 = tk.Text(window, height=3, width=70)
e2.grid(row=2, column=1, columnspan=1, padx=50, pady=5)
e2.config(state="normal", bg="white")
e3 = tk.Text(window, height=3, width=70)
e3.grid(row=3, column=1, columnspan=1, padx=80, pady=5)
e3.config(state="normal", bg="white")
message = "Configuration text output"
T = tk.Text(window, height=25, width=100, font=("Courier New", 8))
T.config(state="normal")
T.insert(tk.INSERT, message)
T.grid(row=5, column=1, rowspan=4, columnspan=2, padx=10, pady=5)

############################################ BOTTONI ####################################################

zone_button = tk.Button(text="Create Zoning Configuration", command=start, font=("Arial", 10), height=2, width=25, fg="green")
zone_button.grid(row=5, column=0, columnspan=1, padx=20, pady=5)
smartzone_button = tk.Button(text="Create SmartZoning Configuration", command=create_smartzoning, font=("Arial", 10), height=2, width=25)
smartzone_button.grid(row=6, column=0, columnspan=1, padx=20, pady=5)
clear_all_button = tk.Button(text="Clear all textbox", command=clear_all, font=("Arial", 10), height=2, width=25, fg="red")
clear_all_button.grid(row=7, column=0, columnspan=1, padx=20, pady=5)
help_button = tk.Button(text="Help", command=print_help, font=("Arial", 10), height=2, width=25)
help_button.grid(row=8, column=0, columnspan=1, padx=20, pady=5)

############################################ MAIN CODE AND MAINLOOP() ##############################################

author = tk.Label(window, text="Developed by Bottalu", font=("Arial", 7))
author.grid(row=9, column=0, columnspan=1)

if __name__ == "__main__":
    window.mainloop()                      


#############################################################################################
###################TIPS######################################################################
#zone = simpledialog.askstring("input string", "Enter value")   input con popup box
#
# 
# TO CREATE EXECUTABLE FILE USE THE FOLLOWING TOOL: pyinstaller zoning.py --noconsole --onefile
# 
# 
#           

                    









