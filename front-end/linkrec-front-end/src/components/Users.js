import React from 'react';
import UserCard from './UserCard';
import { useQuery } from '@apollo/client';
import { GET_USERS } from '../GraphQL/queries';

const Users = () => {
    const { loading, error, data } = useQuery(GET_USERS);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div className="min-w-screen bg-gray-100 dark:bg-gray-900 flex-grow">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 p-4">
                {data.users.map(user => (
                    <UserCard 
                        key={user.id}
                        firstName={user.firstName} 
                        lastName={user.name} 
                        location = {user.location}
                        email={user.email} 
                    />
                ))}
            </div>
        </div>
    );
};


export default Users;