import React from 'react';

const VacancyCard = ({ jobTitle, company, requiredSkills, startDate, endDate }) => {
    const { name, location } = company;
    const { country, city, cityCode, street, houseNumber } = location;

    return (
        <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 h-auto">
            <a href="#">
                <h5 className="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">{jobTitle}</h5>
            </a>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Company: {name}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Location: {`${street} ${houseNumber}, ${city} ${cityCode}, ${country}`}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Required Skills: {requiredSkills.join(', ')}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">Start Date: {startDate}</p>
            <p className="mb-3 font-normal text-gray-500 dark:text-gray-400">End Date: {endDate}</p>
        </div>
    );
};
export default VacancyCard;