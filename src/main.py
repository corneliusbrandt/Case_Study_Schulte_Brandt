import streamlit as st
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import users as users
import devices as devices
import queries as queries
import reservations as reservations


st.title("Geräte- und Reservierungsmanager")

menu = st.sidebar.radio("Menü", ["Benutzer", "Geräte", "Reservierungen"])

if menu == "Benutzer":
    action = st.radio("Aktion", ["Benutzer hinzufügen", "Benutzer bearbeiten"])
    if action == "Benutzer hinzufügen":
        st.header("Benutzerverwaltung")
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Benutzer hinzufügen"):
            users.User(name, email).store_data()
            st.success("Benutzer hinzugefügt")

        st.subheader("Benutzerliste")
    
    if action == "Benutzer bearbeiten":
        users_in_db = queries.find_users()
        #user_id = st.selectbox("Benutzer auswählen", [user.doc_id for user in users_in_db], format_func=lambda x: next(u['name'] for u in users_in_db if u.doc_id == x))
        #user = next(u for u in users if u.doc_id == user_id)
        #user = users.User.find_by_attribute("name", user_id)

        current_user_id = st.selectbox('Benutzer auswählen', options=users_in_db, key="sbUser")
        loaded_user = users.User.find_by_attribute("name", current_user_id)

        name = st.text_input("Name", value=loaded_user['name'])
        email = st.text_input("Email", value=loaded_user['email'])

        if st.button("Benutzer aktualisieren"):
            #user_manager.table.update({'name': name, 'email': email}, doc_ids=[user_id])
            loaded_user.store_data()
            st.success("Benutzer aktualisiert")
    
    users = queries.find_users()
    for user in users:
        st.write(f"Name: {user['name']}, Email: {user['email']}")

elif menu == "Geräte":
    st.header("Geräteverwaltung")
    action = st.radio("Aktion", ["Gerät hinzufügen", "Gerät bearbeiten"])

    if action == "Gerät hinzufügen":
        device_name = st.text_input("Gerätename")
        managed_by_user_id = st.text_input("Verantwortlicher")
        end_of_life = st.date_input("End of Life")
        maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1)
        maintenance_cost = st.number_input("Wartungskosten", min_value=0.0, step=0.01)
        status = st.selectbox("Status", ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"])
        if st.button("Gerät hinzufügen"):
            #device_manager.store_data()
            devices.Device(device_name, managed_by_user_id, end_of_life, maintenance_interval, maintenance_cost, status).store_data()
            st.success("Gerät hinzugefügt")

    elif action == "Gerät bearbeiten":
        devices = queries.find_devices()
        device_id = st.selectbox("Gerät auswählen", [device.doc_id for device in devices], format_func=lambda x: next(d['name'] for d in devices if d.doc_id == x))
        device = next(d for d in devices if d.doc_id == device_id)

        name = st.text_input("Gerätename", value=device['device_name'])
        managed_by_user_id = st.text_input("Verantwortlicher", value=device['manged_by_user_id'])
        end_of_life = st.date_input("End of Life", value=datetime.strptime(device['end_of_life'], '%Y-%m-%d'))
        maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1, value=device['maintenance_interval'])
        maintenance_cost = st.number_input("Wartungskosten", min_value=0.0, step=0.01, value=device['maintenance_cost'])
        status = st.selectbox("Status", ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"], index=["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"].index(device['status']))

        if st.button("Gerät aktualisieren"):
            device.store_data()
            st.success("Gerät aktualisiert")

    st.subheader("Geräteliste")
    devices = queries.find_devices()
    for device in devices:
        st.write(f"Name: {device['device_name']}, Verantwortlicher: {device['managed_by_user_id']}, Status: {device['status']}")


elif menu == "Reservierungen":
    st.header("Reservierungssystem")

    users = queries.find_users()
    devices = queries.find_devices()

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


