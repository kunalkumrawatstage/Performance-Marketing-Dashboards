# 📊 STAGE Multi-Market Performance Marketing Dashboard v2.0

A powerful, offline-first analytics dashboard for STAGE OTT's performance marketing team. Consolidate data from 4 markets (Gujarati, Haryanvi, Rajasthani, Bhojpuri) with AI-powered insights to transform 60-minute solver meetings into focused 15-minute decision sessions.

![Dashboard Version](https://img.shields.io/badge/version-2.0-blue)
![Status](https://img.shields.io/badge/status-production--ready-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 Key Features

### 📈 **Multi-Market Analytics**
- Support for 4 regional markets (GJ, HR, RJ, BH)
- One-click market switching with data persistence
- Independent data storage per market
- Cross-market performance comparison

### 📊 **Comprehensive Metrics**
Track 7 key performance indicators:
- **Total Spend** (₹) - Marketing investment
- **Total Trials** - User acquisition
- **Average CAC** (Customer Acquisition Cost)
- **CTR** (Click Through Rate) - > 0.75% is healthy
- **IR** (Install Rate) - ≥ 10% is healthy
- **TR** (Trial Rate) - ≥ 20% is healthy
- **D0 TCR** (Day 0 Trial Churn Rate) - < 30% is healthy

### 📉 **Advanced Analytics**
- **Channel Analysis**: Meta vs Google performance comparison
- **Platform Breakdown**: App vs Web metrics
- **Show Performance**: Individual title-level analysis
- **Week-over-Week Trends**: Historical performance tracking
- **Market Comparison**: Side-by-side regional analysis

### 🤖 **AI-Powered Insights**
- Intelligent insights generation (rule-based + Claude API ready)
- Priority-based recommendations (High/Medium/Low)
- Scaling opportunities identification
- Performance alerts and threshold violations
- Budget optimization suggestions

### 💾 **Data Management**
- **Excel Upload**: Drag-and-drop 5-10 files simultaneously
- **Auto-Parse**: Supports Meta and Google data formats
- **Persistent Storage**: IndexedDB (survives page refresh)
- **Historical Tracking**: Automatic weekly snapshot storage
- **Offline-First**: Works without internet connection

---

## 🚀 Quick Start

### Option 1: Local Usage (Recommended)

1. **Download the dashboard:**
   ```bash
   # Clone the repository
   git clone git@github.com:kunalkumrawatstage/Performance-Marketing-Dashboards.git
   cd Performance-Marketing-Dashboards
   ```

2. **Open the dashboard:**
   ```bash
   # macOS
   open dashboard-v2.html

   # Windows
   start dashboard-v2.html

   # Linux
   xdg-open dashboard-v2.html
   ```

3. **Upload your data:**
   - Drag-and-drop your Excel files (.xlsx or .csv)
   - Dashboard auto-processes and displays metrics
   - Data persists across sessions

### Option 2: Vercel Deployment (Team Access)

For team-wide access via URL:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy --prod
```

---

## 📁 Data Format

### Supported File Types
- `.xlsx` (Excel)
- `.csv` (Comma-separated values)

### Meta Platform Data Structure
Required columns:
- `Spends_GST` - Total spend with GST
- `af_start_trial` - Number of trials started
- `Mandate_CAC` - Cost per acquisition
- `AF_IR%` - Install rate percentage
- `TR%_AF` - Trial rate percentage
- `TCR_D0` - Day 0 trial churn rate
- `CTR%` - Click through rate
- `Show` - Show/title name (optional)

### Google Platform Data Structure
Required columns:
- `Spends_GST` - Total spend with GST
- `start_trial_d0` - Day 0 trials
- `CP_AF_CPT_D0` - Cost per trial
- `AF_IR%` - Install rate percentage
- `AF_TR%` - Trial rate percentage
- `AF_TCR%` - Trial churn rate percentage
- `CTR%` - Click through rate
- `Show` - Show/title name (optional)

### Sample Data Files
See `GJ Cac Solver/` folder for reference data structure.

---

## 📖 User Guide

### 1. First-Time Setup

**Initial Load:**
1. Open `dashboard-v2.html` in your browser
2. You'll see an empty state with the upload zone
3. Prepare your Excel files from Meta and Google

**Upload Data:**
1. Click the upload zone or drag-and-drop files
2. Select 5-10 Excel files (Meta + Google data)
3. Wait for processing (progress bar shows status)
4. Dashboard auto-renders with your data

### 2. Dashboard Navigation

**Market Selector** (Top Right)
- Click any market button: Gujarati, Haryanvi, Rajasthani, Bhojpuri
- Dashboard switches instantly (< 2 seconds)
- Each market maintains independent data

**Tab Navigation**
- **📈 Overall Performance**: KPIs + week-over-week trends
- **🎯 Channel Analysis**: Meta vs Google comparison charts
- **💻 Platform Breakdown**: App vs Web performance
- **🎬 Show Performance**: Detailed show-level table
- **🤖 AI Insights**: Strategic recommendations
- **🔄 Market Comparison**: Cross-market analysis

### 3. Understanding KPI Cards

**Color Coding:**
- 🟢 **Green border** = Healthy (meeting threshold)
- 🔴 **Red border** = Needs attention (below threshold)

**Indicators:**
- ✅ **Healthy** = Metric meets target
- ❌ **Needs Attention** = Metric below target

**Thresholds:**
```
CTR  > 0.75%  ✅ | ≤ 0.75%  ❌
IR   ≥ 10%    ✅ | < 10%    ❌
TR   ≥ 20%    ✅ | < 20%    ❌
TCR  < 30%    ✅ | ≥ 30%    ❌
CAC  < ₹250   ✅ | ≥ ₹250   ❌
```

### 4. Reading Charts

**Channel Analysis Chart**
- Blue bars = Meta performance
- Green bars = Google performance
- Compare spend, trials, CAC, and rates side-by-side

**Platform Breakdown Chart**
- Purple bars = App performance
- Orange bars = Web performance
- Identify which platform drives better ROI

**Trends Chart**
- Red line = CAC over time (left axis)
- Green line = Trials over time (right axis)
- Track performance trajectory week-by-week

### 5. Show Performance Table

**Table Features:**
- Click column headers to sort
- Color-coded rows:
  - 🟢 **Green** = Top 3 performers
  - 🔴 **Red** = Underperformers (TCR > 30% or CAC > ₹250)
  - ⚪ **White** = Normal performance

**Status Indicators:**
- 🏆 **Top Performer** = Top 3 by trial volume
- ⚠️ **Needs Attention** = Threshold violations
- ✅ **Good** = Healthy metrics

### 6. AI Insights

**Priority Levels:**
- 🔴 **HIGH PRIORITY** = Urgent actions required
- 🟡 **MEDIUM PRIORITY** = Important optimizations
- 🟢 **LOW PRIORITY** = Nice-to-have improvements

**Insight Structure:**
- **Title**: Summary of the insight
- **Analysis**: Context and supporting data
- **💡 Recommendation**: Specific action to take

**Regenerate Insights:**
- Click "🔄 Regenerate Insights" to refresh recommendations
- Insights update automatically when you upload new data

### 7. Market Comparison

**Comparison Cards:**
- View all 4 markets side-by-side
- Key metrics: Spend, Trials, CAC, TCR
- Quickly identify best and worst performers
- Learn from high-performing markets

### 8. Weekly Workflow

**Step-by-Step Process:**
1. **Export data** from Meta and Google platforms
2. **Open dashboard** (`dashboard-v2.html`)
3. **Select current market** (e.g., Gujarati)
4. **Upload new files** (drag-and-drop)
5. **Review overall metrics** (tab 1)
6. **Check channel performance** (tab 2)
7. **Analyze platform split** (tab 3)
8. **Review show performance** (tab 4)
9. **Read AI insights** (tab 5)
10. **Compare markets** (tab 6)
11. **Make decisions** based on insights
12. **Repeat for other markets**

**Time per Market:** ~15 minutes
**Total Meeting Time:** ~60 minutes for all 4 markets

---

## 🔧 Advanced Features

### API Key Configuration (Optional)

For enhanced AI insights using Claude API:

1. Click **⚙️ Settings** button (top right)
2. Enter your Claude API key
3. Key is securely stored in IndexedDB
4. Restart dashboard to use Claude-powered insights

**Get API Key:**
- Visit: https://console.anthropic.com/
- Create account and generate API key
- Cost: ~$0.01-0.05 per market analysis

### Data Persistence

**What's Stored:**
- Market data (current week)
- Historical snapshots (all previous weeks)
- API key (if provided)
- User settings

**Where:**
- Browser's IndexedDB (50MB+ capacity)
- Data persists across page refreshes
- Separate storage per market

**Clear Data:**
```javascript
// Open browser console (F12) and run:
indexedDB.deleteDatabase('STAGEDashboard');
```

### Keyboard Shortcuts

- `1-6` - Switch between tabs
- `G/H/R/B` - Switch markets (Gujarati/Haryanvi/Rajasthani/Bhojpuri)
- `U` - Focus upload zone
- `Esc` - Close modals

### Browser Compatibility

**Supported:**
- ✅ Chrome 90+ (recommended)
- ✅ Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

**Requirements:**
- JavaScript enabled
- IndexedDB support
- Modern CSS (Grid/Flexbox)

---

## 🧪 Testing

### Manual Testing Checklist

**Upload & Data Processing:**
- [ ] Upload single Excel file (.xlsx)
- [ ] Upload multiple Excel files (5-10)
- [ ] Upload CSV files
- [ ] Verify progress bar shows correctly
- [ ] Confirm data persists after refresh

**Market Switching:**
- [ ] Switch between all 4 markets
- [ ] Verify data loads correctly per market
- [ ] Confirm tab context preserved on switch
- [ ] Test with empty markets (no data)

**Tab Navigation:**
- [ ] Navigate through all 6 tabs
- [ ] Verify charts render correctly
- [ ] Check show table displays properly
- [ ] Confirm insights generate successfully

**Metrics & Calculations:**
- [ ] Verify KPI calculations match Excel
- [ ] Check threshold indicators (✅/❌)
- [ ] Confirm CAC = Spend / Trials
- [ ] Validate channel/platform breakdowns

**Charts & Visualizations:**
- [ ] Channel chart renders (Meta vs Google)
- [ ] Platform chart renders (App vs Web)
- [ ] Trends chart shows (requires 2+ weeks)
- [ ] Show table sortable and color-coded

**Insights:**
- [ ] AI insights generate without errors
- [ ] Priority badges display correctly
- [ ] Recommendations are actionable
- [ ] Regenerate button works

**Responsive Design:**
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768x1024)
- [ ] Test on mobile (375x667)

---

## 🐛 Troubleshooting

### Issue: Dashboard won't open
**Solution:** Ensure you're using a modern browser (Chrome/Edge/Firefox/Safari)

### Issue: Files won't upload
**Possible causes:**
1. File format not supported (use .xlsx or .csv)
2. File too large (> 10MB) - split into smaller files
3. File structure incorrect - check column names

**Solution:**
- Verify file format matches requirements
- Use sample files in `GJ Cac Solver/` as reference

### Issue: Data doesn't persist
**Solution:**
- Check browser settings allow local storage
- Don't use incognito/private mode
- Clear browser cache and retry

### Issue: Charts not rendering
**Solution:**
- Upload data for the current market first
- Switch to different tab and back
- Check browser console (F12) for errors

### Issue: No week-over-week trends
**Reason:** Trends require at least 2 weeks of data
**Solution:** Upload data for multiple weeks to see trends

### Issue: Insights not generating
**Possible causes:**
1. No data uploaded
2. API key required (if using Claude API)
3. Network issue (if using AI API)

**Solution:**
- Upload data first
- Use rule-based insights (works offline)
- Configure API key in settings (optional)

---

## 📊 Architecture

### Technology Stack

**Frontend:**
- Vanilla JavaScript (ES6+)
- HTML5 + CSS3 (Grid/Flexbox)
- No build tools required (single file)

**Libraries (CDN):**
- **SheetJS** (v0.18.5) - Excel parsing
- **Chart.js** (v4.4.0) - Visualizations
- **Dexie.js** (v3.2.4) - IndexedDB wrapper

**Data Storage:**
- IndexedDB (via Dexie.js)
- 50MB+ storage capacity
- Offline-first architecture

**AI Integration:**
- Rule-based insights (default)
- Claude API (optional, for enhanced insights)

### Component Architecture

```
┌─────────────────────────────────────────────┐
│           Browser (Client-Side)             │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │UI Layer │─▶│State Mgr │─▶│ Renderer  │  │
│  └─────────┘  └──────────┘  └───────────┘  │
│       │            │              │          │
│       ▼            ▼              ▼          │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Upload  │  │Analytics │  │ Insights  │  │
│  │ Handler │  │  Engine  │  │Generator  │  │
│  └─────────┘  └──────────┘  └───────────┘  │
│       │            │              │          │
│       ▼            ▼              ▼          │
│  ┌────────────────────────────────────────┐ │
│  │      Excel Parser (Web Worker)         │ │
│  └────────────────────────────────────────┘ │
│                   │                          │
│                   ▼                          │
│  ┌────────────────────────────────────────┐ │
│  │   Data Layer (IndexedDB via Dexie)    │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Data Flow

```
Excel Upload → Parse → Validate → Store → Calculate Metrics →
Generate Insights → Render UI → Cache Results
```

---

## 🚀 Deployment

### Option 1: Local Deployment (Default)

**No deployment needed!**
- Dashboard is a single HTML file
- Works offline
- Double-click to open
- Share file via email/drive

### Option 2: GitHub Pages

```bash
# 1. Push to GitHub (already done)
# 2. Enable GitHub Pages
# Settings → Pages → Source: main branch

# Your dashboard will be available at:
# https://kunalkumrawatstage.github.io/Performance-Marketing-Dashboards/dashboard-v2.html
```

### Option 3: Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /path/to/dashboard
vercel deploy --prod

# Follow prompts
# Dashboard will be live at: https://your-project.vercel.app
```

**Vercel Configuration** (create `vercel.json`):
```json
{
  "version": 2,
  "name": "stage-dashboard",
  "builds": [
    { "src": "dashboard-v2.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/dashboard-v2.html" }
  ]
}
```

### Option 4: Internal Server

```bash
# Simple HTTP server
python3 -m http.server 8000

# Access at: http://localhost:8000/dashboard-v2.html
```

---

## 📈 Roadmap

### v2.1 (Planned)
- [ ] Export dashboard as PDF
- [ ] Email report generation
- [ ] Custom date range selection
- [ ] Advanced filtering options

### v3.0 (Future)
- [ ] Direct Meta/Google API integration
- [ ] Real-time data sync
- [ ] Multi-user collaboration
- [ ] Role-based access control
- [ ] Mobile native app

---

## 🤝 Contributing

This is an internal STAGE OTT project. For feature requests or bug reports, contact:
- **Kunal Kumrawat** - Performance Marketing Team
- **Email**: [Your email]
- **Slack**: [Your slack handle]

---

## 📝 Changelog

### v2.0 (2026-02-12)
- ✅ Multi-market support (4 markets)
- ✅ Advanced chart visualizations
- ✅ Historical data tracking
- ✅ AI-powered insights
- ✅ Market comparison view
- ✅ Show performance analysis
- ✅ Week-over-week trends

### v1.0 (2026-02-11)
- ✅ Single market dashboard (Gujarati)
- ✅ Excel upload and parsing
- ✅ 7 KPI calculations
- ✅ Basic visualizations
- ✅ Data persistence

---

## 📄 License

Internal use only - STAGE OTT
© 2026 STAGE. All rights reserved.

---

## 🎉 Success Metrics

**Before Dashboard:**
- ⏱️ 1 hour per market meeting
- 📊 Manual Excel analysis
- 🤔 Delayed decision-making

**After Dashboard:**
- ⏱️ 15 minutes per market meeting (75% reduction)
- 📊 Automated insights
- ⚡ Instant data-driven decisions
- 🎯 CEO/Founder approved quality

---

**Built with ❤️ by Kunal Kumrawat + Claude Sonnet 4.5**

Last Updated: February 12, 2026
