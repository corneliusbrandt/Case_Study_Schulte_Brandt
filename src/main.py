import streamlit as st
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import users as users
import devices as devices
import queries as queries
import reservations as reservations



st.title("Geräte- und Reservierungsmanager")

menu = st.sidebar.radio("Menü", ["Benutzer", "Geräte", "Reservierungen", "Wartungsmanager"])

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
        users_list = users.User.find_all()
        user_id = st.selectbox("Benutzer auswählen", [user.email for user in users_list], format_func=lambda x: next(u.name for u in users_list if u.email == x))
        user = next((u for u in users_list if u.email == user_id), None)
        if user is None:
            st.error("Benutzer nicht gefunden")
            st.stop()

        #user.name = st.text_input("Name", value=user.name)
        user.email = st.text_input("Email", value=user.email)

        if st.button("Benutzer aktualisieren"):
            #user_manager.table.update({'name': name, 'email': email}, doc_ids=[user_id])
            user.store_data()
            st.rerun()
            st.success("Benutzer aktualisiert")

        if st.button("Benutzer löschen"):
            user.delete()
            st.rerun()
            st.success("Benutzer gelöscht")
    
    users_for_userlist = queries.find_users()
    for user in users_for_userlist:
        st.write(f"Name: {user['name']}, Email: {user['email']}")

elif menu == "Geräte":
    st.header("Geräteverwaltung")
    action = st.radio("Aktion", ["Gerät hinzufügen", "Gerät bearbeiten"])

    if action == "Gerät hinzufügen":
        device_name = st.text_input("Gerätename")
        users_list = users.User.find_all()
        managed_by_user_id = st.selectbox("Verantwortlicher", [user.name for user in users_list])
        end_of_life = st.date_input("End of Life")
        maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1)
        maintenance_cost = st.number_input("Wartungskosten", min_value=0.0, step=0.01)
        status = st.selectbox("Status", ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"])

        if st.button("Gerät hinzufügen"):
            #device_manager.store_data()
            devices.Device(device_name=device_name, managed_by_user_id=managed_by_user_id, end_of_life=end_of_life, maintenance_interval=maintenance_interval, maintenance_cost=maintenance_cost, status=status).store_data()
            st.success("Gerät hinzugefügt")

        

    elif action == "Gerät bearbeiten":
        devices_list = devices.Device.find_all()
        device_id = st.selectbox("Gerät auswählen", [device.device_name for device in devices_list], format_func=lambda x: next(d.device_name for d in devices_list if d.device_name == x))
        device = next((d for d in devices_list if d.device_name == device_id), None)
        if device is None:
            st.error("Gerät nicht gefunden")
            st.stop()

        device.managed_by_user_id = st.text_input("Verantwortlicher", value=device.managed_by_user_id)
        device.end_of_life = st.date_input("End of Life", value=datetime.strptime(device.end_of_life, '%Y-%m-%d') if device.end_of_life else datetime.today()).strftime('%Y-%m-%d')
        device.maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=0, step=1, value=device.maintenance_interval)
        device.maintenance_cost = st.number_input("Wartungskosten", min_value=0.0, step=0.01, value=device.maintenance_cost)
        status_options = ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"]
        status_index = status_options.index(device.status) if device.status in status_options else 0
        device.status = st.selectbox("Status", status_options, index=status_index)

        if st.button("Gerät aktualisieren"):
            device.store_data()
            st.rerun()
            st.success("Gerät aktualisiert")

        if st.button("Gerät löschen"):
            device.delete()
            st.rerun()
            st.success("Gerät gelöscht")

    st.subheader("Geräteliste")
    devices_list = devices.Device.find_all()
    for device in devices_list:
        st.write(f"Name: {device.device_name}, Verantwortlicher: {device.managed_by_user_id}")


elif menu == "Reservierungen":
    st.header("Reservierungssystem")

    user_list_for_res = users.User.find_all()
    device_list_for_res = devices.Device.find_all()

    if not user_list_for_res or not device_list_for_res:
        st.warning("Bitte fügen Sie zuerst Benutzer und Geräte hinzu.")
    else:
        device_id = st.selectbox(
            "Gerät", 
            [device.device_name for device in device_list_for_res], 
        )
        
        user_id = st.selectbox(
            "Benutzer", 
            [user.name for user in user_list_for_res], 
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
            if reservations.Reservation.find_by_attribute("res_device_id", device_id):
                st.warning("Gerät bereits reserviert. Sie können die bestehende Reservierung ändern oder löschen.")
            if st.button("Reservieren"):
                reservations.Reservation(device_id, user_id, start_datetime, end_datetime).store_data()
                st.success("Gerät reserviert")
            if st.button("Reservierung löschen"):
                reservations.Reservation.find_by_attribute("res_device_id", device_id).delete()
                st.success("Reservierung gelöscht")

    st.subheader("Reservierungsliste")
    reservation_list = reservations.Reservation.find_all()
    if reservation_list:
        for res in reservation_list:
            st.write(f"Reserviertes Gerät: {res.res_device_id}, Verantwortlicher: {res.res_user_id}, Start: {res.res_start_date}, Ende: {res.res_end_date}")
    else:
        st.write("Keine Reservierungen vorhanden")

elif menu == "Wartungsmanager":
    st.header("Wartungsmanager")

    devices_list = devices.Device.find_all()
    maintenance_list = devices.Device.find_maintenance()
    maintenance_cost_next = devices.Device.update_maintenance()
    st.write(f"Kosten für die nächsten Wartungen: {maintenance_cost_next}")

    

    maintenance_id = st.selectbox("Gerät auswählen", [device.device_name for device in devices_list], format_func=lambda x: next(d.device_name for d in devices_list if d.device_name == x))
    device = next((d for d in maintenance_list if d.device_name == maintenance_id), None)
    device.status = st.selectbox("Status", ["Einsatzbereit", "Wartung", "Fehlerhaft", "Außerbetrieb"])
    device.maintenance_last = st.date_input("Last Maintenance", value=datetime.strptime(device.maintenance_last, '%Y-%m-%d') if device.maintenance_last else datetime.today()).strftime('%Y-%m-%d')
    gewartet = st.selectbox("Wartung durchgeführt", ["Ja", "Nein"])
    if st.button("Wartungsstatus aktualisieren"):
            if gewartet:
                device.maintenance_next = datetime.strptime(device.maintenance_last, '%Y-%m-%d') + timedelta(days=device.maintenance_interval)
                device.status = "Einsatzbereit"
            device.store_data()
            st.rerun()
            st.success("Wartungsstatus aktualisiert")

    if maintenance_list:
        for maintenance in maintenance_list:
            print(maintenance.maintenance_cost)
            print(maintenance.maintenance_next)
            st.write(f"Gerät: {maintenance.device_name}, Nächste Wartung: {maintenance.maintenance_next}, Wartungskosten: {maintenance.maintenance_cost}, Status: {maintenance.status}")
    else:
        st.write("Keine Wartungen anstehend")

