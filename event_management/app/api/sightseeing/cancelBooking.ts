import { NextApiRequest, NextApiResponse } from "next";
import { fetchData } from "./utils/api";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method Not Allowed" });
  }

  const { ClientId, TokenId, EndUserIp, BookingId } = req.body;

  if (!ClientId || !TokenId || !EndUserIp || !BookingId) {
    return res.status(400).json({ message: "Missing required parameters" });
  }

  try {
    const response = await fetchData("/SightseeingService.svc/rest/Cancel", {
      ClientId,
      TokenId,
      EndUserIp,
      BookingId
    });

    res.status(200).json(response);
  } catch (error: any) {
    res.status(500).json({ message: error.message });
  }
}