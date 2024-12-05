import React from 'react';
import { useQuery } from '@apollo/client';
import { useParams } from 'react-router-dom';
import { GET_USER_BY_ID } from '../GraphQL/queries';

const UserProfile = () => {
    const { id } = useParams();

    const { loading, error, data } = useQuery(GET_USER_BY_ID, {
        variables: { id }
    });

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    const user = data.user;

    return (
        <div className="profile-container">
            <h1>{user.firstName} {user.name}</h1>
            <p>Email: {user.email}</p>
            <p>Date of Birth: {user.dateOfBirth}</p>
            <p>Gender: {user.gender}</p>
            <h2>Location:</h2>
            <p>{user.location.country}, {user.location.city}, {user.location.cityCode}</p>
            <p>{user.location.street} {user.location.houseNumber}</p>
            
            <h2>Education:</h2>
            {user.educations.map((education, index) => (
                <div key={index}>
                    <p>{education.institution}, {education.degree} in {education.fieldOfStudy} (Graduated in {education.yearGraduated})</p>
                </div>
            ))}
            
            <h2>Experience:</h2>
            {user.experiences.map((experience, index) => (
                <div key={index}>
                    <p>{experience.companyName}: {experience.jobTitle}</p>
                    <p>{experience.startDate} - {experience.endDate}</p>
                    <p>{experience.description}</p>
                </div>
            ))}
        </div>
    );
};

export default UserProfile;