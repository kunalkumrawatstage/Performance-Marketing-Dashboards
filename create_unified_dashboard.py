#!/usr/bin/env python3
"""
Create Unified Multi-Market Dashboard
Combines all available markets into one dashboard with market selector.
"""

import json
from pathlib import Path

def main():
    print("=" * 60)
    print("📊 Creating Unified Multi-Market Dashboard")
    print("=" * 60)

    base_path = Path(__file__).parent

    # Check for market data files
    markets = {}

    # Load Gujarati data
    gj_json = base_path / "GJ Cac Solver" / "gj_data.json"
    if not gj_json.exists():
        print("\n📄 Generating Gujarati data...")
        import subprocess
        subprocess.run(["python3", "generate_dashboard.py"], check=True)

    # Load Haryanvi data
    hr_json = base_path / "hr_data.json"
    if hr_json.exists():
        with open(hr_json, 'r') as f:
            markets['haryanvi'] = json.load(f)
        print(f"✅ Loaded Haryanvi: {len(markets['haryanvi'])} shows")

    # Load Gujarati data from generated dashboard
    dashboard_gen = base_path / "dashboard_generated.html"
    if dashboard_gen.exists():
        import re
        with open(dashboard_gen, 'r') as f:
            content = f.read()
            # Extract DATA array from JavaScript
            match = re.search(r'const DATA = (\[.*?\]);', content, re.DOTALL)
            if match:
                markets['gujarati'] = json.loads(match.group(1))
                print(f"✅ Loaded Gujarati: {len(markets['gujarati'])} shows")

    if not markets:
        print("\n❌ No market data found!")
        print("Please generate at least one market dashboard first.")
        return

    print(f"\n✅ Found {len(markets)} markets")

    # Generate unified dashboard
    print("\n🔨 Creating unified dashboard...")
    html = generate_unified_html(markets)

    output_file = base_path / "dashboard_unified.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ SUCCESS! Created: {output_file.name}")
    print("\n" + "=" * 60)
    print("🎉 UNIFIED DASHBOARD READY!")
    print("=" * 60)
    print(f"\n📊 Markets available: {', '.join(m.capitalize() for m in markets.keys())}")
    print(f"\n💡 Open: {output_file.name}")
    print("   Click market buttons at top to switch between markets!")
    print("=" * 60)

def generate_unified_html(markets_data):
    """Generate unified HTML with market selector"""

    # Market code mapping
    market_codes = {
        'gujarati': 'GJ',
        'haryanvi': 'HR',
        'rajasthani': 'RJ',
        'bhojpuri': 'BH'
    }

    # Create market buttons HTML
    market_buttons = ""
    for idx, market in enumerate(markets_data.keys()):
        active = "active" if idx == 0 else ""
        display_name = market.capitalize()
        code = market_codes.get(market, market[:2].upper())
        market_buttons += f'<button class="market-btn {active}" data-market="{market}">{display_name} ({code})</button>\n            '

    markets_json = json.dumps(markets_data, indent=8)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STAGE Multi-Market Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

        .header {{ background: white; padding: 20px 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .header h1 {{ color: #2563eb; font-size: 24px; }}
        .header p {{ color: #666; font-size: 14px; margin-top: 5px; }}

        .market-selector {{ display: flex; gap: 10px; background: #f3f4f6; padding: 8px; border-radius: 8px; flex-wrap: wrap; }}
        .market-btn {{ padding: 10px 20px; border: none; background: transparent; color: #666; font-weight: 600; cursor: pointer; border-radius: 6px; transition: all 0.2s; font-size: 14px; }}
        .market-btn:hover {{ background: white; color: #2563eb; }}
        .market-btn.active {{ background: #2563eb; color: white; box-shadow: 0 2px 6px rgba(37,99,235,0.3); }}

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
            <div class="header-top">
                <div>
                    <h1>📊 STAGE Multi-Market Performance Dashboard</h1>
                    <p id="marketSubtitle">Select a market to view analytics</p>
                </div>
            </div>
            <div class="market-selector">
                {market_buttons}
            </div>
        </div>

        <div class="success">
            ✅ Multi-market dashboard loaded • <span id="showCount">0</span> shows in current market • Switch markets anytime!
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
                <div class="chart-container"><canvas id="channelChart"></canvas></div>
            </div>
        </div>

        <div id="tab-platform" class="tab-content">
            <div class="chart-section">
                <div class="chart-title">💻 Platform Performance: App vs Web</div>
                <div class="chart-container"><canvas id="platformChart"></canvas></div>
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
        // ALL MARKETS DATA
        const ALL_MARKETS_DATA = {markets_json};

        let currentMarket = '{list(markets_data.keys())[0]}';
        let currentSortCol = 4;
        let sortAsc = false;
        let channelChart = null;
        let platformChart = null;

        function getCurrentData() {{
            return ALL_MARKETS_DATA[currentMarket] || [];
        }}

        function switchMarket(market) {{
            currentMarket = market;
            const marketDisplay = market.charAt(0).toUpperCase() + market.slice(1);
            const marketCodes = {{
                'gujarati': 'GJ',
                'haryanvi': 'HR',
                'rajasthani': 'RJ',
                'bhojpuri': 'BH'
            }};
            const marketCode = marketCodes[market] || market.substring(0, 2).toUpperCase();
            document.getElementById('marketSubtitle').textContent = `${{marketDisplay}} (${{marketCode}}) Market • Data Pre-Loaded ✅`;
            document.getElementById('showCount').textContent = getCurrentData().length;

            // Update UI
            renderAll();

            console.log(`✅ Switched to ${{marketDisplay}} market (${{getCurrentData().length}} shows)`);
        }}

        function renderAll() {{
            renderMetrics();
            renderTable();

            // Re-render charts if those tabs are active
            const currentTab = document.querySelector('.tab-btn.active').dataset.tab;
            if (currentTab === 'channel') renderChannelChart();
            if (currentTab === 'platform') renderPlatformChart();
            if (currentTab === 'insights') renderInsights();
        }}

        // [Include all calculation and rendering functions from original template]
        // For brevity, the full JavaScript would be included here

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

        function formatCurrency(num) {{ return '₹' + parseFloat(num).toLocaleString('en-IN'); }}

        function renderMetrics() {{
            const data = getCurrentData();
            const metrics = calculateMetrics(data);
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

        function renderTable() {{
            const data = getCurrentData();
            const tbody = document.getElementById('showsTableBody');
            const sorted = [...data].sort((a, b) => {{
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

        function renderChannelChart() {{
            const data = getCurrentData();
            const meta = calculateMetrics(data.filter(r => r.channel === 'meta'));
            const google = calculateMetrics(data.filter(r => r.channel === 'google'));
            const ctx = document.getElementById('channelChart');
            if (channelChart) channelChart.destroy();
            channelChart = new Chart(ctx, {{
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
            const data = getCurrentData();
            const app = calculateMetrics(data.filter(r => r.platform === 'app'));
            const web = calculateMetrics(data.filter(r => r.platform === 'web'));
            const ctx = document.getElementById('platformChart');
            if (platformChart) platformChart.destroy();
            platformChart = new Chart(ctx, {{
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

        function calculateChannelMetrics(data, channel) {{
            const filtered = data.filter(row => row.channel === channel);
            return calculateMetrics(filtered);
        }}

        function calculatePlatformMetrics(data, platform) {{
            const filtered = data.filter(row => row.platform === platform);
            return calculateMetrics(filtered);
        }}

        function generateInsights() {{
            const DATA = getCurrentData();
            const metrics = calculateMetrics(DATA);
            const shows = [...DATA].sort((a, b) => b.trials - a.trials);
            const topShow = shows[0];

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
                ${{insights.map(insight => `
                    <div class="insight-card ${{insight.priority}}">
                        <div class="insight-badge ${{insight.priority}}">${{insight.priority.toUpperCase()}} PRIORITY</div>
                        <div class="insight-title">${{insight.title}}</div>
                        <div class="insight-analysis">${{insight.analysis}}</div>
                        <div class="insight-recommendation">${{insight.recommendation}}</div>
                        <div class="insight-impact"><strong>💰 Business Impact:</strong> ${{insight.impact}}</div>
                    </div>
                `).join('')}}
            `;
        }}

        function sortTable(col) {{
            if (currentSortCol === col) sortAsc = !sortAsc;
            else {{ currentSortCol = col; sortAsc = false; }}
            renderTable();
        }}

        // Event listeners
        document.querySelectorAll('.market-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                document.querySelectorAll('.market-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                switchMarket(e.target.dataset.market);
            }});
        }});

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

        // Initialize
        switchMarket(currentMarket);
        console.log('✅ Multi-market dashboard loaded with', Object.keys(ALL_MARKETS_DATA).length, 'markets');
    </script>
</body>
</html>"""

    return html

if __name__ == "__main__":
    main()
