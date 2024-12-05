import React from 'react';
import { useQuery } from '@apollo/client';
import { useParams } from 'react-router-dom';
import { GET_COMPANY_BY_ID } from '../GraphQL/queries';

const CompanyProfile = () => {
    const { id } = useParams();

    const { loading, error, data } = useQuery(GET_COMPANY_BY_ID, {
        variables: { id }
    });

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    const company = data.company;

    return (
        <div className="profile-container">
            <h1>{company.name}</h1>
            <p>Email: {company.email}</p>
            <h2>Location:</h2>
            <p>{company.location.country}, {company.location.city}, {company.location.cityCode}</p>
            <p>{company.location.street} {company.location.houseNumber}</p>
            
            <h2>Vacancies:</h2>
            {company.vacancies.map((vacancy, index) => (
                <div key={index}>
                    <p>{vacancy.jobTitle}, startDate: {vacancy.startDate} , endDate: {vacancy.endDate}</p>
                    {vacancy.requiredSkills.map((skill, skillIndex) => (
                        <div key={skillIndex}>
                            <p>skill:{skill}</p>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default CompanyProfile;