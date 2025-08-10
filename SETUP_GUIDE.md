# 🎵 Folk Festival Voting App - Setup Guide

## 🚨 The Problem (Fixed!)
Your Streamlit app was losing data because:
- **Local storage**: Gets wiped when Streamlit containers restart
- **Session state**: Only persists per browser session, not shared across devices
- **Google Sheets**: The original implementation had broken API calls

## ✅ The Solution: JSONBin.io
JSONBin.io is a free, reliable JSON storage service that provides:
- **Persistent storage** that survives container restarts
- **Cross-device sync** - all users see the same data instantly
- **Real-time updates** - no complex database setup required
- **Free tier** - perfect for small voting apps

## 🛠️ Setup Steps

### Step 1: Create JSONBin.io Account
1. Go to [https://jsonbin.io](https://jsonbin.io)
2. Sign up for a free account
3. Get your **API Key** from your dashboard

### Step 2: Create a Bin
1. In your JSONBin.io dashboard, click "Create Bin"
2. Name it something like "folk-festival-voting"
3. Add this initial JSON structure:
```json
{
  "nominations": {},
  "nominators": [],
  "write_in_candidates": [],
  "nomination_reasons": {}
}
```
4. Copy the **Bin ID** from the URL (it looks like: `abc123def456`)

### Step 3: Configure Streamlit Secrets
1. In your Streamlit app directory, create a `.streamlit/secrets.toml` file:
```toml
[jsonbin]
api_key = "your_jsonbin_api_key_here"
bin_id = "your_bin_id_here"
```

2. **For Streamlit Community Cloud deployment:**
   - Go to your app settings in Streamlit Cloud
   - Add these secrets in the "Secrets" section:
   ```toml
   [jsonbin]
   api_key = "your_jsonbin_api_key_here"
   bin_id = "your_bin_id_here"
   ```

### Step 4: Update Your Code
The code has already been updated with the new `load_data()` and `save_data()` functions that use JSONBin.io.

## 🔧 How It Works

### Data Flow:
1. **User votes** → Data saved to JSONBin.io via API
2. **Any device loads app** → Data loaded from JSONBin.io
3. **Container restarts** → Data survives because it's stored externally
4. **Multiple users** → All see the same data instantly

### Key Functions:
- `load_data()`: Fetches current data from JSONBin.io
- `save_data()`: Saves updated data to JSONBin.io
- **Fallback**: If JSONBin.io is unavailable, falls back to session state

## 🧪 Testing

### Local Testing:
1. Set up your secrets in `.streamlit/secrets.toml`
2. Run: `streamlit run streamlit_folk_festival.py`
3. Vote on one browser/device
4. Open the same URL on another device
5. **Verify**: Votes appear on both devices instantly

### Production Testing:
1. Deploy to Streamlit Community Cloud
2. Test cross-device voting
3. **Verify**: Data persists after container restarts

## 🎯 Why This Solution Works

### ✅ Solves All Your Problems:
- **Persistent**: Data stored externally, survives restarts
- **Shared**: All devices see the same data
- **Real-time**: Updates appear immediately
- **Simple**: No complex database setup
- **Free**: JSONBin.io free tier is sufficient

### 🔄 Data Sync Process:
1. App loads → `load_data()` fetches from JSONBin.io
2. User votes → `save_data()` updates JSONBin.io
3. Other users refresh → See updated data immediately
4. Container restarts → Data reloaded from JSONBin.io

## 🚀 Alternative Solutions

If JSONBin.io doesn't work for you, here are other free options:

### Option 1: Pastebin API
```python
# Similar setup, different API endpoints
PASTEBIN_API_KEY = st.secrets.get("pastebin_api_key", "")
```

### Option 2: GitHub Gist
```python
# Store data as a GitHub Gist
GITHUB_TOKEN = st.secrets.get("github_token", "")
```

### Option 3: Firebase Realtime Database
```python
# More robust but requires Firebase setup
FIREBASE_CONFIG = st.secrets.get("firebase_config", "")
```

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Votes appear on all devices instantly
- ✅ Data survives page refreshes
- ✅ Data survives container restarts
- ✅ Multiple users can vote simultaneously
- ✅ No more "lost votes" complaints

## 🆘 Troubleshooting

### Common Issues:

**"Could not load data from storage"**
- Check your API key and bin ID are correct
- Verify JSONBin.io is accessible
- Check your internet connection

**"Failed to save data"**
- Ensure your API key has write permissions
- Check the bin ID is correct
- Verify the JSON structure is valid

**Data not syncing across devices**
- Make sure both devices are using the same app URL
- Check that secrets are configured correctly
- Verify JSONBin.io service is working

### Debug Mode:
Add this to your app for debugging:
```python
if st.checkbox("Debug mode"):
    st.write("API Key:", JSONBIN_API_KEY[:10] + "..." if JSONBIN_API_KEY else "Not set")
    st.write("Bin ID:", JSONBIN_BIN_ID if JSONBIN_BIN_ID else "Not set")
    st.write("Current data:", st.session_state.nominations)
```

## 🎊 You're All Set!

Your voting app will now:
- **Persist data** across all devices and container restarts
- **Sync in real-time** so everyone sees the same votes
- **Work reliably** on Streamlit Community Cloud
- **Handle multiple users** voting simultaneously

The folk festival early infiltration team selection will now be properly democratic! 🏕️🎵 
