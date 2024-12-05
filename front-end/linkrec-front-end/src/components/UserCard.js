import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';


const UserCard = ({ id, firstName, lastName, location, email }) => {
    return (
        <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 h-64">
            <Link to={`/userProfile/${id}`}>
                <h5 className="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white"> {lastName}</h5>
            </Link>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">first Name: {firstName}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Email: {email}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Country: {location.country}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">City: {location.city}, {location.cityCode}</p>
            {location.street && location.houseNumber ? (
                <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Street: {location.street}, {location.houseNumber}</p>
            ) : (
                <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">&nbsp;</p>
            )}   
        </div>
    );
};

UserCard.propTypes = {
    id: PropTypes.string.isRequired,
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    location: PropTypes.object.isRequired,
    email: PropTypes.string.isRequired,
};

export default UserCard;
