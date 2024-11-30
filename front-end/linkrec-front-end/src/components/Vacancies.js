// import React from "react";
import { GET_ACTIVE_VACANCIES } from "../GraphQL/queries";
import VacancyCard from "./VacancyCard";
import { useQuery } from "@apollo/client";
import React, { useState, useEffect } from 'react';

const Vacancies = () => {
  // const currentDate = new Date().toISOString();
  // const { loading, error, data } = useQuery(GET_ACTIVE_VACANCIES, {
  //     variables: { currentDate },
  //   });
  const [currentDate, setCurrentDate] = useState("");
  useEffect(() => {
    const today = new Date().toISOString().split("T")[0];
    setCurrentDate(today);
  }, []);
  const { loading, error, data } = useQuery(GET_ACTIVE_VACANCIES, {
    variables: { currentDate },
    skip: !currentDate, // Skip the query until currentDate is set
  });
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  if (!data || !data.activeVacancies) {
    return <p>No data available</p>;
  }
  console.log(data.activeVacancies);
  return (
    <div className="min-w-screen bg-gray-100 dark:bg-gray-900 flex-grow">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 p-4">
        {data.activeVacancies.map((vacancy) => (
          <VacancyCard
            key={vacancy.id}
            jobTitle={vacancy.jobTitle}
            company={vacancy.company}
            requiredSkills={vacancy.requiredSkills}
            startDate={vacancy.startDate}
            endDate={vacancy.endDate}
          />
        ))}
      </div>
    </div>
  );
};

export default Vacancies;