# GJ Performance Dashboard - Project Handover

## 📊 Project Overview
Interactive web dashboard analyzing OTT platform marketing performance for Week Feb 1-7, 2026.

## 📁 Files Included

### Data Files (in `GJ Cac Solver/` folder):
1. **Stage_GJ- CAC SOLVER - Meta_SL-App.csv** - Meta App data (Week Feb 1-7)
2. **Stage_GJ- CAC SOLVER - Google_SL-app.csv** - Google App data (Week Feb 1-7)
3. **Stage_GJ- CAC SOLVER - Meta_SL-web_.csv** - Meta Web data (Week Feb 8-14) *Different week!*

### Dashboard:
- **performance_dashboard.html** - Interactive dashboard (open in any browser)

## 🎯 Key Metrics

### Week Feb 1-7, 2026 (App Only):
- **Total Spend:** ₹23.21L (₹23,21,041)
- **Total Trials:** 7,574
  - Meta App: 6,514 trials
  - Google App: 1,060 trials
- **Blended CAC:** ₹307
- **Overall TCR:** 31.6% ❌ (threshold: <30%)
- **IR%:** 14.8% ✅ (threshold: >10%)
- **TR%:** 25.4% ✅ (threshold: >20%)

### Performance Thresholds:
- ✅ **IR% > 10%** (Install Rate)
- ✅ **TR% > 20%** (Trial Rate)
- ✅ **TCR < 30%** (Trial Churn Rate - LOWER IS BETTER)

## 📌 Important Notes

### 1. Data Period Separation
- **App data (Meta + Google):** Week Feb 1-7, 2026
- **Web data (Meta):** Week Feb 8-14, 2026 (**Different week!**)
- Do NOT mix these in overall calculations

### 2. TCR Interpretation
**CRITICAL:** TCR (Trial Churn Rate D0) is a CHURN metric
- **Lower = Better** (less people dropping off)
- **<30% = Good** ✅
- **>30% = High churn** ❌

### 3. Dashboard Structure
The dashboard has 5 tabs:
1. **Overall** - Combined metrics for Week Feb 1-7
2. **Channel-wise** - Google vs Meta App comparison
3. **Platform-wise** - App vs Web view (Web shown separately due to different week)
4. **Show Performance** - Individual show breakdown (Meta App shows)
5. **WoW Trends** - Week over week comparison (Jan 25-31 vs Feb 1-7)

## 🚀 How to Use

### View Dashboard:
```bash
# Open in browser
open performance_dashboard.html
# or double-click the file
```

### Update with New Data:
If you receive new CSV files for a different week:
1. Place CSV files in the `GJ Cac Solver/` folder
2. Make sure all files are for the SAME week
3. Update the dashboard using Claude Code with the new data

## 🔧 Technical Details

### Data Columns Used:
**Google App CSV:**
- `Spends_GST` - Total spend
- `start_trial_d0` - Number of trials
- `CP_AF_CPT_D0` - Cost per trial (CAC)
- `AF_IR%` - Install Rate
- `AF_TR%` - Trial Rate
- `AF_TCR%` - Trial Churn Rate

**Meta App CSV:**
- `Spends_GST` - Total spend
- `af_start_trial` - Number of trials
- `Mandate_CAC` - Cost per trial (CAC)
- `AF_IR%` - Install Rate
- `TR%_AF` - Trial Rate
- `TCR_D0` - Trial Churn Rate

### CAC Calculation:
```
CAC = Total Spend ÷ Total Trials
Blended CAC = (Meta Spend + Google Spend) ÷ (Meta Trials + Google Trials)
```

### Top Performing Shows (Meta App):
1. **Saanwari** - 3,555 trials (53.3% of spend) | CAC: ₹283
2. **31st** - 2,362 trials (31.4% of spend) | CAC: ₹251 (Best CAC)
3. **Minzar** - 209 trials | TCR: 29.61% ✅ (Only major show passing threshold)

## ⚠️ Critical Issues Identified

### Retention Crisis:
- **Meta App TCR:** 32.01% ❌
- **Google App TCR:** 30.47% ❌
- Both channels above 30% threshold = high churn
- Only 2/3 thresholds passing (IR% ✅, TR% ✅, TCR ❌)

### Recommendations:
1. Focus on reducing churn (improve TCR to <30%)
2. Scale Saanwari & 31st (volume + good metrics)
3. Investigate Minzar success (only show with TCR <30%)
4. Consider Web expansion (better CAC at ₹237 vs ₹307)

## 📞 Questions?
All calculations verified:
- Trials: Manually summed from show-level data ✅
- CAC: Spend ÷ Trials verified for each platform ✅
- Overall: Weighted averages by trial volume ✅

## 🛠️ Built With:
- HTML5 + CSS3 + JavaScript
- Font Awesome 6.5.1 for icons
- Responsive design (works on mobile/tablet/desktop)

---

**Dashboard Status:** ✅ Production Ready
**Last Updated:** Week Feb 1-7, 2026 data
**Next Update:** Awaiting Week Feb 15-21 data
