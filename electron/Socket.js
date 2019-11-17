const Express = require('express');
const path = require('path');
const express = Express();
const server = require('http').Server(express);
const io = require('socket.io')(server);
const fs = require('fs');
const mkdirp = require('mkdirp');
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

const GAMES_DATA_FOLDER = path.join(__dirname, '../', 'collected_data', 'games');
mkdirp.sync(GAMES_DATA_FOLDER);


let currentGameFolder = '';
express.post('/', async (req, res) => {
  req.setTimeout(0);
  const gameState = req.body;
  console.log('round', gameState.round, 'points', gameState.points);
  if (actionQueue.length) {
    sendAction(res);
    return;
  }

  if (gameState.round === 1) {
    currentGameFolder = path.join(GAMES_DATA_FOLDER, Date.now().toString());
    mkdirp.sync(currentGameFolder);
  }

  fs.writeFileSync(
    path.join(currentGameFolder, gameState.round + '.json'),
    JSON.stringify(gameState, null, 2)
  );

  const clientSocket = await waitForClient();
  clientSocket.emit('newRound', gameState);
  clientSocket.once('actions', actions => {
    actionQueue = actions;
    sendAction(res);
  });

});



module.exports = server;
