import React, { useState } from "react";
import { Education, WorkExperience } from "@/types";
import { CheckCircle, AlertTriangle, Edit } from "lucide-react";
import ManualVerificationForm from "@/components/dashboard/ManualVerification";

interface QualificationCardProps {
  item: Education | WorkExperience;
  type: "education" | "work";
  index: number;
  resumeId: string;
  onVerify: (
    resumeId: string,
    type: "education" | "work",
    index: number,
    action: "confirm" | "reject"
  ) => void;
}

const QualificationCard: React.FC<QualificationCardProps> = ({
  item,
  type,
  index,
  resumeId,
  onVerify,
}) => {
  const [showManualVerification, setShowManualVerification] = useState(false);

  const isEducation = type === "education";
  const title = isEducation
    ? (item as Education).send.degree
    : (item as WorkExperience).send.position;

  const subtitle = isEducation
    ? (item as Education).send.institution
    : (item as WorkExperience).send.company;

  const actualTitle = isEducation
    ? (item as Education).actual.degree
    : (item as WorkExperience).actual.position;

  const actualSubtitle = isEducation
    ? (item as Education).actual.institution
    : (item as WorkExperience).actual.company;

  // Determine if there are differences between sent and actual data
  const hasDifferences =
    actualTitle !== null &&
    (actualTitle !== title || actualSubtitle !== subtitle);

  const handleManualVerificationComplete = () => {
    setShowManualVerification(false);
    // The parent component will refresh the data
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 relative">
      {/* Verification status indicator */}
      <div className="absolute top-4 right-4">
        {item.verified ? (
          <CheckCircle className="text-green-500" size={24} />
        ) : (
          <div className="flex items-center gap-2">
            <button
              onClick={() => onVerify(resumeId, type, index, "confirm")}
              className="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded text-xs"
            >
              Confirm
            </button>
            <button
              onClick={() => onVerify(resumeId, type, index, "reject")}
              className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs"
            >
              Reject
            </button>
            <button
              onClick={() => setShowManualVerification(true)}
              className="bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded text-xs flex items-center"
            >
              <Edit size={12} className="mr-1" />
              Edit
            </button>
          </div>
        )}
      </div>

      {/* Sent data */}
      <div className="mb-3">
        <h4 className="font-semibold text-lg">{title}</h4>
        <p className="text-gray-600">{subtitle}</p>
        <p className="text-xs text-gray-500 mt-1">Submitted Data</p>
      </div>

      {/* Actual verified data (if different) */}
      {hasDifferences && (
        <div className="border-t pt-2 mt-2">
          <div className="flex items-start">
            <AlertTriangle
              className="text-yellow-500 mr-2 flex-shrink-0 mt-1"
              size={16}
            />
            <div>
              <p className="text-xs text-yellow-700 font-semibold">
                Verified Data (Different from submitted)
              </p>
              <p className="font-medium">{actualTitle || "Not verified"}</p>
              <p className="text-gray-600 text-sm">
                {actualSubtitle || "Not verified"}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Manual verification form */}
      {showManualVerification && (
        <ManualVerificationForm
          resumeId={resumeId}
          type={type}
          index={index}
          onComplete={handleManualVerificationComplete}
          initialData={{
            title: actualTitle || title,
            subtitle: actualSubtitle || subtitle,
          }}
        />
      )}
    </div>
  );
};

export default QualificationCard;
