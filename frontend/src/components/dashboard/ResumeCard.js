import React from 'react';

const ResumeCard = ({ resume }) => {
    return (
        <div className="bg-white shadow-md rounded-lg p-4 m-2">
            <h2 className="text-xl font-bold">{resume.title}</h2>
            <p className="text-gray-700">{resume.description}</p>
            <div className="mt-4">
                <a href={resume.link} className="text-blue-500 hover:underline">
                    View Resume
                </a>
            </div>
        </div>
    );
};

export default ResumeCard;