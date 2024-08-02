const fs = require('fs');
const csv = require('csv-parser');

const results = [];

fs.createReadStream('/home/frigiel/Documents/VSCODE/Django/findword/findapp/dictionary/fr/noun.csv')
    .pipe(csv())
    .on('data', (data) => {
        results.push(data);
    })
    .on('end', () => {
        console.log(results);
        // Process the data here
    });