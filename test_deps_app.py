import pandas as pd
import requests
import streamlit as st
from google.oauth2 import service_account
import google.auth.transport.requests as google_auth_requests

st.set_page_config(page_title="Test Dependencies", page_icon="🧪", layout="wide")

st.title("🧪 Test Dependencies")
st.write("Nếu thấy được bảng dưới đây, nghĩa là pandas + google-auth + requests đều import/chạy OK.")

# Test pandas + st.dataframe (giống hệt cách stats tab của app thật dùng)
df = pd.DataFrame({
    "Tên nhóm": ["Công ty A", "Công ty B", "Công ty C"],
    "Tổng số": [5, 3, 8],
    "Pending": [2, 1, 4],
    "Fixed": [3, 2, 4],
})
st.dataframe(df, width='stretch')
st.bar_chart(df.set_index("Tên nhóm")["Tổng số"])

st.success("✅ Test xong, không có gì crash cả!")

st.write("---")
st.write("Test tạo credentials object (chưa gọi mạng thật):")
try:
    fake_info = {
        "type": "service_account",
        "project_id": "test",
        "private_key_id": "test",
        "private_key": "-----BEGIN PRIVATE KEY-----\ntest\n-----END PRIVATE KEY-----\n",
        "client_email": "test@test.iam.gserviceaccount.com",
        "client_id": "123",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    creds = service_account.Credentials.from_service_account_info(
        fake_info, scopes=["https://www.googleapis.com/auth/firebase.database"]
    )
    st.write("✅ Tạo credentials object OK (chưa refresh/gọi mạng)")
except Exception as e:
    st.write(f"Lỗi khi tạo credentials (không phải crash, chỉ là exception bình thường): {e}")
