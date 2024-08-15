const port = 3000;
const express = require('express')
const app = express();
const http = require('http');
const http_server = http.createServer(app).listen(port);
const http_io = require('socket.io')(http_server);

const fs = require('fs');
const {spawn, fork} = require('child_process');

const path_a = 'pipe_a';
const path_b = 'pipe_b';

let fifo_b = spawn('mkfifo', [path_b]);

fifo_b.on('exit', function(status) {
    console.log("Created Pipe B");

    const fd = fs.openSync(path_b, 'r');
    let fifoRs = fs.createReadStream(null, {fd});
    let fifoWs = fs.createWriteStream(path_a);

    console.log('Ready to write')

    setInterval(() => {
        console.log("----- log -----");
        fifoWs.write(`${new Date().toISOString()}`);
        latency = new Date();
        const data = fifoRs.read();
        if (data) {
            sent_time = new Date(data.toString());
        } else {
            // Handle the case where data is null or undefined
            sent_time = new Date(); // or any default value you prefer
        }

        console.log('Latency: ', latency - sent_time);

    })
});


app.set('view engine', 'ejs');
app.use(express.static('public'));

app.get('/start' , (req, res) => {
    res.render('start.ejs');
});

app.get('/', (req, res) => {
    res.send(value)
});

