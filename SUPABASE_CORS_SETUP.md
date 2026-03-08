# Supabase CORS Configuration for Vercel Deployment

## Steps to Configure CORS for Your AI News Dashboard

### 1. Access Your Supabase Dashboard
1. Go to: https://supabase.com/dashboard/project/keajnbcsqgyfgyikvbca
2. Sign in with your Supabase account

### 2. Configure Authentication Settings
1. Navigate to: **Authentication** → **Settings** → **URL Configuration**
2. Add your Vercel domain to "Additional Redirect URLs":
   ```
   https://ai-news-scraper-3.vercel.app
   ```
3. Add your Vercel domain to "Site URL":
   ```
   https://ai-news-scraper-3.vercel.app
   ```
4. Add your Vercel domain to "Allowed Redirect URLs":
   ```
   https://ai-news-scraper-3.vercel.app/*
   ```

### 3. Configure CORS for API Access
1. Navigate to: **Settings** → **API**
2. In the "CORS" section, add your Vercel domain:
   ```
   https://ai-news-scraper-3.vercel.app
   ```
3. Save the configuration

### 4. Verify Configuration
After saving, your Supabase project should:
- Allow requests from `https://ai-news-scraper-3.vercel.app`
- Accept the publishable key authentication
- Serve articles data to your dashboard

### 5. Test the Configuration
1. Deploy your updated dashboard to Vercel
2. Visit: https://ai-news-scraper-3.vercel.app
3. Check browser console for any CORS errors
4. The dashboard should successfully load articles from Supabase

## Current Supabase Project Details
- **Project URL**: https://keajnbcsqgyfgyikvbca.supabase.co
- **Publishable Key**: sb_publishable_tUM51WsQtzlmiiLABjCnBw_N3HeE0ay
- **Vercel Domain**: https://ai-news-scraper-3.vercel.app

## Notes
- The RLS (Row Level Security) policy "Allow anonymous access" is already configured
- This allows public read access to the articles table
- No authentication is required for reading articles, which is perfect for your dashboard