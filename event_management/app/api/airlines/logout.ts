import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

interface LogoutResponse {
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

  const { token, agencyId, memberId } = req.body;

  if (!token || !agencyId || !memberId) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<LogoutResponse>(
      'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Logout',
      {
        ClientId: process.env.CLIENT_ID,
        TokenAgencyId: agencyId,
        TokenMemberId: memberId,
        EndUserIp: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
        TokenId: token,
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json({ message: 'Logout Successful' });
    } else {
      return res.status(401).json({ error: response.data.Error?.ErrorMessage || 'Logout Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}