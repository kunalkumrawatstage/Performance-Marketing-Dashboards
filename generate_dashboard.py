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
    """Generate comprehensive HTML dashboard with tabs and charts"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STAGE Performance Dashboard - Gujarati Market</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

        .header {{ background: white; padding: 25px 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }}
        .header h1 {{ color: #2563eb; font-size: 24px; }}
        .header p {{ color: #666; font-size: 14px; margin-top: 5px; }}

        .success {{ background: #f0fdf4; color: #15803d; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #22c55e; font-size: 14px; }}

        .tab-nav {{ display: flex; gap: 10px; margin-bottom: 20px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow-x: auto; }}
        .tab-btn {{ padding: 10px 20px; border: none; background: transparent; color: #666; font-weight: 500; cursor: pointer; border-radius: 6px; transition: all 0.2s; white-space: nowrap; }}
        .tab-btn:hover {{ background: #f3f4f6; color: #2563eb; }}
        .tab-btn.active {{ background: #2563eb; color: white; }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #2563eb; }}
        .metric-card.healthy {{ border-left-color: #10b981; }}
        .metric-card.unhealthy {{ border-left-color: #ef4444; }}
        .metric-label {{ font-size: 13px; color: #666; margin-bottom: 8px; font-weight: 500; }}
        .metric-value {{ font-size: 28px; font-weight: 700; color: #111; margin-bottom: 5px; }}
        .metric-status {{ font-size: 12px; font-weight: 600; }}
        .metric-status.healthy {{ color: #10b981; }}
        .metric-status.unhealthy {{ color: #ef4444; }}

        .chart-section {{ background: white; border-radius: 10px; padding: 30px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .chart-title {{ font-size: 18px; font-weight: 600; color: #111; margin-bottom: 20px; }}
        .chart-container {{ position: relative; height: 400px; }}

        .shows-table {{ background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f3f4f6; padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #374151; border-bottom: 2px solid #e5e7eb; cursor: pointer; }}
        th:hover {{ background: #e5e7eb; }}
        td {{ padding: 12px; border-bottom: 1px solid #e5e7eb; font-size: 14px; }}
        tr:hover {{ background: #f9fafb; }}
        .channel-badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
        .channel-meta {{ background: #dbeafe; color: #1e40af; }}
        .channel-google {{ background: #d1fae5; color: #065f46; }}

        .insight-card {{ background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 5px solid #2563eb; }}
        .insight-card.high {{ border-left-color: #ef4444; }}
        .insight-card.medium {{ border-left-color: #f59e0b; }}
        .insight-card.low {{ border-left-color: #10b981; }}
        .insight-badge {{ display: inline-block; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 15px; }}
        .insight-badge.high {{ background: #fee2e2; color: #991b1b; }}
        .insight-badge.medium {{ background: #fef3c7; color: #92400e; }}
        .insight-badge.low {{ background: #d1fae5; color: #065f46; }}
        .insight-title {{ font-size: 18px; font-weight: 700; color: #111; margin-bottom: 15px; line-height: 1.4; }}
        .insight-analysis {{ font-size: 14px; color: #374151; margin-bottom: 15px; line-height: 1.7; }}
        .insight-recommendation {{ background: #f9fafb; padding: 15px; border-radius: 8px; border-left: 3px solid #2563eb; margin-top: 15px; }}
        .insight-recommendation strong {{ color: #2563eb; }}
        .insight-impact {{ background: #1f2937; color: white; padding: 12px; border-radius: 6px; margin-top: 15px; font-size: 13px; }}
        .insight-impact strong {{ color: #60a5fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>📊 STAGE Performance Dashboard</h1>
                <p>Gujarati Market • Data Pre-Loaded ✅</p>
            </div>
        </div>

        <div class="success">
            ✅ Dashboard generated with {len(all_data)} show records • No file upload needed!
        </div>

        <div class="tab-nav">
            <button class="tab-btn active" data-tab="overall">📈 Overall Performance</button>
            <button class="tab-btn" data-tab="channel">🎯 Channel Analysis</button>
            <button class="tab-btn" data-tab="platform">💻 Platform Breakdown</button>
            <button class="tab-btn" data-tab="shows">🎬 Show Performance</button>
            <button class="tab-btn" data-tab="insights">🤖 AI Insights</button>
        </div>

        <div id="tab-overall" class="tab-content active">
            <div class="metrics-grid" id="metricsGrid"></div>
        </div>

        <div id="tab-channel" class="tab-content">
            <div class="chart-section">
                <div class="chart-title">📊 Channel Performance: Meta vs Google</div>
                <div class="chart-container">
                    <canvas id="channelChart"></canvas>
                </div>
            </div>
        </div>

        <div id="tab-platform" class="tab-content">
            <div class="chart-section">
                <div class="chart-title">💻 Platform Performance: App vs Web</div>
                <div class="chart-container">
                    <canvas id="platformChart"></canvas>
                </div>
            </div>
        </div>

        <div id="tab-shows" class="tab-content">
            <div class="shows-table">
                <div class="chart-title">📈 Show Performance Details</div>
                <table id="showsTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">Show ↕</th>
                            <th onclick="sortTable(1)">Channel ↕</th>
                            <th onclick="sortTable(2)">Platform ↕</th>
                            <th onclick="sortTable(3)">Spend (₹) ↕</th>
                            <th onclick="sortTable(4)">Trials ↕</th>
                            <th onclick="sortTable(5)">CAC (₹) ↕</th>
                            <th onclick="sortTable(6)">IR% ↕</th>
                            <th onclick="sortTable(7)">TR% ↕</th>
                            <th onclick="sortTable(8)">TCR% ↕</th>
                            <th onclick="sortTable(9)">CTR% ↕</th>
                        </tr>
                    </thead>
                    <tbody id="showsTableBody"></tbody>
                </table>
            </div>
        </div>

        <div id="tab-insights" class="tab-content">
            <div class="chart-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-bottom: 20px;">
                <div style="text-align: center;">
                    <div style="font-size: 48px; margin-bottom: 10px;">🤖</div>
                    <div class="chart-title" style="color: white; margin-bottom: 10px;">AI-Powered Insights & Recommendations</div>
                    <p style="opacity: 0.9; font-size: 14px;">Executive-level analysis • C-suite quality • Actionable recommendations</p>
                </div>
            </div>
            <div id="insightsContainer"></div>
        </div>
    </div>

    <script>
        const DATA = {json.dumps(all_data, indent=8)};
        let currentSortCol = 4; // Default sort by trials
        let sortAsc = false;

        function calculateMetrics(data) {{
            const totalSpend = data.reduce((sum, row) => sum + row.spend, 0);
            const totalTrials = data.reduce((sum, row) => sum + row.trials, 0);
            const avgCAC = totalTrials > 0 ? (totalSpend / totalTrials) : 0;
            const totalIR = data.reduce((sum, row) => sum + (row.ir * row.trials), 0);
            const totalTR = data.reduce((sum, row) => sum + (row.tr * row.trials), 0);
            const totalTCR = data.reduce((sum, row) => sum + (row.tcr * row.trials), 0);
            const totalCTR = data.reduce((sum, row) => sum + (row.ctr * row.spend), 0);
            const avgIR = totalTrials > 0 ? (totalIR / totalTrials) : 0;
            const avgTR = totalTrials > 0 ? (totalTR / totalTrials) : 0;
            const avgTCR = totalTrials > 0 ? (totalTCR / totalTrials) : 0;
            const avgCTR = totalSpend > 0 ? (totalCTR / totalSpend) : 0;
            return {{ totalSpend, totalTrials, cac: avgCAC, ir: avgIR, tr: avgTR, tcr: avgTCR, ctr: avgCTR }};
        }}

        function calculateChannelMetrics(data, channel) {{
            const filtered = data.filter(row => row.channel === channel);
            return calculateMetrics(filtered);
        }}

        function calculatePlatformMetrics(data, platform) {{
            const filtered = data.filter(row => row.platform === platform);
            return calculateMetrics(filtered);
        }}

        function formatCurrency(num) {{ return '₹' + parseFloat(num).toLocaleString('en-IN'); }}

        function renderMetrics() {{
            const metrics = calculateMetrics(DATA);
            const grid = document.getElementById('metricsGrid');
            const cards = [
                {{ label: 'Total Spend', value: formatCurrency(metrics.totalSpend), status: '', healthy: true }},
                {{ label: 'Total Trials', value: metrics.totalTrials.toLocaleString(), status: '', healthy: true }},
                {{ label: 'Average CAC', value: formatCurrency(metrics.cac.toFixed(2)), status: metrics.cac < 250 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.cac < 250 }},
                {{ label: 'CTR', value: metrics.ctr.toFixed(2) + '%', status: metrics.ctr > 0.75 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.ctr > 0.75 }},
                {{ label: 'Install Rate (IR)', value: metrics.ir.toFixed(2) + '%', status: metrics.ir >= 10 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.ir >= 10 }},
                {{ label: 'Trial Rate (TR)', value: metrics.tr.toFixed(2) + '%', status: metrics.tr >= 20 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.tr >= 20 }},
                {{ label: 'D0 TCR', value: metrics.tcr.toFixed(2) + '%', status: metrics.tcr < 30 ? 'Healthy ✅' : 'Needs Attention ⚠️', healthy: metrics.tcr < 30 }}
            ];
            grid.innerHTML = cards.map(card => `
                <div class="metric-card ${{card.healthy ? 'healthy' : 'unhealthy'}}">
                    <div class="metric-label">${{card.label}}</div>
                    <div class="metric-value">${{card.value}}</div>
                    ${{card.status ? `<div class="metric-status ${{card.healthy ? 'healthy' : 'unhealthy'}}">${{card.status}}</div>` : ''}}
                </div>
            `).join('');
        }}

        function renderChannelChart() {{
            const meta = calculateChannelMetrics(DATA, 'meta');
            const google = calculateChannelMetrics(DATA, 'google');
            const ctx = document.getElementById('channelChart');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Spend (₹)', 'Trials', 'CAC (₹)', 'CTR%', 'IR%', 'TR%', 'TCR%'],
                    datasets: [
                        {{ label: 'Meta', data: [meta.totalSpend, meta.totalTrials, meta.cac, meta.ctr, meta.ir, meta.tr, meta.tcr], backgroundColor: '#3b82f6' }},
                        {{ label: 'Google', data: [google.totalSpend, google.totalTrials, google.cac, google.ctr, google.ir, google.tr, google.tcr], backgroundColor: '#10b981' }}
                    ]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'top' }} }} }}
            }});
        }}

        function renderPlatformChart() {{
            const app = calculatePlatformMetrics(DATA, 'app');
            const web = calculatePlatformMetrics(DATA, 'web');
            const ctx = document.getElementById('platformChart');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Spend (₹)', 'Trials', 'CAC (₹)', 'CTR%', 'IR%', 'TR%', 'TCR%'],
                    datasets: [
                        {{ label: 'App', data: [app.totalSpend, app.totalTrials, app.cac, app.ctr, app.ir, app.tr, app.tcr], backgroundColor: '#8b5cf6' }},
                        {{ label: 'Web', data: [web.totalSpend, web.totalTrials, web.cac, web.ctr, web.ir, web.tr, web.tcr], backgroundColor: '#f97316' }}
                    ]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'top' }} }} }}
            }});
        }}

        function renderTable() {{
            const tbody = document.getElementById('showsTableBody');
            const sorted = [...DATA].sort((a, b) => {{
                const aVal = [a.show, a.channel, a.platform, a.spend, a.trials, a.cac, a.ir, a.tr, a.tcr, a.ctr][currentSortCol];
                const bVal = [b.show, b.channel, b.platform, b.spend, b.trials, b.cac, b.ir, b.tr, b.tcr, b.ctr][currentSortCol];
                return sortAsc ? (aVal > bVal ? 1 : -1) : (aVal < bVal ? 1 : -1);
            }});
            tbody.innerHTML = sorted.map(row => `
                <tr>
                    <td><strong>${{row.show}}</strong></td>
                    <td><span class="channel-badge channel-${{row.channel}}">${{row.channel}}</span></td>
                    <td>${{row.platform}}</td>
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

        function sortTable(col) {{
            if (currentSortCol === col) sortAsc = !sortAsc;
            else {{ currentSortCol = col; sortAsc = false; }}
            renderTable();
        }}

        function generateInsights() {{
            const metrics = calculateMetrics(DATA);
            const shows = [...DATA].sort((a, b) => b.trials - a.trials);
            const topShow = shows[0];
            const top3Shows = shows.slice(0, 3);

            const insights = [];

            // INSIGHT 1: Top Show Scaling Opportunity
            const topShowSpend = topShow.spend;
            const topShowTrials = topShow.trials;
            const projectedTrials = Math.floor(topShowTrials * 1.25);
            const additionalSpend = (projectedTrials - topShowTrials) * topShow.cac;

            insights.push({{
                title: `🚀 Scale "${{topShow.show}}" - Top Performer with ${{topShowTrials.toLocaleString()}} Trials`,
                analysis: `<strong>${{topShow.show}}</strong> is your strongest performer, generating <strong>${{((topShowTrials/metrics.totalTrials)*100).toFixed(1)}}%</strong> of total trials at ₹${{topShow.cac}} CAC. This show demonstrates proven product-market fit with ${{topShow.channel}} on ${{topShow.platform}}. Current spend: ₹${{formatCurrency(topShowSpend)}}. The CAC is <strong>${{topShow.cac < 250 ? 'below target (healthy)' : 'above target'}}</strong> and TCR is ${{topShow.tcr}}% ${{topShow.tcr < 30 ? '(excellent retention)' : '(needs improvement)'}}.`,
                recommendation: `<strong>💡 Immediate Action:</strong> Increase budget by <strong>20-25%</strong> (from ₹${{(topShowSpend/100000).toFixed(1)}}L to ₹${{(topShowSpend*1.25/100000).toFixed(1)}}L). Expected outcome: +${{(projectedTrials - topShowTrials).toLocaleString()}} trials for ₹${{(additionalSpend/100000).toFixed(2)}}L incremental spend. Maintain current creative and targeting strategies. Monitor daily for 5-7 days to ensure CAC stability.`,
                priority: 'high',
                impact: `Scaling top performer = ${{(projectedTrials - topShowTrials).toLocaleString()}} additional trials = ₹${{((projectedTrials - topShowTrials) * topShow.cac / 100000).toFixed(2)}}L efficient spend`
            }});

            // INSIGHT 2: CAC Efficiency Analysis
            const efficientShows = shows.filter(s => s.cac < 250 && s.trials > 50);
            const inefficientShows = shows.filter(s => s.cac >= 250);
            const avgEfficientCAC = efficientShows.length > 0 ?
                (efficientShows.reduce((sum, s) => sum + s.cac, 0) / efficientShows.length).toFixed(0) : metrics.cac;

            insights.push({{
                title: `💰 CAC Analysis: ₹${{metrics.cac.toFixed(0)}} Blended ${{metrics.cac < 250 ? '✅ Below Target' : '⚠️ Above Target'}}`,
                analysis: `Blended CAC of <strong>₹${{metrics.cac.toFixed(0)}}</strong> vs ₹250 target. <strong>${{efficientShows.length}} of ${{shows.length}} shows</strong> operate below target CAC (avg ₹${{avgEfficientCAC}}), driving ${{((efficientShows.reduce((s,sh)=>s+sh.trials,0)/metrics.totalTrials)*100).toFixed(1)}}% of volume. ${{inefficientShows.length > 0 ? `<strong style="color: #ef4444;">${{inefficientShows.length}} shows exceed ₹250 CAC</strong>: ${{inefficientShows.slice(0,3).map(s => s.show + ' (₹' + s.cac + ')').join(', ')}}. These shows require optimization or budget reallocation.` : 'All shows performing efficiently - excellent portfolio health.'}}`,
                recommendation: `<strong>💡 Action Plan:</strong><br>1. <strong>SCALE:</strong> Increase budget 20% for efficient shows: ${{efficientShows.slice(0,3).map(s => s.show).join(', ')}}.<br>2. ${{inefficientShows.length > 0 ? `<strong>OPTIMIZE/PAUSE:</strong> Reduce spend 30-50% on ${{inefficientShows.slice(0,2).map(s => s.show).join(', ')}} until CAC improves below ₹280. Test new creatives and audiences.` : 'Maintain current efficiency - monitor for creative fatigue.'}} <br>3. Reallocate ₹${{((inefficientShows.reduce((s,sh)=>s+sh.spend,0)*0.4)/100000).toFixed(1)}}L from inefficient to efficient shows.`,
                priority: metrics.cac > 250 ? 'high' : 'medium',
                impact: `CAC optimization = estimated ₹${{((metrics.totalSpend * 0.15) / 100000).toFixed(1)}}L cost savings`
            }});

            // INSIGHT 3: Channel Strategy
            const meta = calculateChannelMetrics(DATA, 'meta');
            const google = calculateChannelMetrics(DATA, 'google');
            const channelLeader = meta.cac < google.cac ? 'Meta' : 'Google';
            const cacDiff = Math.abs(meta.cac - google.cac).toFixed(0);
            const cacDiffPercent = (cacDiff / Math.min(meta.cac, google.cac) * 100).toFixed(0);

            insights.push({{
                title: `🎯 Channel Mix: ${{channelLeader}} Outperforming by ₹${{cacDiff}} CAC (${{cacDiffPercent}}%)`,
                analysis: `<strong>Meta:</strong> ${{meta.totalTrials.toLocaleString()}} trials @ ₹${{meta.cac.toFixed(0)}} CAC (${{(meta.totalTrials/metrics.totalTrials*100).toFixed(0)}}% share, ₹${{(meta.totalSpend/100000).toFixed(1)}}L spend). <strong>Google:</strong> ${{google.totalTrials.toLocaleString()}} trials @ ₹${{google.cac.toFixed(0)}} CAC (${{(google.totalTrials/metrics.totalTrials*100).toFixed(0)}}% share, ₹${{(google.totalSpend/100000).toFixed(1)}}L spend). ${{channelLeader}} demonstrates <strong>₹${{cacDiff}} lower CAC</strong> (+${{cacDiffPercent}}% efficiency edge).`,
                recommendation: `<strong>💡 Budget Rebalancing:</strong> ${{channelLeader === 'Meta' ? `Shift 15-20% budget from Google to Meta. Increase Meta from ₹${{(meta.totalSpend/100000).toFixed(1)}}L to ₹${{(meta.totalSpend*1.2/100000).toFixed(1)}}L. ${{cacDiffPercent > 20 ? 'Significant efficiency gap - prioritize Meta scaling.' : 'Maintain Google for audience diversification.'}}` : `Scale Google campaigns 15-20%. ${{cacDiffPercent > 20 ? 'Review Meta creative fatigue and audience saturation.' : 'Maintain balanced mix.'}}`}} Target: Reduce blended CAC to ₹${{(metrics.cac * 0.93).toFixed(0)}}.`,
                priority: cacDiffPercent > 20 ? 'high' : 'medium',
                impact: `Channel optimization = estimated +${{Math.floor(metrics.totalSpend/Math.min(meta.cac, google.cac) - metrics.totalTrials).toLocaleString()}} trials`
            }});

            // INSIGHT 4: Retention & TCR
            const healthyTCRShows = shows.filter(s => s.tcr < 30);
            const poorTCRShows = shows.filter(s => s.tcr >= 30);
            const lostTrials = poorTCRShows.reduce((sum, s) => {{
                const excessChurn = Math.max(0, (s.tcr - 29) / 100);
                return sum + Math.floor(s.trials * excessChurn);
            }}, 0);

            insights.push({{
                title: `${{metrics.tcr < 30 ? '✅' : '🚨'}} Trial Retention: ${{metrics.tcr.toFixed(1)}}% TCR ${{metrics.tcr < 30 ? 'Healthy' : 'CRITICAL'}}`,
                analysis: `Overall D0 churn at <strong>${{metrics.tcr.toFixed(1)}}%</strong> vs <30% target. ${{healthyTCRShows.length}} shows meet retention target${{healthyTCRShows.length > 0 ? ` (${{healthyTCRShows.slice(0,2).map(s => s.show + ': ' + s.tcr + '%').join(', ')}})` : ''}}. ${{poorTCRShows.length > 0 ? `<strong style="color: #ef4444;">${{poorTCRShows.length}} shows exceed 30% churn</strong>, bleeding approximately <strong>${{lostTrials.toLocaleString()}} trials</strong> worth ₹${{((lostTrials * metrics.cac)/100000).toFixed(1)}}L.` : 'Excellent retention across portfolio.'}}`,
                recommendation: `<strong>💡 Retention Strategy:</strong> ${{metrics.tcr >= 30 ? `<strong>URGENT:</strong> Audit content quality, onboarding UX, and trial value prop for ${{poorTCRShows.map(s=>s.show).join(', ')}}. Benchmark best performer against worst. Implement fixes within 48 hours. Target: Reduce TCR to <28%.` : `Maintain retention excellence. Document success factors from top performers and replicate. Continue A/B testing onboarding improvements.`}}`,
                priority: metrics.tcr >= 30 ? 'high' : 'low',
                impact: `Fixing retention = ${{lostTrials.toLocaleString()}} trial recovery = ₹${{((lostTrials * metrics.cac)/100000).toFixed(1)}}L cost avoidance`
            }});

            // INSIGHT 5: Platform Strategy
            const app = calculatePlatformMetrics(DATA, 'app');
            const web = calculatePlatformMetrics(DATA, 'web');
            const platformLeader = app.cac < web.cac ? 'App' : 'Web';

            insights.push({{
                title: `💻 Platform Mix: ${{platformLeader}} Leading with ₹${{Math.min(app.cac, web.cac).toFixed(0)}} CAC`,
                analysis: `<strong>App:</strong> ${{app.totalTrials.toLocaleString()}} trials @ ₹${{app.cac.toFixed(0)}} CAC. <strong>Web:</strong> ${{web.totalTrials.toLocaleString()}} trials @ ₹${{web.cac.toFixed(0)}} CAC. Platform split: ${{(app.totalTrials/metrics.totalTrials*100).toFixed(0)}}% App, ${{(web.totalTrials/metrics.totalTrials*100).toFixed(0)}}% Web. ${{platformLeader}} demonstrates better cost efficiency.`,
                recommendation: `<strong>💡 Platform Optimization:</strong> ${{platformLeader === 'App' ? 'Prioritize app install campaigns. Optimize app store listing (screenshots, reviews). Consider app-only promotional offers.' : 'Focus on web conversion optimization. Improve landing page UX and reduce signup friction. Test progressive web app (PWA).'}}`,
                priority: 'medium',
                impact: `Platform optimization = estimated +${{Math.floor(metrics.totalTrials * 0.08).toLocaleString()}} trials`
            }});

            // Sort by priority
            insights.sort((a, b) => {{
                const priority = {{ high: 3, medium: 2, low: 1 }};
                return priority[b.priority] - priority[a.priority];
            }});

            return insights;
        }}

        function renderInsights() {{
            const insights = generateInsights();
            const container = document.getElementById('insightsContainer');

            container.innerHTML = `
                <div style="background: #f0fdf4; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #10b981;">
                    <strong style="font-size: 16px; color: #065f46;">📊 Analysis Summary</strong><br>
                    <span style="color: #047857; font-size: 14px;">
                        Generated ${{insights.length}} executive insights •
                        ${{insights.filter(i => i.priority === 'high').length}} high priority •
                        ${{insights.filter(i => i.priority === 'medium').length}} medium priority •
                        ${{insights.filter(i => i.priority === 'low').length}} low priority
                    </span>
                </div>
            ` + insights.map((insight, idx) => `
                <div class="insight-card ${{insight.priority}}">
                    <span class="insight-badge ${{insight.priority}}">${{insight.priority.toUpperCase()}} PRIORITY</span>
                    <div class="insight-title">${{idx + 1}}. ${{insight.title}}</div>
                    <div class="insight-analysis">${{insight.analysis}}</div>
                    <div class="insight-recommendation">${{insight.recommendation}}</div>
                    <div class="insight-impact"><strong>💼 Business Impact:</strong> ${{insight.impact}}</div>
                </div>
            `).join('');
        }}

        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                e.target.classList.add('active');
                document.getElementById('tab-' + e.target.dataset.tab).classList.add('active');
                if (e.target.dataset.tab === 'channel') renderChannelChart();
                if (e.target.dataset.tab === 'platform') renderPlatformChart();
                if (e.target.dataset.tab === 'insights') renderInsights();
            }});
        }});

        renderMetrics();
        renderTable();
        console.log('✅ Dashboard loaded with', DATA.length, 'shows for Gujarati (GJ) Market');
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
