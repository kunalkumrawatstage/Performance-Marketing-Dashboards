#!/usr/bin/env python3
"""
STAGE Performance Dashboard Generator
Reads CSV files and creates a standalone HTML dashboard with data embedded.
NO FILE UPLOAD NEEDED - Data is pre-loaded!
"""

import csv
import json
import os
from pathlib import Path

def clean_number(value):
    """Remove commas and convert to number"""
    if not value or value == '':
        return 0
    # Remove commas and percentage signs
    cleaned = str(value).replace(',', '').replace('%', '').strip()
    try:
        return float(cleaned)
    except:
        return 0

def parse_csv_file(filepath):
    """Parse a CSV file and extract show data"""
    data = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        # Find the header row (contains "Spends_GST" or "showname")
        header_idx = None
        for i, line in enumerate(lines):
            if 'Spends_GST' in line or 'showname' in line:
                header_idx = i
                break

        if header_idx is None:
            print(f"   ❌ Could not find header row")
            return data

        # Read CSV starting from header row
        reader = csv.DictReader(lines[header_idx:])

        # Detect file type from filename
        filename = os.path.basename(filepath).lower()
        is_meta = 'meta' in filename
        is_web = 'web' in filename
        is_google = 'google' in filename

        channel = 'meta' if is_meta else 'google'
        platform = 'web' if is_web else 'app'

        print(f"\n📄 Processing: {os.path.basename(filepath)}")
        print(f"   Channel: {channel}, Platform: {platform}")

        for row in reader:
            # Get show name from various possible columns
            show_name = (row.get('Show_Name - APP') or
                        row.get('Show_Name') or
                        row.get('showname') or
                        row.get('show') or '').strip()

            # Skip empty rows, headers, and totals
            if not show_name or show_name in ['Grand Total', 'Values', ''] or 'Week' in show_name:
                continue

            # Extract metrics based on file type
            spend = clean_number(row.get('Spends_GST', 0))

            if is_meta and not is_web:
                # Meta App file
                trials = int(clean_number(row.get('af_start_trial', 0)))
                cac = clean_number(row.get('Mandate_CAC', 0))
                ir = clean_number(row.get('AF_IR%', 0))
                tr = clean_number(row.get('TR%_AF', 0))
                tcr = clean_number(row.get('TCR_D0', 0))
                ctr = clean_number(row.get('CTR', 0))
            elif is_meta and is_web:
                # Meta Web file
                trials = int(clean_number(row.get('Trial_web', 0)))
                cac = clean_number(row.get('Mandate_CAC', 0))
                ir = 0  # Not available in web file
                tr = 0  # Not available in web file
                tcr = clean_number(row.get('TCR_D0', 0))
                ctr = clean_number(row.get('CTR', 0))
            else:
                # Google file
                cac = clean_number(row.get('CP_AF_CPT_D0', 0))
                trials = int(spend / cac) if cac > 0 else 0
                ir = clean_number(row.get('AF_IR%', 0))
                tr = clean_number(row.get('AF_TR%', 0))
                tcr = clean_number(row.get('AF_TCR%', 0))
                ctr = clean_number(row.get('CTR', 0))

            # Only include if we have meaningful data
            if spend > 0 or trials > 0:
                data.append({
                    'show': show_name,
                    'channel': channel,
                    'platform': platform,
                    'spend': spend,
                    'trials': trials,
                    'cac': cac,
                    'ir': ir,
                    'tr': tr,
                    'tcr': tcr,
                    'ctr': ctr
                })
                print(f"   ✓ {show_name}: {trials} trials, ₹{cac} CAC")

        print(f"   📊 Extracted {len(data)} shows")

    return data

def generate_dashboard_html(all_data):
    """Generate standalone HTML dashboard with embedded data"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STAGE Performance Dashboard - Gujarati Market</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header h1 {{ color: #2563eb; font-size: 28px; margin-bottom: 10px; }}
        .header p {{ color: #666; }}

        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #2563eb; }}
        .metric-label {{ font-size: 14px; color: #666; margin-bottom: 8px; font-weight: 500; }}
        .metric-value {{ font-size: 32px; font-weight: 700; color: #111; margin-bottom: 5px; }}
        .metric-status {{ font-size: 13px; font-weight: 600; }}
        .metric-status.healthy {{ color: #10b981; }}
        .metric-status.unhealthy {{ color: #ef4444; }}

        .shows-table {{ background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .shows-table h2 {{ font-size: 20px; margin-bottom: 20px; color: #111; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f3f4f6; padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #374151; border-bottom: 2px solid #e5e7eb; }}
        td {{ padding: 12px; border-bottom: 1px solid #e5e7eb; font-size: 14px; }}
        tr:hover {{ background: #f9fafb; }}
        .channel-badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
        .channel-meta {{ background: #dbeafe; color: #1e40af; }}
        .channel-google {{ background: #d1fae5; color: #065f46; }}
        .platform-app {{ color: #7c3aed; }}
        .platform-web {{ color: #ea580c; }}

        .success {{ background: #f0fdf4; color: #15803d; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #22c55e; }}
        .success strong {{ font-size: 16px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 STAGE Performance Dashboard</h1>
            <p>Gujarati Market • Performance Marketing Analytics • Data Pre-Loaded ✅</p>
        </div>

        <div class="success">
            <strong>✅ Dashboard Generated Successfully!</strong><br>
            All CSV files have been processed and data is embedded in this page.<br>
            <strong>No file upload needed</strong> - just open this file in your browser anytime!
        </div>

        <div class="metrics-grid" id="metricsGrid"></div>

        <div class="shows-table">
            <h2>📈 Show Performance</h2>
            <table id="showsTable">
                <thead>
                    <tr>
                        <th>Show</th>
                        <th>Channel</th>
                        <th>Platform</th>
                        <th>Spend (₹)</th>
                        <th>Trials</th>
                        <th>CAC (₹)</th>
                        <th>IR%</th>
                        <th>TR%</th>
                        <th>TCR%</th>
                        <th>CTR%</th>
                    </tr>
                </thead>
                <tbody id="showsTableBody"></tbody>
            </table>
        </div>
    </div>

    <script>
        // EMBEDDED DATA - Generated from your CSV files
        const DATA = {json.dumps(all_data, indent=8)};

        // Calculate overall metrics
        function calculateMetrics(data) {{
            const totalSpend = data.reduce((sum, row) => sum + row.spend, 0);
            const totalTrials = data.reduce((sum, row) => sum + row.trials, 0);
            const avgCAC = totalTrials > 0 ? (totalSpend / totalTrials) : 0;

            // Weighted averages for percentages
            const totalIR = data.reduce((sum, row) => sum + (row.ir * row.trials), 0);
            const totalTR = data.reduce((sum, row) => sum + (row.tr * row.trials), 0);
            const totalTCR = data.reduce((sum, row) => sum + (row.tcr * row.trials), 0);
            const totalCTR = data.reduce((sum, row) => sum + (row.ctr * row.spend), 0);

            const avgIR = totalTrials > 0 ? (totalIR / totalTrials) : 0;
            const avgTR = totalTrials > 0 ? (totalTR / totalTrials) : 0;
            const avgTCR = totalTrials > 0 ? (totalTCR / totalTrials) : 0;
            const avgCTR = totalSpend > 0 ? (totalCTR / totalSpend) : 0;

            return {{
                totalSpend: totalSpend.toFixed(0),
                totalTrials,
                cac: avgCAC.toFixed(2),
                ir: avgIR.toFixed(2),
                tr: avgTR.toFixed(2),
                tcr: avgTCR.toFixed(2),
                ctr: avgCTR.toFixed(2)
            }};
        }}

        function formatCurrency(num) {{
            return '₹' + parseFloat(num).toLocaleString('en-IN');
        }}

        function renderMetrics() {{
            const metrics = calculateMetrics(DATA);
            const grid = document.getElementById('metricsGrid');

            const cards = [
                {{ label: 'Total Spend', value: formatCurrency(metrics.totalSpend), status: '' }},
                {{ label: 'Total Trials', value: metrics.totalTrials.toLocaleString(), status: '' }},
                {{ label: 'Average CAC', value: formatCurrency(metrics.cac), status: metrics.cac < 250 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.cac < 250 }},
                {{ label: 'CTR', value: metrics.ctr + '%', status: metrics.ctr > 0.75 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.ctr > 0.75 }},
                {{ label: 'Install Rate (IR)', value: metrics.ir + '%', status: metrics.ir >= 10 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.ir >= 10 }},
                {{ label: 'Trial Rate (TR)', value: metrics.tr + '%', status: metrics.tr >= 20 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.tr >= 20 }},
                {{ label: 'D0 TCR', value: metrics.tcr + '%', status: metrics.tcr < 30 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.tcr < 30 }}
            ];

            grid.innerHTML = cards.map(card => `
                <div class="metric-card">
                    <div class="metric-label">${{card.label}}</div>
                    <div class="metric-value">${{card.value}}</div>
                    ${{card.status ? `<div class="metric-status ${{card.healthy ? 'healthy' : 'unhealthy'}}">${{card.status}}</div>` : ''}}
                </div>
            `).join('');
        }}

        function renderTable() {{
            const tbody = document.getElementById('showsTableBody');

            // Sort by trials descending
            const sortedData = [...DATA].sort((a, b) => b.trials - a.trials);

            tbody.innerHTML = sortedData.map(row => `
                <tr>
                    <td><strong>${{row.show}}</strong></td>
                    <td><span class="channel-badge channel-${{row.channel}}">${{row.channel}}</span></td>
                    <td><span class="platform-${{row.platform}}">${{row.platform}}</span></td>
                    <td>${{formatCurrency(row.spend)}}</td>
                    <td>${{row.trials.toLocaleString()}}</td>
                    <td>${{formatCurrency(row.cac)}}</td>
                    <td>${{row.ir}}%</td>
                    <td>${{row.tr}}%</td>
                    <td>${{row.tcr}}%</td>
                    <td>${{row.ctr}}%</td>
                </tr>
            `).join('');
        }}

        // Initialize dashboard
        renderMetrics();
        renderTable();

        console.log('✅ Dashboard loaded with', DATA.length, 'shows');
    </script>
</body>
</html>"""

    return html

def main():
    print("=" * 60)
    print("📊 STAGE Performance Dashboard Generator")
    print("=" * 60)

    # Define file paths
    csv_folder = Path(__file__).parent / "GJ Cac Solver"
    csv_files = [
        csv_folder / "Stage_GJ- CAC SOLVER - Meta_SL-App.csv",
        csv_folder / "Stage_GJ- CAC SOLVER - Meta_SL-web_.csv",
        csv_folder / "Stage_GJ- CAC SOLVER - Google_SL-app.csv"
    ]

    # Check if files exist
    missing_files = [f for f in csv_files if not f.exists()]
    if missing_files:
        print("\n❌ ERROR: Cannot find CSV files:")
        for f in missing_files:
            print(f"   - {f}")
        print("\nMake sure CSV files are in the 'GJ Cac Solver' folder")
        return

    # Parse all CSV files
    all_data = []
    for csv_file in csv_files:
        try:
            data = parse_csv_file(csv_file)
            all_data.extend(data)
        except Exception as e:
            print(f"\n❌ ERROR parsing {csv_file.name}: {e}")
            return

    if not all_data:
        print("\n❌ ERROR: No data extracted from CSV files")
        return

    print(f"\n✅ Total shows extracted: {len(all_data)}")

    # Generate HTML dashboard
    print("\n🔨 Generating HTML dashboard...")
    html_content = generate_dashboard_html(all_data)

    # Write to file
    output_file = Path(__file__).parent / "dashboard_generated.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ SUCCESS! Dashboard created: {output_file.name}")
    print("\n" + "=" * 60)
    print("🎉 HOW TO USE:")
    print("=" * 60)
    print("1. Open 'dashboard_generated.html' in your browser")
    print("2. That's it! Data is already loaded.")
    print("3. No file upload needed - everything is embedded!")
    print("\nTo update with new data:")
    print("1. Replace CSV files in 'GJ Cac Solver' folder")
    print("2. Run this script again: python3 generate_dashboard.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
