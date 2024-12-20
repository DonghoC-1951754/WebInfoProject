import React, { useState } from 'react';
import UserCard from './UserCard';
import CompanyCard from './CompanyCard';
import { useQuery } from '@apollo/client';
import { GET_USERS, GET_COMPANIES } from '../GraphQL/queries';


const ToggleCards = () => {
    const [showUsers, setShowUsers] = useState(true);
  
    
    // console.log(localStorage.getItem('accessToken'))
  
    const RenderUsers = () => {
      // Fetch Users
      const { loading: usersLoading, error: usersError, data: usersData } = useQuery(GET_USERS , {
        context: {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        },
      });
      if (usersLoading) return <p>Loading Users...</p>;
      if (usersError) return <p>Error Loading Users: {usersError.message}</p>;
      return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 p-4">
          {usersData.users.map((user) => (
            <UserCard
              key={user.id}
              id = {user.id}
              firstName={user.firstName}
              lastName={user.name}
              location={user.location}
              email={user.email}
            />
          ))}
        </div>
      );
    };
  
    const RenderCompanies = () => {
      // Fetch Companies
      const { loading: companiesLoading, error: companiesError, data: companiesData } = useQuery(GET_COMPANIES, {
        context: {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        },
      });
      if (companiesLoading) return <p>Loading Companies...</p>;
      if (companiesError) return <p>Error Loading Companies: {companiesError.message}</p>;
      return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 p-4">
          {companiesData.companies.map((company) => (
            <CompanyCard
              key={company.id}
              id = {company.id}
              name={company.name}
              location={company.location}
              email={company.email}
            />
          ))}
        </div>
      );
    };
  
    return (
      <div className="min-w-screen bg-gray-100 dark:bg-gray-900 flex-grow">
        <div className="flex justify-center items-center p-4">
          <button
            className={`px-4 py-2 rounded-l ${showUsers ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}
            onClick={() => setShowUsers(true)}
          >
            Users
          </button>
          <button
            className={`px-4 py-2 rounded-r ${!showUsers ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}
            onClick={() => setShowUsers(false)}
          >
            Companies
          </button>
        </div>
        {showUsers ? RenderUsers() : RenderCompanies()}
      </div>
    );
  };
  
  export default ToggleCards;



