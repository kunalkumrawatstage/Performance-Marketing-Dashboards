const fs = require('fs');
const path = require('path');

// Function to parse CSV content
function parseCSV(content) {
    const lines = content.split('\n');
    const result = [];

    for (let line of lines) {
        // Skip empty lines
        if (!line.trim()) continue;

        // Parse CSV line (handle quoted fields with commas)
        const fields = [];
        let currentField = '';
        let inQuotes = false;

        for (let i = 0; i < line.length; i++) {
            const char = line[i];

            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                fields.push(currentField.trim());
                currentField = '';
            } else {
                currentField += char;
            }
        }
        fields.push(currentField.trim());
        result.push(fields);
    }

    return result;
}

// Function to extract show data from parsed CSV
function extractShowData(parsedData, fileName) {
    console.log(`\n${'='.repeat(80)}`);
    console.log(`PARSING FILE: ${fileName}`);
    console.log('='.repeat(80));

    const shows = [];
    let headerRow = null;
    let currentWeek = '';

    for (let i = 0; i < parsedData.length; i++) {
        const row = parsedData[i];

        // Check for week range
        if (row[1] && row[1].includes('Week')) {
            currentWeek = row[1];
            console.log(`\nFound Week: ${currentWeek}`);
        }

        // Look for header row
        if (row[0] && (row[0].includes('Show_Name') || row[0].includes('showname'))) {
            headerRow = row;
            console.log(`\nHeader Row (index ${i}):`, headerRow);
            continue;
        }

        // Extract show data
        if (headerRow && row[0] && row[0].trim() !== '' && !row[0].includes('Grand Total')) {
            // Check if this is a valid data row
            const showName = row[0];
            const spends = row[1] ? row[1].replace(/,/g, '') : '0';
            const trials = row[2] ? row[2].replace(/,/g, '') : '0';

            // Skip rows that are not show data
            if (showName.includes('Insights') || showName.includes('Week_range') ||
                showName.includes('Stage TAM') || showName.includes('PAN IND')) {
                continue;
            }

            const showData = {
                fileName: fileName,
                week: currentWeek,
                showName: showName,
                spends: parseFloat(spends) || 0,
                trials: parseFloat(trials) || 0,
                rawRow: row
            };

            if (showData.spends > 0 || showData.trials > 0) {
                shows.push(showData);
                console.log(`\n  Show: ${showName}`);
                console.log(`  Spends: ${showData.spends}`);
                console.log(`  Trials: ${showData.trials}`);
            }
        }
    }

    return shows;
}

// Main test function
async function testCSVParsing() {
    const folderPath = '/Users/kunalkumrawat/GJ_Performance_Dashboard_Package/GJ Cac Solver/';

    const files = [
        'Stage_GJ- CAC SOLVER - Meta_SL-App.csv',
        'Stage_GJ- CAC SOLVER - Meta_SL-web_.csv',
        'Stage_GJ- CAC SOLVER - Google_SL-app.csv'
    ];

    let allShows = [];

    for (const file of files) {
        const filePath = path.join(folderPath, file);

        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const parsed = parseCSV(content);

            console.log(`\n\nRAW PARSED DATA FOR: ${file}`);
            console.log(`Total rows: ${parsed.length}`);
            console.log('First 10 rows:');
            parsed.slice(0, 10).forEach((row, idx) => {
                console.log(`  Row ${idx}: [${row.slice(0, 5).join(' | ')}]`);
            });

            const shows = extractShowData(parsed, file);
            allShows = allShows.concat(shows);

        } catch (error) {
            console.error(`\nERROR parsing ${file}:`, error.message);
        }
    }

    // Summary
    console.log('\n\n' + '='.repeat(80));
    console.log('SUMMARY OF ALL EXTRACTED DATA');
    console.log('='.repeat(80));

    const totalSpends = allShows.reduce((sum, show) => sum + show.spends, 0);
    const totalTrials = allShows.reduce((sum, show) => sum + show.trials, 0);
    const averageCAC = totalTrials > 0 ? totalSpends / totalTrials : 0;

    console.log(`\nTotal Shows Found: ${allShows.length}`);
    console.log(`Total Spends: ₹${totalSpends.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`);
    console.log(`Total Trials: ${totalTrials.toLocaleString('en-IN')}`);
    console.log(`Average CAC: ₹${averageCAC.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`);

    console.log('\n\nAll Shows:');
    allShows.forEach(show => {
        const cac = show.trials > 0 ? show.spends / show.trials : 0;
        console.log(`  - ${show.showName} (${show.fileName})`);
        console.log(`    Spends: ₹${show.spends.toLocaleString('en-IN')}, Trials: ${show.trials}, CAC: ₹${cac.toFixed(2)}`);
    });

    // Check for unique show names
    const uniqueShows = [...new Set(allShows.map(s => s.showName))];
    console.log(`\n\nUnique Show Names (${uniqueShows.length}):`);
    uniqueShows.forEach(name => console.log(`  - ${name}`));

    return allShows;
}

// Run the test
testCSVParsing().then(() => {
    console.log('\n\nTest completed successfully!');
}).catch(error => {
    console.error('\nTest failed:', error);
});
