const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname)));
app.use('/js', express.static(path.join(__dirname, 'js')));
app.use('/config', express.static(path.join(__dirname, 'config')));

app.get('/', (req, res) => res.sendFile(path.join(__dirname, '../code/screen1/code.html')));
app.get('/screen1', (req, res) => res.sendFile(path.join(__dirname, '../code/screen1/code.html')));
app.get('/screen2', (req, res) => res.sendFile(path.join(__dirname, '../code/screen2/code.html')));
app.get('/screen3', (req, res) => res.sendFile(path.join(__dirname, '../code/screen3/code.html')));
app.get('/screen4', (req, res) => res.sendFile(path.join(__dirname, '../code/screen4/code.html')));
app.get('/screen5', (req, res) => res.sendFile(path.join(__dirname, '../code/screen5/code.html')));

app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
