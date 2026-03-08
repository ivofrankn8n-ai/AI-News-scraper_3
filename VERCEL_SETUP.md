# Vercel Deployment Configuration

## Environment Variables Setup

### 1. Configure Vercel Environment Variables
1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your "ai-news-scraper-3" project
3. Navigate to: **Settings** → **Environment Variables**
4. Add the following environment variables:

```
SUPABASE_URL=https://keajnbcsqgyfgyikvbca.supabase.co
SUPABASE_ANON_KEY=sb_publishable_tUM51WsQtzlmiiLABjCnBw_N3HeE0ay
```

### 2. Deployment Settings
1. Ensure your project is configured as a **Static Site**
2. The `vercel.json` file should be configured correctly
3. No build command needed (static HTML deployment)

### 3. Deploy the Updated Code
1. Push your changes to GitHub
2. Vercel will automatically deploy from your repository
3. Monitor the deployment logs for any errors

## Testing the Deployment

### 1. Test Supabase Connection
1. Visit: https://ai-news-scraper-3.vercel.app/test-supabase.html
2. This test page will verify Supabase connectivity
3. Check browser console for connection details

### 2. Test Main Dashboard
1. Visit: https://ai-news-scraper-3.vercel.app
2. The dashboard should load without React minification errors
3. Articles should load from Supabase
4. Check browser console for any remaining errors

## Expected Behavior After Fixes

### ✅ Should Work:
- Dashboard loads without React errors
- Articles display from Supabase database
- "Today" count shows only today's articles
- Refresh button shows "Searching Articles" status
- Last Updated timestamp only changes on refresh
- Search and filter functionality works

### ❌ Common Issues to Check:
- CORS errors in browser console
- Supabase connection failures
- JavaScript syntax errors
- Missing environment variables

## Troubleshooting

### If Articles Don't Load:
1. Check Supabase CORS configuration (see SUPABASE_CORS_SETUP.md)
2. Verify environment variables in Vercel dashboard
3. Check browser console for specific error messages

### If React Errors Persist:
1. Ensure `vercel.json` is configured correctly
2. Verify no API routing conflicts exist
3. Check that all JavaScript syntax is correct

## Final Verification Checklist

- [ ] Supabase CORS configured for Vercel domain
- [ ] Vercel environment variables set
- [ ] Dashboard loads without React errors
- [ ] Articles display from Supabase
- [ ] Today count filters correctly
- [ ] Refresh functionality works
- [ ] Search and filter functions work