import streamlit as st
from google.oauth2 import service_account

st.set_page_config(page_title="Test Cache", page_icon="🧪", layout="wide")
st.title("🧪 Test @st.cache_resource")


@st.cache_resource
def get_fake_credentials():
    fake_info = {
        "type": "service_account",
        "project_id": "test",
        "private_key_id": "test",
        "private_key": "-----BEGIN PRIVATE KEY-----\ntest\n-----END PRIVATE KEY-----\n",
        "client_email": "test@test.iam.gserviceaccount.com",
        "client_id": "123",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    try:
        return service_account.Credentials.from_service_account_info(
            fake_info, scopes=["https://www.googleapis.com/auth/firebase.database"]
        )
    except Exception as e:
        return f"Lỗi tạo credentials (bình thường vì key giả): {e}"


st.write("Trước khi gọi hàm cache...")
result = get_fake_credentials()
st.write("Sau khi gọi hàm cache — không crash!")
st.write(result)

st.write("---")

# Test thêm: password gate y hệt app thật, dùng on_change callback
def password_entered():
    if st.session_state.get("password_input") == "test123":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False


st.text_input("Test ô nhập mật khẩu (on_change callback)", type="password",
              key="password_input", on_change=password_entered)
st.write("Nếu thấy dòng này, ô nhập với on_change cũng không crash!")
