import streamlit as st
from db import (
    init_db,
    add_program,
    get_all_programs,
    get_program_by_id,
    update_program,
    delete_program,
    get_programs_by_subject
)

# ==================== INITIAL SETUP ====================
st.set_page_config(page_title="CodeZoro", page_icon="💻", layout="wide")
init_db()

# ==================== SIDEBAR ====================
st.sidebar.title(" CodeZoro ⚔")
menu = st.sidebar.radio("Navigate", ["Home", "➕ Add Program", "Edit/Delete"])

# ==================== HOME PAGE ====================
if menu == "Home":
    st.title(" My Lab Programs")

    subjects = ["DWDM", "ML"]   # 🔸 Can make dynamic later

    for subject in subjects:
        st.markdown(f"## {subject}")
        programs = get_programs_by_subject(subject)

        if not programs:
            st.info(f"No programs added yet for **{subject}**")
            continue

        # Collect lab numbers for this subject
        lab_numbers = sorted({p['lab_number'] for p in programs})

        # Create horizontal tabs for each lab
        lab_tabs = st.tabs([f"Lab {num}" for num in lab_numbers])

        # Render each Lab tab
        for idx, lab_num in enumerate(lab_numbers):
            with lab_tabs[idx]:
                # Filter programs of this lab
                lab_programs = [p for p in programs if p['lab_number'] == lab_num]

                for prog in lab_programs:
                    st.subheader(prog['title'])
                    if prog['description']:
                        st.write(prog['description'])
                    st.code(prog['code'], language='python')

# ==================== ADD PROGRAM PAGE ====================
elif menu == "➕ Add Program":
    st.title("➕ Add New Program")
    with st.form("add_form"):
        title = st.text_input("Program Title")
        subject = st.selectbox("Subject", ["ML", "DWDM"])
        lab_number = st.number_input("Lab Number", min_value=1, step=1)
        description = st.text_area("Description")
        code = st.text_area("Code", height=200)
        submitted = st.form_submit_button("💾 Save Program")

        if submitted:
            if title and code.strip():
               # Corrected order
                add_program(subject, lab_number, title, description, code)

                st.success("✅ Program added successfully!")
            else:
                st.error("⚠️ Title and Code are required fields.")

# ==================== EDIT / DELETE PAGE ====================
elif menu == "Edit/Delete":
    st.title("🛠 Manage Programs")
    programs = get_all_programs()

    if not programs:
        st.info("No programs found.")
    else:
        # Dropdown to select program
        prog_list = {
            f"{p['title']} ({p['subject']} - Lab {p['lab_number']})": p['id']
            for p in programs
        }
        selected = st.selectbox("Select a Program to Edit/Delete", list(prog_list.keys()))
        prog_id = prog_list[selected]
        prog_data = get_program_by_id(prog_id)

        # Edit/Delete form
        with st.form("edit_form"):
            new_title = st.text_input("Title", value=prog_data['title'])

            new_subject = st.selectbox(
                "Subject",
                ["ML", "DWDM"],
                index=0 if prog_data['subject'] == "ML" else 1
            )

            # Convert lab_number to int for number_input
            lab_val = int(prog_data['lab_number']) if str(prog_data['lab_number']).isdigit() else 1
            new_lab = st.number_input("Lab Number", min_value=1, step=1, value=lab_val)

            new_description = st.text_area("Description", value=prog_data['description'])
            new_code = st.text_area("Code", value=prog_data['code'], height=200)

            col1, col2 = st.columns(2)
            with col1:
                save_btn = st.form_submit_button("💾 Update Program")
            with col2:
                delete_btn = st.form_submit_button("🗑 Delete Program")

        if save_btn:
            update_program(prog_id, new_title, new_subject, new_lab, new_description, new_code)
            st.success("✅ Program updated successfully!")
            st.experimental_rerun()

        if delete_btn:
            delete_program(prog_id)
            st.warning("⚠️ Program deleted.")
            st.experimental_rerun()
