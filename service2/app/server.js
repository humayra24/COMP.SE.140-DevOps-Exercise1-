const express = require('express');
const axios = require('axios');
const os = require('os');
const fs = require('fs');

const app = express();

app.get('/status', (req, res) => {
  const timestamp = new Date().toISOString().split('.')[0] + 'Z';
  const uptime = (os.uptime() / 3600).toFixed(1); // Uptime in hours
  const freeDiskMB = Math.floor(os.freemem() / (1024 * 1024)); 
   const record = `Timestamp2 ${timestamp}: uptime ${uptime} hours, free disk in root: ${freeDiskMB} MBytes`;


  // Log to Storage 
  axios.post('http://storage:5050/log', record, { headers: { 'Content-Type': 'text/plain' } })
    .then(() => console.log('Logged to Storage'))
    .catch(err => console.error('Storage log failed:', err));

  // Log to vStorage volume
  fs.appendFileSync('/vstorage', record + '\n', 'utf-8');

  res.set('Content-Type', 'text/plain').send(record);
});

app.listen(3000, () => console.log('Service2 running on port 3000'));