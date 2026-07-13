import requests
import streamlit as st
from google.oauth2 import service_account
import google.auth.transport.requests as google_auth_requests

st.set_page_config(page_title="Test Firebase thật", page_icon="🧪", layout="wide")
st.title("🧪 Test kết nối Firebase thật")

missing = [k for k in ("firebase_database_url", "firebase_service_account") if k not in st.secrets]
if missing:
    st.error(f"Thiếu Secrets: {missing}. Dán lại đúng secrets như app chính (app_password không bắt buộc cho test này).")
    st.stop()

st.write("Bước 1: Tạo credentials object từ service account thật...")
try:
    info = dict(st.secrets["firebase_service_account"])
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/firebase.database",
                      "https://www.googleapis.com/auth/userinfo.email"]
    )
    st.success("✅ Tạo credentials OK")
except Exception as e:
    st.error(f"Lỗi tạo credentials: {e}")
    st.stop()

st.write("Bước 2: Ký JWT + gọi mạng thật để lấy access token...")
try:
    creds.refresh(google_auth_requests.Request())
    st.success(f"✅ Lấy access token OK (dài {len(creds.token)} ký tự)")
except Exception as e:
    st.error(f"Lỗi lấy access token: {e}")
    st.stop()

st.write("Bước 3: Gọi REST API thật để đọc dữ liệu Firebase...")
try:
    base = st.secrets["firebase_database_url"].rstrip("/")
    resp = requests.get(f"{base}/issue_follow/customers.json",
                         headers={"Authorization": f"Bearer {creds.token}"}, timeout=10)
    resp.raise_for_status()
    data = resp.json() or {}
    st.success(f"✅ Đọc Firebase OK — có {len(data)} khách hàng")
    st.json(data)
except Exception as e:
    st.error(f"Lỗi gọi Firebase REST: {e}")
    st.stop()

st.write("---")
st.success("✅✅✅ Nếu thấy dòng này, TOÀN BỘ luồng Firebase thật chạy OK, không crash!")
