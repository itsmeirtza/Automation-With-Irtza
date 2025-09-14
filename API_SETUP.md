# 🔑 YouTube API Setup - Automation With Irtza

**Created by: Irtza Ali Waris**  
**Email:** Irtzaaliwaris@gmail.com  
**Website:** https://ialiwaris.com

## ✅ **Current Configuration**

Your API is already configured with:
- **Client ID:** `34536726114-fkiahglk2fpkj0g4q2l450kmu6i1uovh.apps.googleusercontent.com`
- **Project:** `automation-with-irtza`

## ⚠️ **Important: Complete API Setup Required**

The `client_secret.json` file has been created with your Client ID, but you still need to:

### 1. Get the Real Client Secret
Go to [Google Cloud Console](https://console.developers.google.com):
1. Select your project with Client ID: `34536726114-fkiahglk2fpkj0g4q2l450kmu6i1uovh`
2. Go to **APIs & Services** → **Credentials**
3. Find your OAuth 2.0 Client ID
4. Download the JSON file
5. Replace the current `client_secret.json` with the downloaded file

### 2. Enable Required APIs
In Google Cloud Console, enable:
- **YouTube Data API v3**
- **YouTube Analytics API** (optional)

### 3. Configure OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Add your app name: `Automation With Irtza`
3. Add your email: `Irtzaaliwaris@gmail.com`
4. Add scopes: `https://www.googleapis.com/auth/youtube.upload`

### 4. Set Authorized Redirect URIs
In your OAuth client configuration, add:
- `http://localhost`
- `http://localhost:8080`
- `urn:ietf:wg:oauth:2.0:oob`

## 📋 **Current client_secret.json Structure**

```json
{
  "installed": {
    "client_id": "34536726114-fkiahglk2fpkj0g4q2l450kmu6i1uovh.apps.googleusercontent.com",
    "project_id": "automation-with-irtza",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-automation-irtza-secret",
    "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"]
  }
}
```

## 🔧 **How to Test API Connection**

1. Run the application:
   ```bash
   python run.py
   ```

2. Go to the workflow and try to process a video

3. On first run, it will open browser for OAuth authorization

4. Grant permissions to your YouTube account

5. The app will create a `token.pkl` file for future authentications

## 🚀 **Features Enabled with This API**

- ✅ **Upload videos to YouTube**
- ✅ **Generate automatic titles and descriptions**
- ✅ **Add tags automatically**
- ✅ **Set video privacy (public/private/unlisted)**
- ✅ **Upload up to 6 videos per day (quota limits)**

## ⚡ **Quick Start**

1. Complete the API setup above
2. Run: `python run.py`
3. Open: `http://localhost:5000`
4. Enter your YouTube channel
5. Add a video URL to process
6. Let AI create clips
7. Upload to YouTube automatically!

## 📊 **API Quotas & Limits**

- **Daily Upload Limit:** 6 videos (YouTube API quota)
- **Video Size Limit:** 128GB or 12 hours
- **API Calls per Day:** 10,000 (standard quota)

## 🔒 **Security Notes**

- Never share your `client_secret.json` file
- Keep your `token.pkl` file secure
- The Client ID is already configured and safe to use
- Your videos are uploaded to your own YouTube account

---

**Ready to automate! Your API is configured and ready for video uploads! 🎉**