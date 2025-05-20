import React from "react";
import { Resume } from "@/types";
import QualificationSection from "@/components/dashboard/QualificationSection";
import { CheckCircle, XCircle } from "lucide-react";

interface ResumeCardProps {
  resume: Resume;
  onVerify: (
    resumeId: string,
    type: "education" | "work",
    index: number,
    action: "confirm" | "reject"
  ) => void;
}

const ResumeCard: React.FC<ResumeCardProps> = ({ resume, onVerify }) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">{resume.name}</h2>
        <div className="flex items-center">
          {resume.is_verified === "VERIFIED" ? (
            <span className="flex items-center text-green-600">
              <CheckCircle className="mr-1" size={20} />
              Verified
            </span>
          ) : resume.is_verified === "REJECTED" ? (
            <span className="flex items-center text-red-600">
              <XCircle className="mr-1" size={20} />
              Rejected
            </span>
          ) : (
            <span className="text-yellow-600">Pending Verification</span>
          )}
        </div>
      </div>

      <div className="mb-4">
        <p className="text-gray-700">
          <span className="font-semibold">Email:</span> {resume.email}
        </p>
        <p className="text-gray-700">
          <span className="font-semibold">Phone:</span> {resume.phone}
        </p>
        <p className="text-gray-700">
          <span className="font-semibold">Status:</span> {resume.status}
        </p>
        <p className="text-gray-700">
          <span className="font-semibold">Ranking Score:</span>{" "}
          {resume.ranking_score.toFixed(2)}
        </p>
      </div>

      <div className="space-y-6">
        <QualificationSection
          title="Education"
          items={resume.education}
          type="education"
          resumeId={resume.resume_id}
          onVerify={onVerify}
        />

        <QualificationSection
          title="Work Experience"
          items={resume.work_experience}
          type="work"
          resumeId={resume.resume_id}
          onVerify={onVerify}
        />
      </div>
    </div>
  );
};

export default ResumeCard;
