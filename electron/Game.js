const path = require('path');
const child_process = require('child_process');
const { sleep } = require('./Utils');

const gamePath = (() => {
  const binariesFolder = path.join(__dirname, '../', 'game_binaries');
  const binaryName = process.platform == 'win32' ? 'ic20_windows.exe' : 'ic20_linux';
  return path.join(binariesFolder, binaryName);
})();
const gameArgs = ['-t', '0'];


/**
 * @property {ChildProcessWithoutNullStreams} game
 */
class GameProcess {
  constructor() {
    this.game = null;
    this._gameExit = this._gameExit.bind(this);
  }

  start() {
    const pro = child_process.spawn(gamePath, gameArgs);
    pro.on('exit', this._gameExit);
    pro.stdout.on('data', function() {}); // clear buffer
    pro.stderr.on('data', function() {}); // clear buffer
    pro.stdin.on('data', function() {}); // clear buffer
    this.game = pro;
  }

  _gameExit(code, signal) {
    this.game = null;
    console.log('exited with', code, signal);
    this.start();
  }

  async restart() {
    if (this.game)
      this.game.kill();

    //FIXME: hack to wait for the process to be terminated
    while (this.game)
      await sleep(200);

    this.start();
  }
}

module.exports = new GameProcess();
