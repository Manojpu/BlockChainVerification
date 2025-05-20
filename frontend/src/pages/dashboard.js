import React, { useState } from "react";
import ResumeList from "../components/dashboard/ResumeList";

const Dashboard = () => {
  // Hardcoded resume data
  const [resumes, setResumes] = useState([
    {
      id: "1",
      title: "Software Engineer Resume",
      lastUpdated: "2025-05-15T10:30:00Z",
      template: "Professional",
      status: "completed",
    },
    {
      id: "2",
      title: "Product Manager Application",
      lastUpdated: "2025-05-10T14:45:00Z",
      template: "Modern",
      status: "completed",
    },
    {
      id: "3",
      title: "Data Scientist Resume",
      lastUpdated: "2025-05-05T09:20:00Z",
      template: "Classic",
      status: "draft",
    },
    {
      id: "4",
      title: "UX Designer Portfolio",
      lastUpdated: "2025-04-28T16:15:00Z",
      template: "Creative",
      status: "completed",
    },
  ]);

  // Simulate loading state (optional - set to false since we're using hardcoded data)
  const [loading, setLoading] = useState(false);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>
      <p className="welcome-text">Welcome to your resume dashboard!</p>

      {resumes.length > 0 ? (
        <ResumeList resumes={resumes} />
      ) : (
        <p>No resumes found. Create your first resume to get started!</p>
      )}

      {/* Button to create a new resume */}
      <button
        className="create-resume-btn"
        onClick={() => console.log("Create new resume clicked")}
      >
        Create New Resume
      </button>
    </div>
  );
};

export default Dashboard;
