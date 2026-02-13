#!/usr/bin/env node

/**
 * CSV Parser Test Script
 * This script reads the actual CSV files and tests parsing logic
 * to identify what data can be extracted successfully.
 */

const fs = require('fs');
const path = require('path');

// File paths
const CSV_FOLDER = path.join(__dirname, 'GJ Cac Solver');
const CSV_FILES = [
    'Stage_GJ- CAC SOLVER - Meta_SL-App.csv',
    'Stage_GJ- CAC SOLVER - Meta_SL-web_.csv',
    'Stage_GJ- CAC SOLVER - Google_SL-app.csv'
];

// Configuration - matches dashboard config
const CONFIG = {
    metaColumns: {
        spend: ['Spends_GST', 'Spend'],
        trials: ['af_start_trial', 'Trial_web', 'Trials', 'trial'],
        cac: ['Mandate_CAC', 'CAC'],
        ir: ['AF_IR%', 'IR%', 'IR'],
        tr: ['TR%_AF', 'AF_TR%', 'TR%', 'TR'],
        tcr: ['TCR_D0', 'TCR%', 'TCR'],
        ctr: ['CTR', 'CTR%']
    },
    googleColumns: {
        spend: ['Spends_GST', 'Spend'],
        trials: ['start_trial_d0', 'Trials', 'trial'],
        cac: ['CP_AF_CPT_D0', 'CAC'],
        ir: ['AF_IR%', 'IR%', 'IR'],
        tr: ['AF_TR%', 'TR%', 'TR'],
        tcr: ['AF_TCR%', 'TCR%', 'TCR'],
        ctr: ['CTR', 'CTR%']
    }
};

/**
 * Parse CSV line respecting quoted fields
 */
function parseCSVLine(line) {
    const result = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
        const char = line[i];

        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            result.push(current.trim());
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current.trim()); // Push last field

    return result;
}

/**
 * CSV parser that handles quoted fields with commas
 * Also handles CSVs with metadata rows before headers
 */
function parseCSV(content) {
    const lines = content.split(/\r?\n/);
    const result = [];

    if (lines.length === 0) return result;

    // Find the header row (contains Show_Name or showname)
    let headerIndex = -1;
    let headers = [];

    for (let i = 0; i < Math.min(10, lines.length); i++) {
        const line = lines[i];
        if (line.includes('Show_Name') || line.includes('showname')) {
            headers = parseCSVLine(line);
            headerIndex = i;
            console.log(`  ✓ Found headers at line ${i + 1}: ${headers.slice(0, 5).join(', ')}...`);
            break;
        }
    }

    if (headerIndex === -1) {
        console.warn('  ⚠️  No header row found (looking for Show_Name or showname)');
        return result;
    }

    // Parse data lines starting after header
    for (let i = headerIndex + 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line || line === ','.repeat(headers.length - 1)) continue; // Skip empty lines

        const values = parseCSVLine(line);
        const row = {};

        for (let j = 0; j < headers.length; j++) {
            if (headers[j]) {
                row[headers[j]] = values[j] || '';
            }
        }

        result.push(row);
    }

    return result;
}

/**
 * Parse number values (removes commas and percentages)
 */
function parseNumber(value) {
    if (!value) return 0;
    const cleaned = String(value).replace(/,/g, '').replace(/%/g, '').trim();
    return parseFloat(cleaned) || 0;
}

/**
 * Find first matching column from array of possible names
 */
function findColumn(row, possibleNames) {
    for (const name of possibleNames) {
        if (name in row && row[name] != null && row[name] !== '') {
            return row[name];
        }
    }
    return null;
}

/**
 * Normalize CSV data to standard format
 */
function normalizeData(data, filename = '') {
    if (!data || data.length === 0) {
        console.warn('⚠️  Empty data array');
        return [];
    }

    console.log(`📋 Processing ${data.length} raw rows from ${filename}`);

    // Filter out empty rows and header rows
    const validRows = data.filter(row => {
        const showName = row.Show_Name || row['Show_Name - APP'] || row.Show || row.show || row.showname;

        if (!showName || !showName.trim()) return false;
        if (showName === 'Grand Total') return false;
        if (String(showName).includes('Week_range')) return false;
        if (String(showName).includes('Insights')) return false;
        if (String(showName).includes('Week (')) return false;
        if (String(showName).toLowerCase() === 'values') return false;

        return true;
    });

    console.log(`✓ ${validRows.length} valid rows after filtering`);

    if (validRows.length === 0) {
        console.warn('⚠️  No valid rows found after filtering');
        return [];
    }

    const firstRow = validRows[0];
    console.log(`🔍 Columns found: ${Object.keys(firstRow).slice(0, 10).join(', ')}...`);

    // Detect if Meta or Google based on column presence
    const isMeta = 'af_start_trial' in firstRow || 'Trial_web' in firstRow || 'Mandate_CAC' in firstRow;
    const channel = isMeta ? 'meta' : 'google';
    console.log(`📍 Detected channel: ${channel}`);

    // Detect platform from filename
    const platform = filename.toLowerCase().includes('web') ? 'web' : 'app';
    console.log(`📍 Detected platform: ${platform}`);

    const cols = isMeta ? CONFIG.metaColumns : CONFIG.googleColumns;
    const normalized = [];

    for (let i = 0; i < validRows.length; i++) {
        const row = validRows[i];

        // Get show name
        const showName = (row.Show_Name || row['Show_Name - APP'] || row.Show || row.show || row.showname || 'Unknown').trim();

        // Find values using flexible column matching
        const spendValue = findColumn(row, cols.spend);
        const trialsValue = findColumn(row, cols.trials);
        const cacValue = findColumn(row, cols.cac);
        const irValue = findColumn(row, cols.ir);
        const trValue = findColumn(row, cols.tr);
        const tcrValue = findColumn(row, cols.tcr);
        const ctrValue = findColumn(row, cols.ctr);

        // Parse all values
        const spend = parseNumber(spendValue);
        let cac = parseNumber(cacValue);
        let trials = Math.round(parseNumber(trialsValue));

        // Calculate trials from spend/CAC if trials column missing or zero
        if ((!trials || trials === 0) && spend > 0 && cac > 0) {
            trials = Math.round(spend / cac);
            console.log(`  💡 Calculated trials for ${showName}: ${trials} (from spend ${spend} / CAC ${cac})`);
        }

        // Calculate CAC from spend/trials if CAC is missing or zero
        if ((!cac || cac === 0) && spend > 0 && trials > 0) {
            cac = parseFloat((spend / trials).toFixed(2));
            console.log(`  💡 Calculated CAC for ${showName}: ${cac} (from spend ${spend} / trials ${trials})`);
        }

        const normalizedRow = {
            channel: channel,
            platform: platform,
            show: showName,
            spend: spend,
            trials: trials,
            cac: cac,
            ir: parseNumber(irValue),
            tr: parseNumber(trValue),
            tcr: parseNumber(tcrValue),
            ctr: parseNumber(ctrValue)
        };

        // Only include if we have meaningful data
        if (spend > 0 || trials > 0) {
            normalized.push(normalizedRow);
        }
    }

    console.log(`✅ Normalized ${normalized.length} rows with data\n`);
    return normalized;
}

/**
 * Calculate overall metrics
 */
function calculateMetrics(data) {
    if (!data || !data.length) return null;

    let totalSpend = 0, totalTrials = 0, irSum = 0, trSum = 0, tcrSum = 0, ctrSum = 0, count = 0;

    data.forEach(row => {
        totalSpend += parseFloat(row.spend) || 0;
        totalTrials += parseInt(row.trials) || 0;
        irSum += parseFloat(row.ir) || 0;
        trSum += parseFloat(row.tr) || 0;
        tcrSum += parseFloat(row.tcr) || 0;
        ctrSum += parseFloat(row.ctr) || 0;
        count++;
    });

    const cac = totalTrials > 0 ? totalSpend / totalTrials : 0;

    return {
        totalSpend: totalSpend.toFixed(0),
        totalTrials,
        cac: cac.toFixed(2),
        ir: (irSum / count).toFixed(2),
        tr: (trSum / count).toFixed(2),
        tcr: (tcrSum / count).toFixed(2),
        ctr: (ctrSum / count).toFixed(2)
    };
}

/**
 * Main test function
 */
function runTests() {
    console.log('\n' + '='.repeat(80));
    console.log('CSV PARSING TEST SCRIPT');
    console.log('='.repeat(80) + '\n');

    const allData = [];
    const fileResults = [];

    for (const filename of CSV_FILES) {
        const filePath = path.join(CSV_FOLDER, filename);

        console.log('━'.repeat(80));
        console.log(`📄 Testing: ${filename}`);
        console.log('━'.repeat(80));

        if (!fs.existsSync(filePath)) {
            console.error(`❌ File not found: ${filePath}\n`);
            fileResults.push({ filename, success: false, error: 'File not found' });
            continue;
        }

        try {
            // Read file
            const content = fs.readFileSync(filePath, 'utf-8');
            console.log(`✓ File read successfully (${content.length} bytes)`);

            // Parse CSV
            const rawData = parseCSV(content);
            console.log(`✓ CSV parsed: ${rawData.length} rows`);

            if (rawData.length > 0) {
                console.log(`✓ Sample columns: ${Object.keys(rawData[0]).slice(0, 5).join(', ')}...`);
            }

            // Normalize data
            const normalizedData = normalizeData(rawData, filename);

            if (normalizedData.length > 0) {
                console.log('\n📊 Sample Normalized Data (first 3 rows):');
                console.log(JSON.stringify(normalizedData.slice(0, 3), null, 2));

                // Add to combined dataset
                allData.push(...normalizedData);

                fileResults.push({
                    filename,
                    success: true,
                    rowCount: normalizedData.length,
                    data: normalizedData
                });
            } else {
                console.warn('⚠️  No data extracted from this file');
                fileResults.push({
                    filename,
                    success: false,
                    error: 'No data extracted'
                });
            }
        } catch (error) {
            console.error(`❌ Error processing file: ${error.message}`);
            fileResults.push({
                filename,
                success: false,
                error: error.message
            });
        }

        console.log('\n');
    }

    // Summary
    console.log('━'.repeat(80));
    console.log('SUMMARY');
    console.log('━'.repeat(80));
    console.log(`\n📈 Files Processed: ${CSV_FILES.length}`);
    console.log(`✅ Successful: ${fileResults.filter(r => r.success).length}`);
    console.log(`❌ Failed: ${fileResults.filter(r => !r.success).length}`);
    console.log(`📊 Total Rows Extracted: ${allData.length}\n`);

    if (allData.length > 0) {
        console.log('━'.repeat(80));
        console.log('CALCULATED METRICS (COMBINED DATA)');
        console.log('━'.repeat(80) + '\n');

        const metrics = calculateMetrics(allData);

        console.log('Overall Performance:');
        console.log(`  💰 Total Spend: ₹${parseFloat(metrics.totalSpend).toLocaleString('en-IN')}`);
        console.log(`  🎯 Total Trials: ${metrics.totalTrials.toLocaleString('en-IN')}`);
        console.log(`  📊 Average CAC: ₹${metrics.cac}`);
        console.log(`  📈 CTR: ${metrics.ctr}%`);
        console.log(`  📲 IR (Install Rate): ${metrics.ir}%`);
        console.log(`  🎬 TR (Trial Rate): ${metrics.tr}%`);
        console.log(`  ⚠️  TCR (Trial Churn): ${metrics.tcr}%\n`);

        // Show-wise breakdown
        console.log('Show-wise Performance:');
        const showMap = {};
        allData.forEach(row => {
            if (!showMap[row.show]) {
                showMap[row.show] = {
                    spend: 0,
                    trials: 0,
                    shows: []
                };
            }
            showMap[row.show].spend += row.spend;
            showMap[row.show].trials += row.trials;
            showMap[row.show].shows.push(row);
        });

        Object.keys(showMap).forEach(show => {
            const data = showMap[show];
            const cac = data.trials > 0 ? (data.spend / data.trials).toFixed(2) : 0;
            console.log(`  • ${show}: ₹${data.spend.toLocaleString('en-IN')} spend, ${data.trials} trials, ₹${cac} CAC`);
        });

        console.log('\n');
    }

    console.log('━'.repeat(80));
    console.log('TEST COMPLETE');
    console.log('━'.repeat(80) + '\n');

    // Write results to JSON file
    const outputPath = path.join(__dirname, 'test_results.json');
    fs.writeFileSync(outputPath, JSON.stringify({
        timestamp: new Date().toISOString(),
        fileResults,
        allData,
        metrics: allData.length > 0 ? calculateMetrics(allData) : null
    }, null, 2));
    console.log(`📝 Detailed results saved to: ${outputPath}\n`);

    // Return success status
    return allData.length > 0;
}

// Run tests
const success = runTests();
process.exit(success ? 0 : 1);
