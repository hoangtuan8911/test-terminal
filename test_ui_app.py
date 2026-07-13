from datetime import date

import streamlit as st

st.set_page_config(page_title="Test UI phức tạp", page_icon="🧪", layout="wide")

# ==== DỮ LIỆU GIẢ (thay cho Firebase) ====
FAKE_DB = {
    "cust1": {"name": "Công ty ABC", "issues": {
        "iss1": {"title": "Lỗi kẹt băng tải", "device": "Checkweigher C33", "serial": "SN-AAA",
                 "status": "Pending", "url": "", "steps": {
                     "s1": {"date": "01/07/2026", "activity": "Kiểm tra motor", "pic": "Tuấn",
                            "result": "OK", "lead_time": "20/07/2026"}}}}},
    "cust2": {"name": "Công ty XYZ", "issues": {
        "iss2": {"title": "Lỗi cân sai số", "device": "Máy X33", "serial": "SN-BBB",
                 "status": "Fixed", "url": "", "steps": {}}}},
}

if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = None
if "selected_issue_id" not in st.session_state:
    st.session_state.selected_issue_id = None

st.title("🧪 Test UI phức tạp (tabs, sidebar, form, rerun)")

# ==== SIDEBAR: danh sách khách hàng, nút bấm động trong vòng lặp ====
st.sidebar.header("Khách Hàng")
with st.sidebar.expander("🔍 Tìm / Thêm Khách Hàng"):
    typed = st.text_input("Nhập tên", key="search_input")
    if typed:
        st.button(f"+ Thêm Mới '{typed}'", key="add_btn")

for cid, c in FAKE_DB.items():
    is_selected = cid == st.session_state.selected_customer_id
    if st.sidebar.button(f"📁 {c['name']}", key=f"cust_btn_{cid}", width='stretch',
                          type="primary" if is_selected else "secondary"):
        st.session_state.selected_customer_id = cid
        st.session_state.selected_issue_id = None
        st.rerun()

# ==== TABS ====
tab1, tab2 = st.tabs(["📋 Quản lý Issues", "📊 Thống Kê"])

with tab1:
    cid = st.session_state.selected_customer_id
    if not cid:
        st.info("👈 Chọn 1 khách hàng ở sidebar.")
    else:
        customer = FAKE_DB[cid]
        st.subheader(f"📁 {customer['name']}")

        with st.expander("+ Thêm Issue mới"):
            st.text_input("Tiêu đề", key="new_title")
            st.selectbox("Thiết bị", options=["(Nhập mới...)", "Máy A", "Máy B"], key="new_dev")
            st.button("💾 Lưu Issue", key="save_issue_btn")

        issues = customer["issues"]
        for iid, issue in issues.items():
            is_sel = iid == st.session_state.selected_issue_id
            if st.button(f"🔹 {issue['title']} [{issue['status']}]", key=f"issue_btn_{iid}",
                         width='stretch', type="primary" if is_sel else "secondary"):
                st.session_state.selected_issue_id = iid
                st.rerun()

        if st.session_state.selected_issue_id in issues:
            iid = st.session_state.selected_issue_id
            issue = issues[iid]

            with st.expander("✏️ Sửa Issue"):
                st.text_input("Tiêu đề", value=issue["title"], key=f"edit_title_{iid}")
                st.selectbox("Trạng thái", options=["Pending", "Fixed"],
                             index=0 if issue["status"] == "Pending" else 1, key=f"edit_status_{iid}")

            st.markdown("##### Activities")
            with st.expander("+ Thêm Activity"):
                st.text_input("Tên hoạt động", key=f"act_name_{iid}")
                st.date_input("Ngày", value=date.today(), format="DD/MM/YYYY", key=f"act_date_{iid}")
                st.checkbox("Đóng issue", key=f"act_close_{iid}")
                st.button("💾 Lưu", key=f"save_act_{iid}")

            for sid, step in issue["steps"].items():
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
                    with c1:
                        st.markdown(f"**{step['date']}** — {step['activity']}")
                        st.caption(f"PIC: {step['pic']}")
                    with c2:
                        if st.button("✏️", key=f"edit_act_{sid}"):
                            st.session_state[f"editing_{sid}"] = not st.session_state.get(f"editing_{sid}", False)
                            st.rerun()
                    with c3:
                        st.button("🗑️", key=f"del_act_{sid}")
                    with c4:
                        st.button("⚡", key=f"export_{sid}")

                    if st.session_state.get(f"editing_{sid}"):
                        with st.form(key=f"edit_form_{sid}"):
                            st.text_input("Tên hoạt động", value=step["activity"])
                            st.date_input("Ngày", value=date.today(), format="DD/MM/YYYY")
                            st.form_submit_button("Cập nhật")

with tab2:
    st.write("Tab thống kê giả — không cần test lại pandas (đã confirm OK).")
    st.radio("Nhóm theo:", ["Khách hàng", "Issue"], horizontal=True)

st.write("---")
st.success("✅ Nếu thấy dòng này ở cuối trang, toàn bộ UI phức tạp đều chạy OK, không crash!")
