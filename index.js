const Express = require('express');
const fs = require('fs');

const pathogenDict = require('./pathogen.json');
console.log(Object.keys(pathogenDict), Object.keys(pathogenDict).length);

const app = Express();
app.use(Express.json({ limit: '50mb' }));

app.post('/', (req, res) => {
  // console.log(req);
  const data = req.body;
  data.cities = Object.values(data.cities).map(el => el.events).filter(e => e);
  const events = data.events.filter(e => e.type === 'pathogenEncountered');
  const hasChanged = events.map(e => addPathogen(e.pathogen)).some(a => a);
  if (hasChanged) {
    fs.writeFileSync('./pathogen.json', JSON.stringify(pathogenDict, null, 2));
    console.log('new pathogen...');
  }

  // console.assert(events.every(e => e.round === 1), 'Pathogen not in round 1', events);
  res.send(JSON.stringify({ "type": "endRound" }));
});

app.listen(50123, () =>
  console.log('Example app listening on port 50123!'),
);

function addPathogen(pathogen) {
  const name = pathogen.name;
  delete pathogen.name;
  if (pathogenDict.hasOwnProperty(name))
    return false;

  pathogenDict[name] = pathogen;
  return true;
}
