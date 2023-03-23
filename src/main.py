import sys
import PySimpleGUI as sg

# Simula una lista de hosts activos para fines de demostración
# Reemplaza esto con la funcionalidad de lectura/escritura de archivos de hosts según sea necesario
active_hosts = [
    {"host": "127.0.0.1", "destination": "example.com", "active": True},
    {"host": "192.168.1.1", "destination": "mywebsite.local", "active": False},
]

def toggle_host_activation(host):
    host["active"] = not host["active"]
    print(f"Host {host['host']} {'activado' if host['active'] else 'desactivado'}")

def add_host(host_str, destination_str):
    active_hosts.append({"host": host_str, "destination": destination_str, "active": True})
    print(f"Host agregado: {host_str} {destination_str}")

def remove_host(host_str, destination_str):
    active_hosts[:] = [host for host in active_hosts if host["host"] != host_str or host["destination"] != destination_str]
    print(f"Host eliminado: {host_str} {destination_str}")

def show_hosts_popup():
    layout = [
        [sg.Text("Hosts")],
        *[
            [sg.Checkbox(f"{host['host']} {host['destination']}", default=host["active"], key=f"{host['host']} {host['destination']}", enable_events=True)]
            for host in active_hosts
        ],
        [sg.InputText(key="new_host"), sg.InputText(key="new_destination"), sg.Button("Agregar", key="add_host")],
        [sg.Button("Eliminar host seleccionado", key="remove_host")],
        [sg.Button("Cerrar")],
    ]

    window = sg.Window("Configuración de hosts", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cerrar":
            break
        elif event in [f"{host['host']} {host['destination']}" for host in active_hosts]:
            toggle_host_activation(next(host for host in active_hosts if f"{host['host']} {host['destination']}" == event))
        elif event == "add_host":
            add_host(values["new_host"], values["new_destination"])
            window.close()
            show_hosts_popup()
            break
        elif event == "remove_host":
            selected_host = next((host for host in active_hosts if f"{host['host']} {host['destination']}" in values and values[f"{host['host']} {host['destination']}"]), None)
            if selected_host:
                remove_host(selected_host["host"], selected_host["destination"])
                window.close()
                show_hosts_popup()
                break

    window.close()

if __name__ == "__main__":
    show_hosts_popup()
