import os
import tkinter as tk
from tkinter import messagebox
import netifaces as net
import winreg
from string import Template
from py_essentials import simpleRandom


def get_values(key):
    key_dict = {}
    i = 0
    while True:
        try:
            sub_value = winreg.EnumValue(key, i)
        except WindowsError as e:
            break
        key_dict[sub_value[0]] = sub_value[1:]
        i += 1
    return key_dict


# def get_correct_interface():
#     current_interface = net.gateways()['default'][net.AF_INET][1]
#     print(current_interface)
#
#     with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
#         path = Template("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\$n1")
#         key_index = -1
#
#         while True:
#             key_index += 1
#             key_string = f"{key_index}"
#             key = ("0000" + key_string)[len(key_string):]
#
#             try:
#                 with winreg.OpenKey(hkey, path.substitute(n1=key), 0, winreg.KEY_ALL_ACCESS) as sub_key:
#                     selected_interface_values = get_values(sub_key)
#
#                     if selected_interface_values["NetCfgInstanceId"][0] == current_interface:
#                         return [key, selected_interface_values]
#
#             except WindowsError as e:
#                 return


def spoof_mac():
    current_interface = net.gateways()['default'][net.AF_INET][1]
    print(current_interface)

    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
        path = Template("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\$n1")
        run = True
        key_index = 0

        while run:
            key_index += 1
            key_string = f"{key_index}"
            key = ("0000" + key_string)[len(key_string):]

            try:
                with winreg.OpenKey(hkey, path.substitute(n1=key), 0, winreg.KEY_ALL_ACCESS) as sub_key:
                    selected_interface_values = get_values(sub_key)

                    if selected_interface_values["NetCfgInstanceId"][0] == current_interface:
                        winreg.SetValueEx(sub_key, "NetworkAddress", 0, winreg.REG_SZ,
                                          f"DE{simpleRandom.randomString(10)}")

                        response = messagebox.askyesno(title="Restart?",
                                                       message="Your PC Needs To Restart For The Changes To Take Affect.\nRestart Now?", )
                        if response:
                            os.system("shutdown /r /t 0")
                        run = False

            except WindowsError as e:
                run = False


def undo_spoof():
    current_interface = net.gateways()['default'][net.AF_INET][1]
    print(current_interface)

    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
        path = Template("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\$n1")
        run = True
        key_index = 0

        while run:
            key_index += 1
            key_string = f"{key_index}"
            key = ("0000" + key_string)[len(key_string):]

            try:
                with winreg.OpenKey(hkey, path.substitute(n1=key), 0, winreg.KEY_ALL_ACCESS) as sub_key:
                    selected_interface_values = get_values(sub_key)

                    if selected_interface_values["NetCfgInstanceId"][0] == current_interface:
                        winreg.DeleteValue(sub_key, "NetworkAddress")

                        response = messagebox.askyesno(title="Restart?",
                                                       message="Your PC Needs To Restart For The Changes To Take Affect.\nRestart Now?", )
                        if response:
                            os.system("shutdown /r /t 0")
                        run = False

            except WindowsError as e:
                run = False


root = tk.Tk()

root.title("<3")
root.geometry("200x100+50+50")
root.resizable(False, False)

main_text = tk.Message(root, text="I am awaiting your command...", width=200)
spoof = tk.Button(root, text="Spoof Mac Address", command=spoof_mac)
undo = tk.Button(root, text="Set Back To Default", command=undo_spoof)

main_text.pack()
spoof.pack()
undo.pack()

root.mainloop()
