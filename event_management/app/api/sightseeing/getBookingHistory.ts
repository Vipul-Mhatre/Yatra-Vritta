import { NextApiRequest, NextApiResponse } from "next";
import { fetchData } from "./utils/api";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method Not Allowed" });
  }

  const { ClientId, TokenId, EndUserIp, TokenAgencyId, TokenMemberId } = req.body;

  if (!ClientId || !TokenId || !EndUserIp || !TokenAgencyId || !TokenMemberId) {
    return res.status(400).json({ message: "Missing required parameters" });
  }

  try {
    const response = await fetchData("/SightseeingService.svc/rest/GetBookingHistory", {
      ClientId,
      TokenId,
      EndUserIp,
      TokenAgencyId,
      TokenMemberId
    });

    res.status(200).json(response);
  } catch (error: any) {
    res.status(500).json({ message: error.message });
  }
}