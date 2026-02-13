# Quick Start Guide - GJ Performance Dashboard

## 🚀 FASTEST WAY TO GET YOUR DASHBOARD WORKING (2 MINUTES)

---

## Step 1: Open the Dashboard (10 seconds)

1. Open Finder
2. Navigate to: `/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/`
3. **Double-click:** `dashboard-simple.html`
4. It will open in your web browser (Safari, Chrome, etc.)

---

## Step 2: Load Your Data (30 seconds)

### Option A: Drag and Drop (Easiest)

1. Open a **second Finder window**
2. Navigate to: `/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/GJ Cac Solver/`
3. You'll see 3 CSV files:
   - `Stage_GJ- CAC SOLVER - Meta_SL-App.csv`
   - `Stage_GJ- CAC SOLVER - Meta_SL-web_.csv`
   - `Stage_GJ- CAC SOLVER - Google_SL-app.csv`
4. **Select all 3 files** (Cmd+A or click each while holding Cmd)
5. **Drag them** into the blue drop zone in your dashboard
6. **Drop them** and wait 1-2 seconds

### Option B: Click to Browse

1. **Click** on the blue drop zone in the dashboard
2. In the file picker, navigate to: `GJ Cac Solver` folder
3. **Select all 3 CSV files**
4. Click **"Open"**
5. Wait 1-2 seconds

---

## Step 3: View Your Results (Instant!)

After loading, you'll see:

### ✅ Top Metrics (4 Big Cards)
- **Total Spend:** How much money was spent
- **Total Trials:** How many trials you got
- **Average CAC:** Cost per trial
- **Shows:** Number of active shows

### ✅ Detailed Show Cards
Below the metrics, you'll see cards for each show:
- Show name
- Individual spend
- Individual trials
- Individual CAC
- Which files the data came from

### ✅ Success Message
Green box saying: "✓ Successfully loaded 3 file(s) with [X] data points!"

---

## 🎯 What You Should See

**Expected Numbers (approximate):**
- Total Spend: ₹24-25 Lakhs
- Total Trials: 8,000-8,500
- Average CAC: ₹290-310
- Shows: 10-12 shows

**Top Shows:**
1. Saanwari (biggest spender)
2. 31st
3. JholaChhap
4. Minzar
5. BuilderBoys
6. And more...

---

## ❓ Troubleshooting

### Problem: Nothing happens after dropping files

**Solution 1:** Check file format
- Make sure files end with `.csv`
- If they end with `.xlsx`, you need to convert them to CSV first

**Solution 2:** Check browser console
1. Press `F12` (Windows) or `Cmd+Option+I` (Mac)
2. Click "Console" tab
3. Look for error messages
4. Share any red error messages with me

**Solution 3:** Use Debug Mode
1. Scroll to bottom of dashboard
2. Click "Show/Hide Debug" button
3. Look at the debug log
4. It will show exactly what was parsed

### Problem: Numbers look wrong

**Solution:** Check the debug log
1. Click "Show/Hide Debug"
2. Look for lines like:
   - "Extracted: Saanwari - Spends: 1007212, Trials: 3555"
3. Verify these match your CSV files
4. If they don't match, share the debug log with me

### Problem: Some shows are missing

**Solution:** Check file names
1. Make sure all 3 files are loaded
2. Look at the "Loaded Files" section
3. Each file should have a green "✓ X shows" badge
4. If any file has a red "✗ Error" badge, that file failed to load

---

## 📊 Understanding Your Dashboard

### Metric Cards (Top)
- **Purple cards** with large numbers
- Show overall performance across all shows
- Hover over them - they'll lift slightly

### Show Cards (Below)
- **White cards** with show-specific data
- Sorted by spend (highest first)
- Each card shows 4 metrics:
  1. Total Spend (₹)
  2. Trials (count)
  3. CAC (₹ per trial)
  4. Sources (which CSV files)

### File List
- Shows which files were successfully loaded
- Green badge = Success
- Number shows how many shows were extracted from that file

### Debug Section
- Technical details about parsing
- Only use if something goes wrong
- Shows exact data extracted from each file

---

## 🎨 Features

✅ **Drag and Drop:** Just drop your CSV files
✅ **Multiple Files:** Load all 3 at once
✅ **Auto-Aggregation:** Combines data from multiple files
✅ **Real-Time Processing:** See results immediately
✅ **Beautiful Design:** Modern, clean interface
✅ **No Installation:** Just open in browser
✅ **No Internet Required:** Works completely offline
✅ **Privacy:** All data stays on your computer

---

## 🔄 Loading New Data

Want to load different CSV files?

1. **Refresh the page:** Press `Cmd+R` (Mac) or `F5` (Windows)
2. **Drag new files:** Drop your new CSV files
3. **Done!** The dashboard updates with new data

---

## 💾 Saving Results

### To Save as PDF:
1. With dashboard open, press `Cmd+P` (Mac) or `Ctrl+P` (Windows)
2. Select "Save as PDF"
3. Click "Save"

### To Take Screenshot:
1. **Mac:** Press `Cmd+Shift+4`, then drag to select area
2. **Windows:** Press `Windows+Shift+S`, then select area

---

## 🆘 Still Having Issues?

If the dashboard doesn't work after following these steps:

1. **Take a screenshot** of what you see
2. **Click "Show/Hide Debug"** and take a screenshot of the log
3. **Share both screenshots** with me
4. **Tell me:** What browser are you using? (Safari, Chrome, Firefox, etc.)

I'll help you fix it immediately!

---

## ✅ Success Checklist

Before asking for help, make sure:

- [ ] You opened `dashboard-simple.html` (NOT dashboard-v2.html)
- [ ] You loaded all 3 CSV files
- [ ] The files are in CSV format (not XLSX)
- [ ] You're using a modern browser (Safari 14+, Chrome 90+, Firefox 88+)
- [ ] You waited at least 2-3 seconds after dropping files
- [ ] You checked the "Loaded Files" section for error badges

---

## 📁 File Locations Reference

| File | Location |
|------|----------|
| **Dashboard** | `/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/dashboard-simple.html` |
| **CSV Files** | `/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/GJ Cac Solver/` |
| **This Guide** | `/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/QUICK_START_GUIDE.md` |
| **Test Results** | `/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/TEST_RESULTS.md` |

---

## 🎉 That's It!

Your dashboard should be working now. If you see your metrics and show cards, **you're done!**

Enjoy your dashboard! 🚀

---

**Questions?** Just ask - I'm here to help!

Generated: 2026-02-13
