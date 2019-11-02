const Express = require('express');

const app = Express();
app.use(Express.json({ limit: '50mb' }));

app.post('/', (req, res) => {
  res.send(JSON.stringify({ 'type': 'endRound' }));
});

app.listen(50123, () =>
  console.log('Server listening on port 50123!'),
);
