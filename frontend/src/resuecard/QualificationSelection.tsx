import React from "react";
import { Education, WorkExperience } from "@/types";
import QualificationCard from "@/components/dashboard/QualificationCard";

interface QualificationSectionProps {
  title: string;
  items: Education[] | WorkExperience[];
  type: "education" | "work";
  resumeId: string;
  onVerify: (
    resumeId: string,
    type: "education" | "work",
    index: number,
    action: "confirm" | "reject"
  ) => void;
}

const QualificationSection: React.FC<QualificationSectionProps> = ({
  title,
  items,
  type,
  resumeId,
  onVerify,
}) => {
  if (!items || items.length === 0) {
    return (
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="text-xl font-semibold mb-3">{title}</h3>
        <p className="text-gray-500 italic">
          No {title.toLowerCase()} entries found.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <h3 className="text-xl font-semibold mb-3">{title}</h3>
      <div className="space-y-4">
        {items.map((item, index) => (
          <QualificationCard
            key={index}
            item={item}
            type={type}
            index={index}
            resumeId={resumeId}
            onVerify={onVerify}
          />
        ))}
      </div>
    </div>
  );
};

export default QualificationSection;
