require('dotenv').config();
const express = require('express');
const app = express();
const mongoConnect = require('./db');
const cors = require('cors');
const medicalRoutes = require('./routes/Medical_routes');
const miceRoutes = require('./routes/MICE_routes');
const wedRoutes = require('./routes/Wedding_routes');
const userRoutes = require('./routes/User_routes');
const port = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());

//routes

app.use("/api/user", userRoutes);

//routes

mongoConnect(process.env.MONGO_URL).then(() => {
    app.listen(port, () => {
        console.log(`Server is listening at http://localhost:${port}`);
    });
}).catch((err) => {
    console.error(err);
    process.exit(1);
});