import sys
import os

import PySimpleGUI as sg

HOSTS_FILE = "/etc/hosts" if os.name == "posix" else "C:\\Windows\\System32\\drivers\\etc\\hosts"

def read_hosts_file():
    active_hosts = []

    with open(HOSTS_FILE, "r") as hosts_file:
        for line in hosts_file:
            line = line.strip()

            if not line or line.startswith("#") and not line[1:].strip().split(None, 1):
                continue

            is_active = not line.startswith("#")

            if not is_active:
                line = line[1:].strip()

            parts = line.split(None, 1)

            if len(parts) == 2:
                host, destination = parts
                active_hosts.append({"host": host, "destination": destination, "active": is_active})

    return active_hosts



def write_hosts_file(active_hosts):
    with open(HOSTS_FILE, "w") as f:
        for host in active_hosts:
            line = f"{'#' if not host['active'] else ''}{host['host']} {host['destination']}\n"
            f.write(line)

def toggle_host_activation(host):
    host["active"] = not host["active"]
    print(f"Host {host['host']} {'activado' if host['active'] else 'desactivado'}")
    write_hosts_file(active_hosts)

def add_host(host_str, destination_str):
    active_hosts.append({"host": host_str, "destination": destination_str, "active": True})
    print(f"Host agregado: {host_str} {destination_str}")
    write_hosts_file(active_hosts)

def remove_host(host_str, destination_str):
    active_hosts[:] = [host for host in active_hosts if host["host"] != host_str or host["destination"] != destination_str]
    print(f"Host eliminado: {host_str} {destination_str}")
    write_hosts_file(active_hosts)

def show_hosts_popup():
    layout = [
        [sg.Text("Hosts")],
        *[
            [
                sg.Checkbox(f"{host['host']} {host['destination']}", default=host["active"], key=f"{host['host']} {host['destination']}", enable_events=True),
                sg.Button("X", key=f"remove_{host['host']} {host['destination']}", border_width=0)
            ]
            for host in active_hosts
        ],
        [
           
            sg.Column([
                [sg.Text("Host"), sg.InputText(key="new_host", size=(15, 1))],
                [sg.Text("Destination"), sg.InputText(key="new_destination", size=(15, 1))],
            ]),
            sg.Button("Agregar", key="add_host")
        ],
        [sg.Button("Cerrar")],
    ]

    frame_layout = [
        [sg.Frame("", layout, border_width=5, background_color="black", title_color="black", relief="ridge")]
    ]

    window = sg.Window("Configuración de hosts", frame_layout, finalize=True, background_color="black")

    for element in window.AllKeysDict.values():
        if isinstance(element, sg.Button) and not element.ImageFilename:
            element.Widget.config(borderwidth=5, relief="ridge", highlightthickness=0)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cerrar":
            break
        elif event in [f"{host['host']} {host['destination']}" for host in active_hosts]:
            toggle_host_activation(next(host for host in active_hosts if f"{host['host']} {host['destination']}" == event))
            write_hosts_file(active_hosts)
        elif event.startswith("remove_"):
            host_key = event[7:]
            selected_host = next((host for host in active_hosts if f"{host['host']} {host['destination']}" == host_key), None)
            if selected_host:
                confirmation = sg.popup_yes_no("¿Está seguro de que desea eliminar este host?")
                if confirmation == "Yes":
                    remove_host(selected_host["host"], selected_host
                    ["destination"])
                    window.close()
                    show_hosts_popup()
                    break
        
        elif event == "add_host":
            add_host(values["new_host"], values["new_destination"])
            window.close()
            show_hosts_popup()
            break

    window.close()

if __name__ == "__main__":
    active_hosts = read_hosts_file()
    show_hosts_popup()
    write_hosts_file(active_hosts)
