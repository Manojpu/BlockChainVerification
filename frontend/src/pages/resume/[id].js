import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import api from '../../services/api';
import ResumeCard from '../../components/dashboard/ResumeCard';

const ResumePage = () => {
    const router = useRouter();
    const { id } = router.query;
    const [resume, setResume] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (id) {
            const fetchResume = async () => {
                try {
                    const response = await api.get(`/resumes/${id}`);
                    setResume(response.data);
                } catch (err) {
                    setError('Failed to load resume');
                } finally {
                    setLoading(false);
                }
            };

            fetchResume();
        }
    }, [id]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            {resume ? (
                <ResumeCard resume={resume} />
            ) : (
                <div>No resume found</div>
            )}
        </div>
    );
};

export default ResumePage;