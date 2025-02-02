// Load environment variables from the .env file
require('dotenv').config();

const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const BASE_URL = "http://api.tektravels.com/SharedServices/SharedData.svc/rest";

// Retrieve credentials from the .env file
const CLIENT_ID = process.env.CLIENT_ID;
const USERNAME = process.env.USERNAME;
const PASSWORD = process.env.PASSWORD;
const END_USER_IP = process.env.END_USER_IP;

// 1. Authenticate API
app.post('/authenticate', async (req, res) => {
    try {
        const response = await axios.post(`${BASE_URL}/Authenticate`, {
            ClientId: CLIENT_ID,
            UserName: USERNAME,
            Password: PASSWORD,
            EndUserIp: END_USER_IP,
        }, { headers: { 'Content-Type': 'application/json' } });

        if (response.data.Status === 1) {
            res.json(response.data);
        } else {
            res.status(400).json(response.data);
        }
    } catch (error) {
        res.status(500).json({ error: error.response?.data || error.message });
    }
});

// 2. Fetch Country List API
app.post('/country-list', async (req, res) => {
    const { TokenId } = req.body; // TokenId should be provided from previous authentication
    try {
        const response = await axios.post(`${BASE_URL}/CountryList`, {
            ClientId: CLIENT_ID,
            EndUserIp: END_USER_IP,
            TokenId,
        }, { headers: { 'Content-Type': 'application/json' } });

        if (response.data.Status === 1) {
            res.json(response.data);
        } else {
            res.status(400).json(response.data);
        }
    } catch (error) {
        res.status(500).json({ error: error.response?.data || error.message });
    }
});

// 3. Get Destination Search Static Data API
app.post('/destination-search', async (req, res) => {
    const { TokenId, SearchType, CountryCode } = req.body;
    try {
        const response = await axios.post(`${BASE_URL}/GetDestinationSearchStaticData`, {
            ClientId: CLIENT_ID,
            EndUserIp: END_USER_IP,
            TokenId,
            SearchType,
            CountryCode,
        }, { headers: { 'Content-Type': 'application/json' } });

        if (response.data.Status === 1) {
            res.json(response.data);
        } else {
            res.status(400).json(response.data);
        }
    } catch (error) {
        res.status(500).json({ error: error.response?.data || error.message });
    }
});

// 4. Get Agency Balance API
app.post('/agency-balance', async (req, res) => {
    const { TokenAgencyId, TokenMemberId, TokenId } = req.body;
    try {
        const response = await axios.post(`${BASE_URL}/GetAgencyBalance`, {
            ClientId: CLIENT_ID,
            TokenAgencyId,
            TokenMemberId,
            EndUserIp: END_USER_IP,
            TokenId,
        }, { headers: { 'Content-Type': 'application/json' } });

        if (response.data.Status === 1) {
            res.json(response.data);
        } else {
            res.status(400).json(response.data);
        }
    } catch (error) {
        res.status(500).json({ error: error.response?.data || error.message });
    }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});