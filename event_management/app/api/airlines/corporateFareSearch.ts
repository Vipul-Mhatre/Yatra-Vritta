import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { withAuth } from './authMiddleware';

interface CorporateFareRequest {
  token: string;
  corporateCodes: Array<{ PCC: string; AirlineKeys: Array<{ Airline: string; CorporateCode: string }> }>;
  origin: string;
  destination: string;
  travelDate: string;
  cabinClass: string;
  adults: number;
  children: number;
  infants: number;
}

interface CorporateFareResponse {
  traceId: string;
  itineraries: Array<{ flightIndex: string; fare: object; details: object }>;
  Status: number;
  Error?: { ErrorCode: number; ErrorMessage: string };
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { token, corporateCodes, origin, destination, travelDate, cabinClass, adults, children, infants }: CorporateFareRequest = req.body;

  if (!token || !corporateCodes || !origin || !destination || !travelDate || !cabinClass || !adults) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  try {
    const response = await axios.post<CorporateFareResponse>(
      'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Search',
      {
        TokenId: token,
        CorporateCodes: corporateCodes,
        EndUserIp: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
        AdultCount: adults,
        ChildCount: children,
        InfantCount: infants,
        JourneyType: 1,
        Segments: [{
          Origin: origin,
          Destination: destination,
          PreferredDepartureTime: travelDate,
          CabinClass: cabinClass,
        }],
      }
    );

    if (response.data.Status === 1) {
      return res.status(200).json(response.data);
    } else {
      return res.status(400).json({ error: response.data.Error?.ErrorMessage || 'Corporate Fare Search Failed' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

export default withAuth(handler);