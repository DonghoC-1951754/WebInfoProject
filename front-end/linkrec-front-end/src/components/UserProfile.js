import React, { useState } from 'react';
import { useQuery, useMutation } from '@apollo/client';
import { useParams } from 'react-router-dom';
import { GET_USER_BY_ID } from '../GraphQL/queries';
import { UPDATE_USER } from '../GraphQL/mutations';

const UserProfile = () => {
    const { id } = useParams();
    const loggedInUserID = localStorage.getItem('userID');
    const isUser = id === loggedInUserID;

    const { loading, error, data } = useQuery(GET_USER_BY_ID, {
        variables: { id },
    });

    const [editableFields, setEditableFields] = useState({
        id: id,
        firstName: undefined,
        name: undefined,
        email: undefined,
        dateOfBirth: undefined,
        gender: undefined,
        country: undefined,
        city: undefined,
        cityCode: undefined,
        street: undefined,
        houseNumber: undefined,
    });
    const [updateUser] = useMutation(UPDATE_USER); // Use the hook here

    const toggleEdit = (field, currentValue) => {
        setEditableFields((prev) => ({
            ...prev,
            [field]: prev[field] === undefined ? currentValue : undefined,
        }));
    };

    const handleFieldChange = (field, value) => {
        setEditableFields((prev) => ({
            ...prev,
            [field]: value,
        }));
    };

    const saveChanges = async () => {
        try {
            await updateUser({
                variables: {
                    id,
                    ...editableFields, // Spread all editable fields into variables
                },
            });
            console.log("Updated user successfully:", editableFields);
            setEditableFields({}); // Clear editable fields after saving
        } catch (err) {
            console.error("Failed to update user:", err);
        }
    };

    if (loading) return <p className="text-center text-xl text-gray-700">Loading user data...</p>;
    if (error) return <p className="text-center text-xl text-red-500">Error: {error.message}</p>;

    const user = data.user;

    return (
        <div className="profile-container w-[80%] max-w-screen-lg mx-auto p-12 bg-white shadow-lg rounded-lg">
            {/* Header Section */}
            <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-800">
                {editableFields.firstName !== undefined ? (
                            <input
                                type="text"
                                value={editableFields.firstName}
                                onChange={(e) => handleFieldChange("firstName", e.target.value)}
                                className="border p-1 rounded"
                            />
                        ) : (
                            user.firstName
                        )}
                        {isUser && (
                            <button
                                type="button"
                                onClick={() =>
                                    editableFields.firstName !== undefined
                                        ? saveChanges("firstName")
                                        : toggleEdit("firstName", user.firstName)
                                }
                                className="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm p-2.5 inline-flex items-center ms-2"
                            >
                                {editableFields.firstName !== undefined ? "Save" : "Edit"}
                            </button>
                        )} 
                        {editableFields.name !== undefined ? (
                            <input
                                type="text"
                                value={editableFields.name}
                                onChange={(e) => handleFieldChange("name", e.target.value)}
                                className="border p-1 rounded"
                            />
                        ) : (
                            user.name
                        )}
                        {isUser && (
                            <button
                                type="button"
                                onClick={() =>
                                    editableFields.name !== undefined
                                        ? saveChanges("name")
                                        : toggleEdit("name", user.name)
                                }
                                className="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm p-2.5 inline-flex items-center ms-2"
                            >
                                {editableFields.name !== undefined ? "Save" : "Edit"}
                            </button>
                        )}
                </h1>
                <p className="text-gray-600 text-sm mt-2">User ID: {user.id} </p>
            </div>

            {/* Personal Information */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Personal Information</h2>
                <ul className="list-none space-y-2">
                    <li>
                        <strong>Email:</strong>{" "} {user.email}
                    </li>
                    <li>
                        <strong>Date of Birth:</strong> {" "} {user.dateOfBirth}
                    </li>
                    <li>
                        <strong>Gender:</strong> 
                        {editableFields.gender !== undefined ? (
                            <select
                                type="text"
                                value={editableFields.gender}
                                onChange={(e) => handleFieldChange("gender", e.target.value)}
                                className="border p-1 rounded">
                                <option>male</option>
                                <option>female</option>
                                <option>other</option>
                            </select>
                        ) : (
                            user.gender
                        )}
                        {isUser && (
                            <button
                                type="button"
                                onClick={() =>
                                    editableFields.gender !== undefined
                                        ? saveChanges("gender")
                                        : toggleEdit("gender", user.gender)
                                }
                                className="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm p-2.5 inline-flex items-center ms-2"
                            >
                                {editableFields.gender !== undefined ? "Save" : "Edit"}
                            </button>
                        )}
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
                <p>
                    <strong>cityCode:</strong> {user.location.cityCode}
                </p>
                <p>
                    <strong>houseNumber:</strong> {user.location.houseNumber}
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
