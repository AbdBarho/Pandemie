const Express = require('express');
const path = require('path');
const express = Express();
const server = require('http').Server(express);
const io = require('socket.io')(server);
const { sleep } = require('./Utils');

express.use(Express.json({ limit: '100mb' }));
express.use('/client', Express.static(path.join(__dirname, '../', 'client')));

let clientSocket = null;
io.on('connection', socket => (clientSocket = socket) && console.log('client connected'));

async function waitForClient() {
  while (!clientSocket) {
    console.log('waiting for client to connect');
    await sleep(500);
  }
  return clientSocket;
}


express.post('/', async (req, res) => {
  req.setTimeout(0);
  const clientSocket = await waitForClient();
  clientSocket.once('actions', actions => res.send(JSON.stringify(actions)));
  clientSocket.emit('newRound', req.body);
});

module.exports = server;
