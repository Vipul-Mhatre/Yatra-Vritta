import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { withAuth } from './authMiddleware';

interface BookingRequest {
  token: string;
  traceId: string;
  flightIndex: string;
  passengers: Array<{ name: string; type: string }>;
}

interface BookingResponse {
  pnr: string;
  ticketStatus: string;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { token, traceId, flightIndex, passengers }: BookingRequest = req.body;

  if (!token || !traceId || !flightIndex || !passengers) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<BookingResponse>(
      'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Book',
      {
        TokenId: token,
        TraceId: traceId,
        ResultIndex: flightIndex,
        Passengers: passengers,
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json(response.data);
    } else {
      return res.status(400).json({ error: response.data.Error?.ErrorMessage || 'Booking Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

export default withAuth(handler);