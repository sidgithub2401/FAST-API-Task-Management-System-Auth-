import streamlit as st
import requests

API_URL = "https://fast-api-task-management-backend.onrender.com"

st.set_page_config(page_title="Task Manager", page_icon="✅", layout="centered")

# ── helpers ──────────────────────────────────────────────────────
def auth_headers():
    return {"Authorization": f"Bearer {st.session_state['token']}"}


def logout():
    for key in ["token", "user_email", "user_name", "user_username"]:
        st.session_state.pop(key, None)
    st.rerun()


# ── AUTH PAGE (login / register) ─────────────────────────────────
def auth_page():
    st.title("✅ Task Manager")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            submitted = st.form_submit_button("Login")
        if submitted:
            if not email or not password:
                st.warning("Please fill in all fields.")
            else:
                try:
                    resp = requests.post(
                        f"{API_URL}/users/login",
                        json={"email": email, "password": password},
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state["token"] = data["token"]
                        st.session_state["user_email"] = email
                        st.success(data.get("message", "Login successful!"))
                        st.rerun()
                    else:
                        detail = resp.json().get("detail", "Login failed.")
                        st.error(detail)
                except requests.ConnectionError:
                    st.error("Cannot reach the API server. Make sure it is running.")

    with tab_register:
        with st.form("register_form"):
            name = st.text_input("Name", key="reg_name")
            username = st.text_input("Username", key="reg_user")
            email_r = st.text_input("Email", key="reg_email")
            password_r = st.text_input("Password", type="password", key="reg_pass")
            submitted_r = st.form_submit_button("Register")
        if submitted_r:
            if not all([name, username, email_r, password_r]):
                st.warning("Please fill in all fields.")
            else:
                try:
                    resp = requests.post(
                        f"{API_URL}/users/create_user",
                        json={
                            "name": name,
                            "username": username,
                            "email": email_r,
                            "password": password_r,
                        },
                        timeout=10,
                    )
                    if resp.status_code == 201:
                        st.success("Registration successful! You can now login.")
                    else:
                        detail = resp.json().get("detail", "Registration failed.")
                        st.error(detail)
                except requests.ConnectionError:
                    st.error("Cannot reach the API server. Make sure it is running.")


# ── TASKS PAGE ───────────────────────────────────────────────────
def tasks_page():
    st.header("📋 My Tasks")

    # ---- Create task expander ----
    with st.expander("➕ Create New Task", expanded=False):
        with st.form("create_task_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            is_completed = st.checkbox("Completed")
            create_btn = st.form_submit_button("Create Task")
        if create_btn:
            if not title or not description:
                st.warning("Title and description are required.")
            else:
                try:
                    resp = requests.post(
                        f"{API_URL}/tasks/create_tasks",
                        json={
                            "title": title,
                            "description": description,
                            "is_completed": is_completed,
                        },
                        headers=auth_headers(),
                        timeout=10,
                    )
                    if resp.status_code == 201:
                        st.success("Task created!")
                        st.rerun()
                    else:
                        detail = resp.json().get("detail", "Failed to create task.")
                        st.error(detail)
                except requests.ConnectionError:
                    st.error("Cannot reach the API server.")

    st.divider()

    # ---- Fetch and display tasks ----
    try:
        resp = requests.get(
            f"{API_URL}/tasks/tasks", headers=auth_headers(), timeout=10
        )
    except requests.ConnectionError:
        st.error("Cannot reach the API server.")
        return

    if resp.status_code != 200:
        detail = resp.json().get("detail", "Failed to fetch tasks.")
        st.error(detail)
        return

    tasks = resp.json()

    if not tasks:
        st.info("You have no tasks yet. Create one above!")
        return

    for task in tasks:
        tid = task["id"]
        status_icon = "✅" if task["is_completed"] else "⬜"

        with st.container(border=True):
            col1, col2, col3 = st.columns([6, 1, 1])
            with col1:
                st.markdown(
                    f"**{status_icon} {task['title']}**  \n{task['description']}"
                )
            with col2:
                if st.button("✏️", key=f"edit_{tid}", help="Edit task"):
                    st.session_state["editing_task"] = tid
            with col3:
                if st.button("🗑️", key=f"del_{tid}", help="Delete task"):
                    try:
                        r = requests.delete(
                            f"{API_URL}/tasks/delete_tasks/{tid}",
                            headers=auth_headers(),
                            timeout=10,
                        )
                        if r.status_code == 200:
                            st.success("Task deleted!")
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Delete failed."))
                    except requests.ConnectionError:
                        st.error("Cannot reach the API server.")

            # ---- Inline edit form ----
            if st.session_state.get("editing_task") == tid:
                with st.form(f"edit_form_{tid}"):
                    new_title = st.text_input("Title", value=task["title"])
                    new_desc = st.text_area("Description", value=task["description"])
                    new_status = st.checkbox(
                        "Completed", value=task["is_completed"]
                    )
                    col_save, col_cancel = st.columns(2)
                    save_btn = col_save.form_submit_button("Save")
                    cancel_btn = col_cancel.form_submit_button("Cancel")
                if save_btn:
                    try:
                        r = requests.put(
                            f"{API_URL}/tasks/update_tasks/{tid}",
                            json={
                                "title": new_title,
                                "description": new_desc,
                                "is_completed": new_status,
                            },
                            headers=auth_headers(),
                            timeout=10,
                        )
                        if r.status_code == 200:
                            st.success("Task updated!")
                            st.session_state.pop("editing_task", None)
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Update failed."))
                    except requests.ConnectionError:
                        st.error("Cannot reach the API server.")
                if cancel_btn:
                    st.session_state.pop("editing_task", None)
                    st.rerun()


# ── PROFILE PAGE ─────────────────────────────────────────────────
def profile_page():
    st.header("👤 My Profile")

    # ---- Edit details ----
    st.subheader("Edit Details")
    with st.form("edit_profile_form"):
        name = st.text_input("Name", value=st.session_state.get("user_name", ""))
        username = st.text_input(
            "Username", value=st.session_state.get("user_username", "")
        )
        email = st.text_input(
            "Email", value=st.session_state.get("user_email", ""), disabled=True
        )
        password = st.text_input("New Password", type="password")
        update_btn = st.form_submit_button("Update Profile")

    if update_btn:
        if not all([name, username, password]):
            st.warning("Please fill in all fields (including new password).")
        else:
            try:
                resp = requests.put(
                    f"{API_URL}/users/update_user",
                    json={
                        "name": name,
                        "username": username,
                        "email": st.session_state["user_email"],
                        "password": password,
                    },
                    headers=auth_headers(),
                    timeout=10,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state["user_name"] = data["name"]
                    st.session_state["user_username"] = data["username"]
                    st.success("Profile updated! Please login again with new password.")
                else:
                    detail = resp.json().get("detail", "Update failed.")
                    st.error(detail)
            except requests.ConnectionError:
                st.error("Cannot reach the API server.")

    st.divider()

    # ---- Delete account ----
    st.subheader("⚠️ Danger Zone")
    with st.form("delete_account_form"):
        st.warning("This action is irreversible. All your tasks will also be deleted.")
        confirm_email = st.text_input(
            "Type your email to confirm deletion", key="confirm_del_email"
        )
        delete_btn = st.form_submit_button("Delete My Account", type="primary")

    if delete_btn:
        if confirm_email != st.session_state.get("user_email"):
            st.error("Email does not match. Account NOT deleted.")
        else:
            try:
                resp = requests.delete(
                    f"{API_URL}/users/delete_user",
                    json={"email": confirm_email},
                    headers=auth_headers(),
                    timeout=10,
                )
                if resp.status_code == 200:
                    st.success("Account deleted.")
                    logout()
                else:
                    detail = resp.json().get("detail", "Deletion failed.")
                    st.error(detail)
            except requests.ConnectionError:
                st.error("Cannot reach the API server.")


# ── MAIN ENTRYPOINT ──────────────────────────────────────────────
def main():
    if "token" not in st.session_state:
        auth_page()
        return

    # Sidebar navigation
    with st.sidebar:
        st.title("✅ Task Manager")
        st.caption(f"Logged in as **{st.session_state.get('user_email', '')}**")
        page = st.radio("Navigate", ["Tasks", "Profile"], label_visibility="collapsed")
        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()

    if page == "Tasks":
        tasks_page()
    elif page == "Profile":
        profile_page()


if __name__ == "__main__":
    main()
