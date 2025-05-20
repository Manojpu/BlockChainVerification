import React, { useState, useEffect } from "react";
import { Resume } from "@/types";
import ResumeCard from "@/components/dashboard/ResumeCard";
import axios from "axios";

const HomePage: React.FC = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/resumes");
      setResumes(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch resumes. Please try again later.");
      console.error("Error fetching resumes:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (
    resumeId: string,
    type: "education" | "work",
    index: number,
    action: "confirm" | "reject"
  ) => {
    try {
      await axios.post("/api/verify", {
        resumeId,
        type,
        index,
        action,
      });

      // Refresh the resumes after verification
      fetchResumes();
    } catch (err) {
      setError("Failed to update verification status. Please try again.");
      console.error("Error verifying qualification:", err);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{error}</p>
          <button
            onClick={fetchResumes}
            className="mt-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Resume Verification Dashboard</h1>

      {resumes.length === 0 ? (
        <div className="bg-gray-100 p-6 rounded-lg text-center">
          <p className="text-gray-700">No resumes found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resumes.map((resume) => (
            <ResumeCard
              key={resume._id}
              resume={resume}
              onVerify={handleVerify}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default HomePage;
