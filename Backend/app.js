require('dotenv').config();
const express = require('express');
const app = express();
const mongoConnect = require('./db');
const cors = require('cors');
const routes = require('./routes/router');
const port = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());
app.use(routes); // yaha pe routes daalenge thodi der me

mongoConnect(process.env.MONGO_URL).then(() => {
    app.listen(port, () => {
        console.log(`Server is listening at http://localhost:${port}`);
    });
}).catch((err) => {
    console.error(err);
    process.exit(1);
});