import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import ResumeList from '../components/dashboard/ResumeList';
import { fetchResumes } from '../services/api';

const Dashboard = () => {
    const { user } = useContext(AuthContext);
    const [resumes, setResumes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getResumes = async () => {
            try {
                const data = await fetchResumes(user.id);
                setResumes(data);
            } catch (error) {
                console.error('Error fetching resumes:', error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            getResumes();
        }
    }, [user]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Dashboard</h1>
            {resumes.length > 0 ? (
                <ResumeList resumes={resumes} />
            ) : (
                <p>No resumes found.</p>
            )}
        </div>
    );
};

export default Dashboard;