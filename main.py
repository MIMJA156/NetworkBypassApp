import os
import random
import string
import winreg
import netifaces
import tkinter
from tkinter import messagebox


def get_values(key):
    key_dict = {}
    i = 0
    while True:
        try:
            sub_value = winreg.EnumValue(key, i)
        except WindowsError:
            break
        key_dict[sub_value[0]] = sub_value[1:]
        i += 1
    return key_dict


def get_correct_interface():
    current_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    print(current_interface)

    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
        path = string.Template("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\$n1")
        key_index = -1

        while True:
            key_index += 1
            key_string = f"{key_index}"
            key = ("0000" + key_string)[len(key_string):]

            try:
                sub_key = winreg.OpenKey(hkey, path.substitute(n1=key), 0, winreg.KEY_ALL_ACCESS)
                selected_interface_values = get_values(sub_key)

                if selected_interface_values["NetCfgInstanceId"][0] == current_interface:
                    return sub_key

            except PermissionError:
                messagebox.showwarning(title="<3", message="This program requires administrator privileges to run.")
                root.destroy()
                break

            except WindowsError:
                break


def spoof_mac():
    sub_key = get_correct_interface()

    if type(sub_key).__name__ != "PyHKEY":
        print("No Interface")
        return

    winreg.SetValueEx(sub_key, "NetworkAddress", 0, winreg.REG_SZ, f"DE{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}")
    winreg.CloseKey(sub_key)

    response = messagebox.askyesno(title="Restart?",
                                   message="Your PC Needs To Restart For The Changes To Take Affect.\nRestart Now?")
    if response:
        os.system("shutdown /r /t 0")


def undo_spoof():
    sub_key = get_correct_interface()

    if type(sub_key).__name__ != "PyHKEY":
        print("No Interface")
        return

    winreg.DeleteValue(sub_key, "NetworkAddress")
    winreg.CloseKey(sub_key)

    response = messagebox.askyesno(title="Restart?",
                                   message="Your PC Needs To Restart For The Changes To Take Affect.\nRestart Now?")
    if response:
        os.system("shutdown /r /t 0")


root = tkinter.Tk()

root.title("<3")
root.geometry("200x100+50+50")
root.resizable(False, False)

main_text = tkinter.Message(root, text="I am awaiting your command...", width=200)
spoof = tkinter.Button(root, text="Spoof Mac Address", command=spoof_mac)
undo = tkinter.Button(root, text="Set Back To Default", command=undo_spoof)

main_text.pack()
spoof.pack()
undo.pack()

root.mainloop()
