import React, { useState } from "react";

interface ManualVerificationFormProps {
  resumeId: string;
  type: "education" | "work";
  index: number;
  onComplete: () => void;
  initialData: {
    title: string;
    subtitle: string;
  };
}

const ManualVerificationForm: React.FC<ManualVerificationFormProps> = ({
  resumeId,
  type,
  index,
  onComplete,
  initialData,
}) => {
  const [formData, setFormData] = useState({
    title: initialData.title || "",
    subtitle: initialData.subtitle || "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    // Simulate API call delay
    setTimeout(() => {
      // In a real implementation, this would send data to an API
      // For now, we just complete the process
      setIsLoading(false);
      onComplete();

      // In a real app, the parent component would refresh the data
      // to show the updated verification status
    }, 800);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 mt-4">
      <h4 className="font-semibold text-lg mb-3">Manual Verification</h4>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            {type === "education" ? "Actual Degree" : "Actual Position"}
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) =>
              setFormData({ ...formData, title: e.target.value })
            }
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
            required
            disabled={isLoading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            {type === "education" ? "Actual Institution" : "Actual Company"}
          </label>
          <input
            type="text"
            value={formData.subtitle}
            onChange={(e) =>
              setFormData({ ...formData, subtitle: e.target.value })
            }
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
            required
            disabled={isLoading}
          />
        </div>
        <div className="flex gap-2">
          <button
            type="submit"
            className="flex-1 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300"
            disabled={isLoading}
          >
            {isLoading ? "Saving..." : "Verify with This Data"}
          </button>
          <button
            type="button"
            onClick={onComplete}
            className="py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            disabled={isLoading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ManualVerificationForm;
