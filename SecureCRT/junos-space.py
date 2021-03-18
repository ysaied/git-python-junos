#$language = "Python"
#$interface = "1.0"
import SecureCRT

def main():
    tab = crt.GetScriptTab()

    if tab.Session.Connected != True:
        crt.Dialog.MessageBox(
            "Error.\n" +
            "This script was designed to be launched after a valid "+
            "connection is established.\n\n"+
            "Please connect to a remote machine before running this script.")
        return

    tab.Screen.Synchronous = True

    for x in range(3):
        match_index = tab.Screen.WaitForStrings(match_txt) - 1
        tab.Screen.Send(send_txt[match_index] + "\n")

match_txt = [
    "[1-7,AQR]:",
    "password for admin:"
    ]

send_txt = [
    "7",
    "Juniper@123@123"
    ]

main()