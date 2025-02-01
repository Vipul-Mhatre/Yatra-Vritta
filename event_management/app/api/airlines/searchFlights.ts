import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { withAuth } from './authMiddleware';

interface SearchRequest {
  token: string;
  origin: string;
  destination: string;
  travelDate: string;
  returnDate?: string;
  cabinClass: string;
  adults: number;
  children: number;
  infants: number;
}

interface SearchResponse {
  traceId: string;
  itineraries: Array<{ flightIndex: string; fare: object; details: object }>;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const {
    token,
    origin,
    destination,
    travelDate,
    returnDate,
    cabinClass,
    adults,
    children,
    infants,
  }: SearchRequest = req.body;

  if (!token || !origin || !destination || !travelDate || !cabinClass || !adults) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<SearchResponse>(
      'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Search',
      {
        EndUserIp: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
        TokenId: token,
        AdultCount: adults,
        ChildCount: children,
        InfantCount: infants,
        JourneyType: returnDate ? 2 : 1,
        Segments: [
          {
            Origin: origin,
            Destination: destination,
            PreferredDepartureTime: travelDate,
            CabinClass: cabinClass,
          },
          returnDate && {
            Origin: destination,
            Destination: origin,
            PreferredDepartureTime: returnDate,
            CabinClass: cabinClass,
          },
        ].filter(Boolean),
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json(response.data);
    } else {
      return res.status(400).json({ error: response.data.Error?.ErrorMessage || 'Search Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

export default withAuth(handler);