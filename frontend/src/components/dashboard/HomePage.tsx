import React, { useState, useEffect } from "react";
import { Resume } from "@/types";
import ResumeCard from "@/components/dashboard/ResumeCard";
import { mockResumes } from "@/definitions/mockdata";

const HomePage: React.FC = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Simulate API fetch delay
    const timer = setTimeout(() => {
      setResumes(mockResumes);
      setLoading(false);
    }, 800);

    return () => clearTimeout(timer);
  }, []);

  const handleVerify = async (
    resumeId: string,
    type: "education" | "work",
    index: number,
    action: "confirm" | "reject"
  ) => {
    try {
      // Clone the current resumes array
      const updatedResumes = [...resumes];

      // Find the resume with the matching ID
      const resumeIndex = updatedResumes.findIndex(
        (resume) => resume.resume_id === resumeId
      );

      if (resumeIndex !== -1) {
        const resume = updatedResumes[resumeIndex];
        const items =
          type === "education" ? resume.education : resume.work_experience;

        if (index >= 0 && index < items.length) {
          const item = items[index];

          if (action === "confirm") {
            // Mark as verified and use sent data as actual if actual is null
            item.verified = true;

            if (
              type === "education" &&
              "degree" in item.actual &&
              !item.actual.degree
            ) {
              item.actual.degree = (item.send as any).degree;
              item.actual.institution = (item.send as any).institution;
            } else if (
              type === "work" &&
              "position" in item.actual &&
              !item.actual.position
            ) {
              item.actual.position = (item.send as any).position;
              item.actual.company = (item.send as any).company;
            }
          } else if (action === "reject") {
            // Mark as not verified
            item.verified = false;
          }

          // Check overall verification status
          const allEducationVerified = resume.education.every(
            (item) => item.verified
          );
          const allWorkVerified = resume.work_experience.every(
            (item) => item.verified
          );

          if (allEducationVerified && allWorkVerified) {
            resume.is_verified = "VERIFIED";
          } else {
            // If any item is explicitly rejected, mark as rejected
            const anyRejected = [
              ...resume.education,
              ...resume.work_experience,
            ].some(
              (item) =>
                item.verified === false &&
                ((type === "education" &&
                  "degree" in item.actual &&
                  item.actual.degree !== null) ||
                  (type === "work" &&
                    "position" in item.actual &&
                    item.actual.position !== null))
            );

            resume.is_verified = anyRejected ? "REJECTED" : "PENDING";
          }

          // Update the resumes state
          setResumes(updatedResumes);
        }
      }
    } catch (err) {
      setError("Failed to update verification status. Please try again.");
      console.error("Error verifying qualification:", err);
    }
  };

  // Mock function to simulate refreshing data
  const refreshData = () => {
    setLoading(true);
    setTimeout(() => {
      setResumes(mockResumes);
      setError(null);
      setLoading(false);
    }, 800);
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
            onClick={refreshData}
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
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Resume Verification Dashboard</h1>
        <button
          onClick={refreshData}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center"
        >
          Refresh Data
        </button>
      </div>

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
