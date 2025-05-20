import { NextApiRequest, NextApiResponse } from "next";
import { connectToDatabase } from "@/lib/mongodb";
import { ObjectId } from "mongodb";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method not allowed" });
  }

  const { resumeId, type, index, action } = req.body;

  if (!resumeId || !type || index === undefined || !action) {
    return res.status(400).json({ message: "Missing required fields" });
  }

  try {
    const { db } = await connectToDatabase();

    // Construct the update field path based on type
    const fieldPath =
      type === "education"
        ? `education.${index}.verified`
        : `work_experience.${index}.verified`;

    // Create the update operation
    const updateOperation =
      action === "confirm"
        ? { $set: { [fieldPath]: true } }
        : { $set: { [fieldPath]: false } };

    // Update the resume document
    const result = await db
      .collection("resumes")
      .updateOne({ resume_id: resumeId }, updateOperation);

    if (result.modifiedCount === 0) {
      return res
        .status(404)
        .json({ message: "Resume not found or no changes made" });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error("Database error:", error);
    return res
      .status(500)
      .json({ message: "Error updating verification status" });
  }
}
