import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { withAuth } from './authMiddleware';

interface FareRulesRequest {
  token: string;
  traceId: string;
  flightIndex: string;
}

interface FareRulesResponse {
  fareRules: Array<{ rule: string; baggage: string }>;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { token, traceId, flightIndex }: FareRulesRequest = req.body;

  if (!token || !traceId || !flightIndex) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<FareRulesResponse>(
      'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/FareRules',
      {
        TokenId: token,
        TraceId: traceId,
        ResultIndex: flightIndex,
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json(response.data);
    } else {
      return res.status(400).json({ error: response.data.Error?.ErrorMessage || 'Fare Rules Fetch Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

export default withAuth(handler);