import React from 'react';
import ProfileCard from './ProfileCard';
import { useQuery } from '@apollo/client';
import { GET_PROFILES } from '../GraphQL/queries';

const Profiles = () => {
    const { loading, error, data } = useQuery(GET_PROFILES);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div className="min-w-screen bg-gray-100 dark:bg-gray-900 flex-grow">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 p-4">
                {data.profiles.map(profile => (
                    <ProfileCard 
                        key={profile.id}
                        firstName={profile.firstName} 
                        lastName={profile.name} 
                        location={profile.location} 
                        email={profile.email} 
                    />
                ))}
            </div>
        </div>
    );
};


export default Profiles;