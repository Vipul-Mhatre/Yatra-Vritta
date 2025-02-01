import { NextApiRequest, NextApiResponse } from "next";
import { fetchData } from "./utils/api";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method Not Allowed" });
  }

  const { ClientId, TokenId, TokenAgencyId, TokenMemberId, EndUserIp } = req.body;

  if (!ClientId || !TokenId || !TokenAgencyId || !TokenMemberId || !EndUserIp) {
    return res.status(400).json({ message: "Missing required parameters" });
  }

  try {
    const response = await fetchData("/SharedServices/SharedData.svc/rest/Logout", {
      ClientId,
      TokenId,
      TokenAgencyId,
      TokenMemberId,
      EndUserIp
    });

    res.status(200).json(response);
  } catch (error: any) {
    res.status(500).json({ message: error.message });
  }
}