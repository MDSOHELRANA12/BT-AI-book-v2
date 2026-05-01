import streamlit as st
from supabase import create_client
import uuid
import random
import os

# ১. সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# ২. পেজ সেটআপ (সবার আগে থাকতে হবে)
st.set_page_config(page_title="BT AI book", layout="wide")

# ৩. ফরম্যাট ফাংশন
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# ৪. ডিজাইন ও স্টাইল (আপনার অরিজিনাল কাঠামো)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .btn-reward { display: block; width: 100%; padding: 12px; margin: 10px 0; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# ৫. মেইন অ্যাপ ফাংশন
def main():
    st.title("🛡️ BT AI book")

    if 'user' not in st.session_state:
        st.session_state.user = None
        st.session_state.pic = None

    # লগইন সিস্টেম
    if not st.session_state.user:
        st.sidebar.header("🔐 User Login")
        u_name = st.sidebar.text_input("Enter Registered Name")
        if u_name and st.sidebar.button("Login"):
            user_data = supabase.table("users").select("*").eq("username", u_name).execute()
            if user_data.data:
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
    else:
        st.sidebar.image(st.session_state.pic, width=100)
        st.sidebar.success(f"Profile: {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()

    tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

    if tab == "🌍 World Feed":
        try:
            res = supabase.table("videos").select("*").execute()
            data = res.data if res.data else []
            random.shuffle(data)
            for index, v in enumerate(data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><span class="username-text">{v.get("uploader_name", "BT User")}</span></div>', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.markdown(f'<span class="stat-box">👁️ {format_value(v.get("views", 0))} Views</span>', unsafe_allow_html=True)
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Diamond Reward</a>', unsafe_allow_html=True)
                st.components.v1.html("""<script type="text/javascript">atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>""", height=65)
                st.markdown('</div>', unsafe_allow_html=True)
        except: st.error("Syncing Feed...")

    elif tab == "📤 Upload Video":
        if st.session_state.user:
            v_file = st.file_uploader("Select MP4", type=['mp4'])
            if st.button("🚀 Publish") and v_file:
                with st.spinner("Publishing..."):
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=v_uuid, file=v_file.getvalue())
                    v_url = supabase.storage.from_("videos").get_public_url(v_uuid)
                    supabase.table("videos").insert({"video_url": v_url, "uploader_name": st.session_state.user, "uploader_pic": st.session_state.pic, "likes": 0, "followers": 0, "views": 0}).execute()
                    st.success("✅ সোহেল ভাই, ভিডিও লাইভ হয়েছে!")

# ৬. ভারসেল হ্যান্ডলার (এটিই আসল সমাধান)
app = main

if __name__ == "__main__":
    main()
