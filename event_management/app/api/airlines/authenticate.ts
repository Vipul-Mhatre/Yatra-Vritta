import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

interface AuthResponse {
  TokenId: string;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const response = await axios.post<AuthResponse>(
      'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Authenticate',
      {
        ClientId: process.env.CLIENT_ID,
        UserName: process.env.API_USERNAME,
        Password: process.env.API_PASSWORD,
        EndUserIp: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json({ token: response.data.TokenId });
    } else {
      return res.status(401).json({ error: response.data.Error?.ErrorMessage || 'Authentication Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}