import { Link } from "react-router-dom";
import React from "react";
import { useQuery } from "@apollo/client";
import { useLazyQuery } from "@apollo/client";
import { GET_PROFILES } from "../GraphQL/queries";

function ProfileCreationForm() {
  const [fetchProfiles, { loading, error, data }] = useLazyQuery(GET_PROFILES);
  // if (loading) return <p>Loading...</p>;
  // if (error) return <p>Error: {error.message}</p>;
  // console.log(data);

  return (
    <section className="w-full overflow-hidden dark:bg-gray-900 flex-grow">
      <div className="flex flex-col">
        <div className="sm:w-[80%] xs:w-[90%] mx-auto flex py-6">
          <h1 className="w-full text-left my-4 sm:mx-4 xs:pl-4 text-gray-800 dark:text-white lg:text-4xl md:text-3xl sm:text-3xl xs:text-xl font-serif">
            Create your profile
          </h1>
        </div>
        <div className="xl:w-[80%] lg:w-[90%] md:w-[90%] sm:w-[92%] xs:w-[90%] mx-auto flex flex-col gap-4 relative lg:-top-8 md:-top-6 sm:-top-4 xs:-top-4 p-4">
          <p className="w-fit text-gray-700 dark:text-gray-400 text-md py-2">
            These are the details that will be displayed on your profile page
            and will be visible to others.<br></br>This information will be used
            in our recommendation system to help you find the right
            opportunites.
          </p>
          <div className="w-full my-auto py-6 flex flex-col justify-center gap-2">
            <div className="w-full flex sm:flex-row xs:flex-col gap-2 justify-center">
              <div className="w-full">
                <dl className="text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
                  <div className="flex flex-col pb-3">
                    <label
                      htmlFor="firstNameInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      First Name
                    </label>
                    <input
                      type="text"
                      id="firstNameInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="First Name"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="lastNameInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Last Name
                    </label>
                    <input
                      type="text"
                      id="lastNameInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Last Name"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="emailInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Email
                    </label>
                    <input
                      type="mail"
                      id="emailInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Email"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="locationInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Location
                    </label>
                    <input
                      type="text"
                      id="locationInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Location"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="websiteInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Website
                    </label>
                    <input
                      type="text"
                      id="websiteInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Website"
                      required
                    />
                  </div>
                </dl>
              </div>
              <div className="w-full">
                <dl className="text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
                  <div className="flex flex-col pb-3">
                    <label
                      htmlFor="graduatedFromInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Graduated From
                    </label>
                    <input
                      type="text"
                      id="graduatedFromInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Graduated From"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="degreeInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Degree
                    </label>
                    <input
                      type="text"
                      id="degreeInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Degree"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="professionalExpInput"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Professional Experience
                    </label>
                    <input
                      type="text"
                      id="professionalExpInput"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Professional Experience"
                      required
                    />
                  </div>
                </dl>
              </div>
            </div>
          </div>
          <button
            onClick={() => fetchProfiles()}
            className="w-full h-12 px-6 text-indigo-100 transition-colors duration-150 bg-indigo-700 rounded-lg focus:shadow-outline hover:bg-indigo-800"
          >
            Create Profile
          </button>
          {/* {loading && <p>Loading...</p>}
          {error && <p>Error: {error.message}</p>}
          {data && (
            <ul>
              {data.profiles.map((profile) => (
                <li key={profile.id}>
                  <strong>{profile.name}</strong> - {profile.industry}
                </li>
              ))}
            </ul>
          )} */}
        </div>
      </div>
    </section>
  );
}

export default ProfileCreationForm;
