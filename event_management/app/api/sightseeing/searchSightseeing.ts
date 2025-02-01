import { NextApiRequest, NextApiResponse } from "next";
import { fetchData } from "./utils/api";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method Not Allowed" });
  }

  const { EndUserIp, TokenId, TravelStartDate, CityId, CountryCode, FromDate, ToDate, AdultCount, ChildCount, PreferredCurrency } = req.body;

  if (!EndUserIp || !TokenId || !TravelStartDate || !CityId || !CountryCode || !FromDate || !ToDate || !AdultCount) {
    return res.status(400).json({ message: "Missing required parameters" });
  }

  try {
    const response = await fetchData("/SightseeingService.svc/rest/Search", {
      EndUserIp,
      TokenId,
      TravelStartDate,
      CityId,
      CountryCode,
      FromDate,
      ToDate,
      AdultCount,
      ChildCount: ChildCount || 0,
      PreferredCurrency: PreferredCurrency || "USD"
    });

    res.status(200).json(response);
  } catch (error: any) {
    res.status(500).json({ message: error.message });
  }
}