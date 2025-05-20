import { MongoClient } from "mongodb";

const MONGODB_URI =
  process.env.MONGODB_URI || "mongodb://localhost:27017/resume_verification";
const MONGODB_DB = process.env.MONGODB_DB || "resume_verification";

let cachedClient: MongoClient | null = null;
let cachedDb: any = null;

export async function connectToDatabase() {
  // If we have the cached connection, use it
  if (cachedClient && cachedDb) {
    return { client: cachedClient, db: cachedDb };
  }

  // Connect to MongoDB
  const client = await MongoClient.connect(MONGODB_URI);
  const db = client.db(MONGODB_DB);

  // Cache the connection
  cachedClient = client;
  cachedDb = db;

  return { client, db };
}
