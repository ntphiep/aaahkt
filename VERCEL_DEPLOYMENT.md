# Vercel Deployment Instructions

This guide provides step-by-step instructions for deploying the AWS DevOps Pipeline dashboard to Vercel.

## Prerequisites

- Vercel account (sign up at [vercel.com](https://vercel.com))
- GitHub repository access
- Vercel CLI installed (optional)

## Method 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Connect GitHub Repository

1. Log in to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository: `ntphiep/aaahkt`
4. Authorize Vercel to access the repository

### Step 2: Configure Build Settings

Vercel should auto-detect Next.js. Configure these settings:

**Framework Preset:** Next.js

**Root Directory:** `dashboard`

**Build Command:** `npm run build`

**Output Directory:** `.next` (auto-detected)

**Install Command:** `npm install`

### Step 3: Set Environment Variables

Add the following environment variable in Vercel:

| Name | Value | Description |
|------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://your-api-url.com` | Your backend API URL |

**How to add:**
1. Go to Project Settings → Environment Variables
2. Add the variable for Production, Preview, and Development
3. Click "Save"

### Step 4: Deploy

1. Click "Deploy"
2. Wait for the build to complete (usually 1-2 minutes)
3. Your dashboard will be live at `https://your-project.vercel.app`

### Step 5: Configure Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed by Vercel
4. SSL certificate will be provisioned automatically

## Method 2: Deploy via Vercel CLI

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy from Dashboard Directory

```bash
cd dashboard
vercel
```

Follow the prompts:
- Set up and deploy: Yes
- Which scope: Choose your account/team
- Link to existing project: No (for first deploy)
- What's your project's name: aws-devops-dashboard
- In which directory is your code located: ./

### Step 4: Set Environment Variables

```bash
vercel env add NEXT_PUBLIC_API_URL production
# Enter your backend API URL when prompted
```

### Step 5: Deploy to Production

```bash
vercel --prod
```

## Method 3: Deploy via GitHub Integration (Automatic)

### Step 1: Connect Repository

1. In Vercel Dashboard, click "Add New..." → "Project"
2. Select your GitHub repository
3. Configure as described in Method 1

### Step 2: Enable Automatic Deployments

Vercel automatically deploys:
- **Production**: When you push to `main` branch
- **Preview**: When you create/update a pull request

### Step 3: Configure Build Settings

Ensure `vercel.json` in project root is configured:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "dashboard/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "dashboard/$1"
    }
  ]
}
```

## Post-Deployment Verification

### 1. Check Deployment Status

Visit your deployment URL and verify:
- ✅ Dashboard loads without errors
- ✅ API connection status shows (check top of dashboard)
- ✅ No console errors in browser DevTools
- ✅ Responsive design works on mobile

### 2. Test API Connection

```bash
# From browser console
fetch(process.env.NEXT_PUBLIC_API_URL + '/health')
  .then(r => r.json())
  .then(console.log)
```

Expected response:
```json
{"status": "healthy"}
```

### 3. Monitor Performance

1. Go to Vercel Dashboard → Analytics
2. Check page load times
3. Monitor Core Web Vitals
4. Review error logs if any

## Troubleshooting

### Build Fails

**Error: Cannot find module 'next'**
- Ensure `package.json` is in `dashboard/` directory
- Check Vercel root directory is set to `dashboard`

**Error: Build exceeded time limit**
- Optimize dependencies
- Check for circular dependencies
- Review build logs for specific errors

### Environment Variables Not Working

**API URL undefined**
- Ensure variable name starts with `NEXT_PUBLIC_`
- Redeploy after adding environment variables
- Check variable is set for correct environment (Production/Preview)

### Dashboard Shows But API Fails

**CORS Errors**
- Update backend API CORS settings to allow Vercel domain
- Add Vercel deployment URL to allowed origins

**Connection Timeout**
- Verify backend API is accessible from internet
- Check API URL is correct (https://, not http://)
- Ensure backend API is deployed and running

### 404 Not Found

- Verify root directory is set to `dashboard`
- Check `next.config.js` configuration
- Review Vercel build logs

## Production Best Practices

### 1. Security

```bash
# Set up additional environment variables
vercel env add AWS_REGION production
vercel env add KESTRA_URL production
```

### 2. Performance

- Enable Vercel Analytics
- Use Vercel Edge Network for global distribution
- Implement ISR (Incremental Static Regeneration) where applicable

### 3. Monitoring

```javascript
// Add to dashboard/app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 4. Custom Domain Setup

1. Purchase domain or use existing
2. Add domain in Vercel Dashboard
3. Update DNS records:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

## Continuous Deployment

### Automatic Deployments

Every push to main branch triggers:
1. Build process
2. Run tests (if configured)
3. Deploy to production

### Preview Deployments

Every pull request creates:
1. Unique preview URL
2. Isolated environment
3. Full functionality for testing

### Deployment Hooks

Configure webhooks in Vercel:
```bash
# Trigger deployment via webhook
curl -X POST https://api.vercel.com/v1/integrations/deploy/[PROJECT_ID]/[TOKEN]
```

## Scaling Considerations

### Vercel Pro/Enterprise Features

- Custom domains unlimited
- Enhanced DDoS protection
- Advanced analytics
- Priority support
- Team collaboration
- Password protection
- Staging environments

### Performance Optimization

1. **Image Optimization**: Use Next.js Image component
2. **Code Splitting**: Automatic with Next.js
3. **Caching**: Configure in `next.config.js`
4. **CDN**: Automatic via Vercel Edge Network

## Cost Estimation

### Hobby Plan (Free)
- Unlimited deployments
- 100 GB bandwidth/month
- Automatic HTTPS
- Perfect for demos and personal projects

### Pro Plan ($20/month)
- Increased bandwidth
- Advanced analytics
- Commercial use
- Team features

## Deployment Checklist

- [ ] Vercel account created
- [ ] Repository connected to Vercel
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Test deployment successful
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] API backend deployed and accessible
- [ ] CORS configured on backend
- [ ] Analytics enabled
- [ ] Error monitoring active
- [ ] Performance verified
- [ ] Mobile responsiveness tested

## Getting Help

### Resources
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Vercel Support](https://vercel.com/support)

### Common Commands

```bash
# Check deployment status
vercel ls

# View logs
vercel logs [deployment-url]

# Remove deployment
vercel remove [deployment-name]

# List environment variables
vercel env ls

# Pull environment variables locally
vercel env pull
```

## Example Deployment URL

After successful deployment, your dashboard will be accessible at:

```
https://aws-devops-dashboard.vercel.app
```

Or with custom domain:
```
https://devops.yourdomain.com
```

## Next Steps

After deployment:
1. Share the live URL in your hackathon submission
2. Add deployment URL to README.md
3. Take screenshots for documentation
4. Monitor performance and errors
5. Collect user feedback

---

**Your AWS DevOps Pipeline dashboard is now live on Vercel!** 🎉

For updates to the dashboard, simply push to your repository and Vercel will automatically redeploy.
