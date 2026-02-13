#!/bin/bash
# Generate Haryanvi (HR) Market Dashboard

echo "=========================================="
echo "📊 Generating Haryanvi Market Dashboard"
echo "=========================================="

# Check if HR folder exists
if [ ! -d "HR Cac Solver" ]; then
    echo "❌ ERROR: 'HR Cac Solver' folder not found!"
    echo ""
    echo "Please create the folder and add your CSV files:"
    echo "  1. mkdir 'HR Cac Solver'"
    echo "  2. Copy your HR CSV files into that folder"
    echo ""
    exit 1
fi

# Check if CSV files exist
if ! ls "HR Cac Solver"/*.csv 1> /dev/null 2>&1; then
    echo "❌ ERROR: No CSV files found in 'HR Cac Solver' folder!"
    echo ""
    echo "Please add your Haryanvi CSV files to the folder."
    echo ""
    exit 1
fi

echo "✅ Found HR Cac Solver folder"
echo "✅ Found CSV files"
echo ""

# Temporarily replace GJ folder reference in Python script
echo "🔨 Generating dashboard..."

# Create a temporary modified script
sed 's/GJ Cac Solver/HR Cac Solver/g' generate_dashboard.py > temp_hr_generate.py
sed -i '' 's/Gujarati Market/Haryanvi Market/g' temp_hr_generate.py
sed -i '' 's/Gujarati (GJ)/Haryanvi (HR)/g' temp_hr_generate.py

# Run the modified script
python3 temp_hr_generate.py

# Rename output
if [ -f "dashboard_generated.html" ]; then
    mv dashboard_generated.html dashboard_haryanvi.html
    echo ""
    echo "✅ SUCCESS! Haryanvi dashboard created: dashboard_haryanvi.html"
    echo ""
    echo "🎉 To view:"
    echo "   open dashboard_haryanvi.html"
else
    echo "❌ Error: Dashboard generation failed"
fi

# Cleanup
rm -f temp_hr_generate.py

echo "=========================================="
