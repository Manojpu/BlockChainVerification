import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export const login = async (credentials) => {
    try {
        const response = await axios.post(`${API_URL}/auth/login`, credentials);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const register = async (userData) => {
    try {
        const response = await axios.post(`${API_URL}/auth/register`, userData);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const uploadResume = async (resumeData) => {
    try {
        const response = await axios.post(`${API_URL}/resumes/upload`, resumeData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const getResumes = async () => {
    try {
        const response = await axios.get(`${API_URL}/resumes`);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const verifyResume = async (resumeId) => {
    try {
        const response = await axios.get(`${API_URL}/verification/${resumeId}`);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};