import { NextApiRequest, NextApiResponse } from "next";
import { connectToDatabase } from "@/lib/mongodb";
import { Resume } from "../../types";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "GET") {
    return res.status(405).json({ message: "Method not allowed" });
  }

  try {
    const { db } = await connectToDatabase();
    const resumes = await db.collection("resumes").find({}).toArray();

    return res.status(200).json(resumes);
  } catch (error) {
    console.error("Database error:", error);
    return res.status(500).json({ message: "Error connecting to database" });
  }
}
