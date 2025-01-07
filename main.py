import streamlit as st
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import src.users as users
import src.devices as devices
import src.queries as queries

user_manager = users.User()
device_manager = devices.Device()
#reservation_manager = Datenbank.Reservation()

st.title("Geräte- und Reservierungsmanager")

menu = st.sidebar.radio("Menü", ["Benutzer", "Geräte", "Reservierungen"])

if menu == "Benutzer":
    action = st.radio("Aktion", ["Benutzer hinzufügen", "Benutzer bearbeiten"])
    if action == "Benutzer hinzufügen":
        st.header("Benutzerverwaltung")
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Benutzer hinzufügen"):
            user_manager.add(name, email)
            st.success("Benutzer hinzugefügt")

        st.subheader("Benutzerliste")
    
    if action == "Benutzer bearbeiten":
        users = user_manager.get_all()
        user_id = st.selectbox("Benutzer auswählen", [user.doc_id for user in user_manager.table], format_func=lambda x: next(u['name'] for u in users if u.doc_id == x))
        user = next(u for u in users if u.doc_id == user_id)

        name = st.text_input("Name", value=user['name'])
        email = st.text_input("Email", value=user['email'])

        if st.button("Benutzer aktualisieren"):
            user_manager.table.update({'name': name, 'email': email}, doc_ids=[user_id])
            st.success("Benutzer aktualisiert")
    
    users = user_manager.get_all()
    for user in users:
        st.write(f"Name: {user['name']}, Email: {user['email']}")

elif menu == "Geräte":
    st.header("Geräteverwaltung")
    action = st.radio("Aktion", ["Gerät hinzufügen", "Gerät bearbeiten"])

    if action == "Gerät hinzufügen":
        name = st.text_input("Gerätename")
        responsible = st.text_input("Verantwortlicher")
        end_of_life = st.date_input("End of Life")
        maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1)
        maintenance_cost = st.number_input("Wartungskosten", min_value=0.0, step=0.01)
        status = st.selectbox("Status", ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"])
        if st.button("Gerät hinzufügen"):
            device_manager.add(name, responsible, end_of_life, maintenance_interval, maintenance_cost, status)
            st.success("Gerät hinzugefügt")

    elif action == "Gerät bearbeiten":
        devices = device_manager.get_all()
        device_id = st.selectbox("Gerät auswählen", [device.doc_id for device in device_manager.table], format_func=lambda x: next(d['name'] for d in devices if d.doc_id == x))
        device = next(d for d in devices if d.doc_id == device_id)

        name = st.text_input("Gerätename", value=device['name'])
        responsible = st.text_input("Verantwortlicher", value=device['responsible'])
        end_of_life = st.date_input("End of Life", value=datetime.strptime(device['end_of_life'], '%Y-%m-%d'))
        maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1, value=device['maintenance_interval'])
        maintenance_cost = st.number_input("Wartungskosten", min_value=0.0, step=0.01, value=device['maintenance_cost'])
        status = st.selectbox("Status", ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"], index=["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"].index(device['status']))

        if st.button("Gerät aktualisieren"):
            device_manager.table.update({
                'name': name,
                'responsible': responsible,
                'end_of_life': end_of_life.strftime('%Y-%m-%d'),
                'maintenance_interval': maintenance_interval,
                'maintenance_cost': maintenance_cost,
                'status': status
            }, doc_ids=[device_id])
            st.success("Gerät aktualisiert")

    st.subheader("Geräteliste")
    devices = device_manager.get_all()
    for device in devices:
        st.write(f"Name: {device['name']}, Verantwortlicher: {device['responsible']}, Status: {device['status']}")

elif menu == "Reservierungen":
    st.header("Reservierungssystem")

    users = user_manager.get_all()
    devices = device_manager.get_all()

    if not users or not devices:
        st.warning("Bitte fügen Sie zuerst Benutzer und Geräte hinzu.")
    else:
        user_id = st.selectbox(
            "Benutzer", 
            [user.doc_id for user in user_manager.table], 
            format_func=lambda x: next(u['name'] for u in users if u.doc_id == x)
        )
        device_id = st.selectbox(
            "Gerät", 
            [device.doc_id for device in device_manager.table], 
            format_func=lambda x: next(d['name'] for d in devices if d.doc_id == x)
        )
        
        start_date = st.date_input("Startdatum")
        start_time = st.time_input("Startzeit")
        end_date = st.date_input("Enddatum", value=start_date)
        end_time = st.time_input("Endzeit", value=(datetime.combine(start_date, start_time) + timedelta(hours=1)).time())

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        if end_time <= start_time:
            st.error("Endzeit muss nach der Startzeit liegen.")
        else:
            if st.button("Reservieren"):
                if reservation_manager.add(user_id, device_id, start_time, end_time):
                    st.success("Reservierung erfolgreich")
                else:
                    st.error("Konflikt: Gerät ist bereits reserviert")

    st.subheader("Reservierungsliste")
    reservations = reservation_manager.get_all()
    for res in reservations:
        st.write(f"Benutzer ID: {res['user_id']}, Gerät ID: {res['device_id']}, Von: {res['start_time']}, Bis: {res['end_time']}")


#test