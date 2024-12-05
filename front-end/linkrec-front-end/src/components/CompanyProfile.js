import React from 'react';
import { useQuery } from '@apollo/client';
import { useParams } from 'react-router-dom';
import { GET_COMPANY_BY_ID } from '../GraphQL/queries';

const CompanyProfile = () => {
    const { id } = useParams();

    const { loading, error, data } = useQuery(GET_COMPANY_BY_ID, {
        variables: { id }
    });

    if (loading) return <p className="text-center text-xl text-gray-700">Loading company data...</p>;
    if (error) return <p className="text-center text-xl text-red-500">Error: {error.message}</p>;

    const company = data.company;

    return (
        <div className="w-[90%] max-w-screen-lg mx-auto p-8 bg-white rounded-lg shadow-lg mt-8">
            {/* Company Name */}
            <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-800">{company.name}</h1>
                <p className="text-gray-500 text-sm mt-2">Company ID: {company.id}</p>
            </div>

            {/* Contact Information */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Contact Information</h2>
                <p className="text-gray-600">
                    <strong>Email:</strong> {company.email}
                </p>
            </section>

            {/* Location Details */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Location</h2>
                <p className="text-gray-600">
                    <strong>Country:</strong> {company.location.country}
                </p>
                <p className="text-gray-600">
                    <strong>City:</strong> {company.location.city}, {company.location.cityCode}
                </p>
                <p className="text-gray-600">
                    <strong>Street:</strong> {company.location.street} {company.location.houseNumber}
                </p>
            </section>

            {/* Vacancies */}
            {company.vacancies.length > 0 && (
                <section>
                    <h2 className="text-2xl font-semibold text-gray-700 mb-4">Vacancies</h2>
                    <div className="space-y-6">
                        {company.vacancies.map((vacancy, index) => (
                            <div
                                key={index}
                                className="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm"
                            >
                                <p className="text-lg font-bold text-gray-700">
                                    {vacancy.jobTitle}
                                </p>
                                <p className="text-gray-600">
                                    <strong>Start Date:</strong> {vacancy.startDate}
                                </p>
                                <p className="text-gray-600">
                                    <strong>End Date:</strong> {vacancy.endDate || 'Ongoing'}
                                </p>
                                <div className="mt-2">
                                    <strong>Required Skills:</strong>
                                    <ul className="list-disc pl-5 mt-1 text-gray-600">
                                        {vacancy.requiredSkills.map((skill, skillIndex) => (
                                            <li key={skillIndex}>{skill}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            )}
        </div>
    );
};

export default CompanyProfile;
