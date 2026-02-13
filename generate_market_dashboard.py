#!/usr/bin/env python3
"""
STAGE Performance Dashboard Generator - Single Market
Generates dashboard from ANY CSV files in specified folder.
"""

import csv
import json
import os
import sys
from pathlib import Path

def clean_number(value):
    """Remove commas and convert to number"""
    if not value or value == '':
        return 0
    cleaned = str(value).replace(',', '').replace('%', '').strip()
    try:
        return float(cleaned)
    except:
        return 0

def get_column_value(row, *possible_names):
    """Get column value with case-insensitive matching"""
    # Create a lowercase key map
    key_map = {k.lower(): k for k in row.keys()}

    for name in possible_names:
        lower_name = name.lower()
        if lower_name in key_map:
            return row[key_map[lower_name]]
    return None

def parse_csv_file(filepath, filename):
    """Parse a CSV file and extract show data"""
    data = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        # Find the header row (case-insensitive)
        header_idx = None
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if 'spends_gst' in line_lower or 'showname' in line_lower or 'grouped showname' in line_lower:
                header_idx = i
                break

        if header_idx is None:
            print(f"   ❌ Could not find header row")
            return data

        reader = csv.DictReader(lines[header_idx:])

        # Detect file type from filename
        is_meta = 'meta' in filename.lower()
        is_web = 'web' in filename.lower()
        is_google = 'google' in filename.lower()

        channel = 'meta' if is_meta else 'google'
        platform = 'web' if is_web else 'app'

        print(f"   Channel: {channel}, Platform: {platform}")

        for row in reader:
            # Get show name from various possible columns
            show_name = (get_column_value(row, 'Grouped Showname', 'Show_Name - APP', 'Show_Name', 'showname', 'show') or '').strip()

            # Skip empty rows
            if not show_name or 'Week' in show_name or show_name == 'Grand Total':
                continue

            # Extract metrics with case-insensitive column matching
            spend = clean_number(get_column_value(row, 'Spends_GST', 'Spends_gst', 'Spend') or 0)

            if is_meta and not is_web:
                # Meta App file - check for both column name variations
                trials = int(clean_number(get_column_value(row, 'af_start_trial_uni', 'af_start_trial', 'Trials') or 0))
                cac = clean_number(get_column_value(row, 'Mandate_CAC', 'CAC') or 0)
                ir = clean_number(get_column_value(row, 'AF_IR%', 'IR%') or 0)
                tr = clean_number(get_column_value(row, 'TR%_AF', 'TR%') or 0)
                tcr = clean_number(get_column_value(row, 'TCR_D0', 'TCR%') or 0)
                ctr = clean_number(get_column_value(row, 'CTR', 'CTR%') or 0)
            elif is_meta and is_web:
                # Meta Web file
                trials = int(clean_number(get_column_value(row, 'Trial_web', 'af_start_trial_uni', 'Trials') or 0))
                cac = clean_number(get_column_value(row, 'Mandate_CAC', 'CAC') or 0)
                ir = 0
                tr = 0
                tcr = clean_number(get_column_value(row, 'TCR_D0', 'TCR%') or 0)
                ctr = clean_number(get_column_value(row, 'CTR', 'CTR%') or 0)
            else:
                # Google file
                cac = clean_number(get_column_value(row, 'CP_AF_CPT_D0', 'CAC') or 0)
                trials = int(spend / cac) if cac > 0 else 0
                ir = clean_number(get_column_value(row, 'AF_IR%', 'IR%') or 0)
                tr = clean_number(get_column_value(row, 'AF_TR%', 'TR%') or 0)
                tcr = clean_number(get_column_value(row, 'AF_TCR%D0', 'AF_TCR%', 'TCR%') or 0)
                ctr = clean_number(get_column_value(row, 'CTR', 'CTR%') or 0)

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

def generate_dashboard_html(all_data, market_name):
    """Generate HTML dashboard with all features"""

    # Read the template from generate_dashboard.py output as reference
    # For now, using simplified inline template

    market_display = market_name.capitalize()

    html_template = open('dashboard_generated.html', 'r').read()

    # Replace market name and data
    html_output = html_template.replace('Gujarati Market', f'{market_display} Market')
    html_output = html_output.replace('Gujarati (GJ)', f'{market_display} ({market_name[:2].upper()})')
    html_output = html_output.replace('const DATA =', f'const DATA = {json.dumps(all_data, indent=8)}; const OLD_DATA =')

    return html_output

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_market_dashboard.py <market_name>")
        print("Example: python3 generate_market_dashboard.py haryanvi")
        print("")
        print("Available markets:")
        print("  - gujarati (folder: GJ Cac Solver)")
        print("  - haryanvi (folder: HR Cac Solver)")
        print("  - rajasthani (folder: RJ Cac Solver)")
        print("  - bhojpuri (folder: BH Cac Solver)")
        sys.exit(1)

    market = sys.argv[1].lower()

    # Map market names to folder names
    folder_map = {
        'gujarati': 'GJ Cac Solver',
        'haryanvi': 'HR Cac Solver',
        'rajasthani': 'RJ Cac Solver',
        'bhojpuri': 'BH Cac Solver'
    }

    if market not in folder_map:
        print(f"❌ Unknown market: {market}")
        print("Available markets: gujarati, haryanvi, rajasthani, bhojpuri")
        sys.exit(1)

    folder_name = folder_map[market]
    base_path = Path(__file__).parent
    csv_folder = base_path / folder_name

    print("=" * 60)
    print(f"📊 STAGE Performance Dashboard Generator - {market.upper()}")
    print("=" * 60)

    if not csv_folder.exists():
        print(f"\n❌ ERROR: Folder '{folder_name}' not found!")
        print(f"\nPlease create the folder and add CSV files:")
        print(f"  mkdir '{folder_name}'")
        sys.exit(1)

    # Find all CSV files in folder
    csv_files = list(csv_folder.glob("*.csv"))

    if not csv_files:
        print(f"\n❌ ERROR: No CSV files found in '{folder_name}'")
        sys.exit(1)

    print(f"\n✅ Found {len(csv_files)} CSV files in '{folder_name}'")

    # Parse all CSV files
    all_data = []
    for csv_file in csv_files:
        print(f"\n📄 Processing: {csv_file.name}")
        try:
            data = parse_csv_file(csv_file, csv_file.name)
            all_data.extend(data)
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            continue

    if not all_data:
        print(f"\n❌ ERROR: No data extracted from CSV files")
        sys.exit(1)

    print(f"\n✅ Total shows extracted: {len(all_data)}")

    # Generate HTML
    print(f"\n🔨 Generating HTML dashboard...")
    try:
        html_content = generate_dashboard_html(all_data, market)

        # Write to file
        output_file = base_path / f"dashboard_{market}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"\n✅ SUCCESS! Dashboard created: {output_file.name}")
        print("\n" + "=" * 60)
        print("🎉 HOW TO USE:")
        print("=" * 60)
        print(f"1. Open '{output_file.name}' in your browser")
        print("2. That's it! Data is already loaded.")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR generating dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
