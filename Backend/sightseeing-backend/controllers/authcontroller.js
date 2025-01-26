const axios = require('axios');
require('dotenv').config();

const API_BASE_URL = 'http://api.tektravels.com/SharedServices/SharedData.svc/rest';

// Function to authenticate and get a Token ID
exports.authenticate = async (req, res) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/Authenticate`, {
      ClientId: process.env.CLIENT_ID,
      UserName: process.env.USERNAME,
      Password: process.env.PASSWORD,
      EndUserIp: process.env.END_USER_IP,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Handle response
    if (response.data.Status === 1) {
      res.status(200).json({
        message: 'Authentication successful!',
        TokenId: response.data.TokenId,
        MemberDetails: response.data.Member,
      });
    } else {
      res.status(400).json({
        message: 'Authentication failed!',
        error: response.data.Error,
      });
    }
  } catch (error) {
    res.status(500).json({
      message: 'Internal Server Error',
      error: error.message,
    });
  }
};