
import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { withAuth } from './authMiddleware';

interface AgencyBalanceRequest {
  token: string;
  agencyId: string;
  memberId: string;
}

interface AgencyBalanceResponse {
  cashBalance: number;
  creditBalance: number;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { token, agencyId, memberId }: AgencyBalanceRequest = req.body;

  if (!token || !agencyId || !memberId) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<AgencyBalanceResponse>(
      'http://api.tektravels.com/SharedServices/SharedData.svc/rest/GetAgencyBalance',
      {
        TokenId: token,
        TokenAgencyId: agencyId,
        TokenMemberId: memberId,
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json(response.data);
    } else {
      return res.status(400).json({ error: response.data.Error?.ErrorMessage || 'Balance Fetch Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

export default withAuth(handler);