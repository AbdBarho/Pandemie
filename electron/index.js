const Game = require('./Game');
const server = require('./Socket');

server.listen(50123, () => {
  require('./Window');
  console.log('Server listening on port 50123!');
  setTimeout(() => Game.start(), 1000);
});
