const Express = require('express');
const path = require('path');
const express = Express();
const server = require('http').Server(express);
const io = require('socket.io')(server);
const { sleep } = require('./Utils');

express.use(Express.json({ limit: '100mb' }));
express.use('/client', Express.static(path.join(__dirname, '../', 'client')));

let clientSocket = null;
io.on('connection', socket => {
  if (clientSocket) {
    console.error('ERROR: Do not refresh page from the window, always close and re-open');
    process.exit(1);
    return;
  }
  clientSocket = socket;
  console.log('client connected');
});

async function waitForClient() {
  while (!clientSocket) {
    console.log('waiting for client to connect');
    await sleep(500);
  }
  return clientSocket;
}

let actionQueue = [];
function sendAction(res) {
  const action = actionQueue.shift();
  console.log('sending action', action);
  res.set({ 'content-type': 'application/json; charset=utf-8' });
  res.json(action);

}
express.post('/', async (req, res) => {
  req.setTimeout(0);
  console.log('round', req.body.round, 'points', req.body.points);
  // res.set({char})
  if (actionQueue.length) {
    sendAction(res);
    return;
  }

  const clientSocket = await waitForClient();
  clientSocket.emit('newRound', req.body);
  clientSocket.once('actions', actions => {
    actionQueue = actions;
    sendAction(res);
  });

});



module.exports = server;
