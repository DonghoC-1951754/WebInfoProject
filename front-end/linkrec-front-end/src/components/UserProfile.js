import React from 'react';
import { useQuery } from '@apollo/client';
import { useParams } from 'react-router-dom';
import { GET_USER_BY_ID } from '../GraphQL/queries';

const UserProfile = () => {
    const { id } = useParams();

    const { loading, error, data } = useQuery(GET_USER_BY_ID, {
        variables: { id }
    });

    if (loading) return <p className="text-center text-xl text-gray-700">Loading user data...</p>;
    if (error) return <p className="text-center text-xl text-red-500">Error: {error.message}</p>;

    const user = data.user;

    return (
        <div className="profile-container w-[80%] max-w-screen-lg mx-auto p-12 bg-white shadow-lg rounded-lg">
            {/* Header Section */}
            <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-800">
                    {user.firstName} {user.name}
                </h1>
                <p className="text-gray-600 text-sm mt-2">User ID: {user.id}</p>
            </div>

            {/* Personal Information */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Personal Information</h2>
                <ul className="list-none space-y-2">
                    <li>
                        <strong>Email:</strong> {user.email}
                    </li>
                    <li>
                        <strong>Date of Birth:</strong> {user.dateOfBirth}
                    </li>
                    <li>
                        <strong>Gender:</strong> {user.gender}
                    </li>
                </ul>
            </section>

            {/* Location Details */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Location</h2>
                <p>
                    <strong>Country:</strong> {user.location.country}
                </p>
                <p>
                    <strong>City:</strong> {user.location.city}, {user.location.cityCode}
                </p>
                <p>
                    <strong>Street:</strong> {user.location.street} {user.location.houseNumber}
                </p>
            </section>

            {/* Education Section */}
            {user.educations.length > 0 && (
                <section className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-700 mb-4">Education</h2>
                    <ul className="list-disc pl-6 space-y-2">
                        {user.educations.map((education, index) => (
                            <li key={index}>
                                <p>
                                    <strong>Institution:</strong> {education.institution}
                                </p>
                                <p>
                                    <strong>Degree:</strong> {education.degree} in {education.fieldOfStudy}
                                </p>
                                <p>
                                    <strong>Year Graduated:</strong> {education.yearGraduated}
                                </p>
                            </li>
                        ))}
                    </ul>
                </section>
            )}

            {/* Experience Section */}
            {user.experiences.length > 0 && (
                <section>
                    <h2 className="text-2xl font-semibold text-gray-700 mb-4">Work Experience</h2>
                    <ul className="list-disc pl-6 space-y-4">
                        {user.experiences.map((experience, index) => (
                            <li key={index}>
                                <p>
                                    <strong>Company:</strong> {experience.companyName}
                                </p>
                                <p>
                                    <strong>Job Title:</strong> {experience.jobTitle}
                                </p>
                                <p>
                                    <strong>Duration:</strong> {experience.startDate} - {experience.endDate || 'Present'}
                                </p>
                                <p>
                                    <strong>Description:</strong> {experience.description}
                                </p>
                            </li>
                        ))}
                    </ul>
                </section>
            )}
        </div>
    );
};

export default UserProfile;
