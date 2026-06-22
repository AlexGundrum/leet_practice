const fs = require('fs');
let algorithms = [];
const batches = [
    'enriched_batch_0_14.json',
    'enriched_batch_15_29.json',
    'enriched_batch_30_44.json',
    'enriched_batch_45_59.json',
    'enriched_batch_60_72.json'
];
for (const b of batches) {
    try {
        const data = JSON.parse(fs.readFileSync(b, 'utf8'));
        algorithms = algorithms.concat(data);
    } catch(e) {
        console.error("Error reading " + b + ": " + e);
        process.exit(1);
    }
}
fs.writeFileSync('algorithms.json', JSON.stringify(algorithms, null, 2));
console.log('Merged ' + algorithms.length + ' algorithms successfully!');
