import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const BASE_URL = "http://api.tektravels.com/SharedServices";

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" }
});

export const fetchData = async (endpoint: string, data: any) => {
  try {
    const response = await apiClient.post(endpoint, data);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.ErrorMessage || "API request failed");
  }
};