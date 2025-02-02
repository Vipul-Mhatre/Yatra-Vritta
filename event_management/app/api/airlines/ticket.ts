import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { withAuth } from './authMiddleware';

interface TicketRequest {
  token: string;
  traceId: string;
  pnr: string;
  bookingId: string;
}

interface TicketResponse {
  ticketNumber: string;
  status: string;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { token, traceId, pnr, bookingId }: TicketRequest = req.body;

  if (!token || !traceId || !pnr || !bookingId) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<TicketResponse>(
      'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Ticket',
      {
        TokenId: token,
        TraceId: traceId,
        PNR: pnr,
        BookingId: bookingId,
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json(response.data);
    } else {
      return res.status(400).json({ error: response.data.Error?.ErrorMessage || 'Ticket Issuance Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

export default withAuth(handler);