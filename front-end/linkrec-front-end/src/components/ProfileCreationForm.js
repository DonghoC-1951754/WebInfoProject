import { Link } from "react-router-dom";
import React, { useState } from 'react';
import { useMutation, useQuery,  useLazyQuery } from "@apollo/client";
import { GET_PROFILES,CHECK_EMAIL_EXISTS  } from "../GraphQL/queries";
import { CREATE_PROFILE } from '../GraphQL/mutations';

function ProfileCreationForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    name: '',
    email: '',
    location: '',
  });

  const [createProfile, { loading, error, data }] = useMutation(CREATE_PROFILE);
  const [checkEmailExists, { loading: emailCheckLoading }] = useLazyQuery(
    CHECK_EMAIL_EXISTS,
    {
      fetchPolicy: "network-only",
    }
  );

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const handleSubmit = async () => {
    const { firstName, name, email, location } = formData;

    // Check if the email exists
    try {
      const { data: emailData } = await checkEmailExists({ variables: { email } });

      if (emailData?.profileByEmail) {
        alert("Email is already in use. Please use a different email.");
        return;
      }

      // Create the profile if email does not exist
      await createProfile({
        variables: { firstName, name, email, location },
      });
      alert("Profile created successfully!");
    } catch (err) {
      console.error("Error checking email or creating profile:", err);
    }
  };

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
            opportunities.
          </p>
          <div className="w-full my-auto py-6 flex flex-col justify-center gap-2">
            <div className="w-full flex sm:flex-row xs:flex-col gap-2 justify-center">
              <div className="w-full">
                <dl className="text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
                  <div className="flex flex-col pb-3">
                    <label
                      htmlFor="firstName"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      First Name
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      value={formData.firstName}
                      onChange={handleInputChange}
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="First Name"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="name"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Last Name
                    </label>
                    <input
                      type="text"
                      id="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Last Name"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="email"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Email
                    </label>
                    <input
                      type="email"
                      id="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Email"
                      required
                    />
                  </div>
                  <div className="flex flex-col py-3">
                    <label
                      htmlFor="location"
                      className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                    >
                      Location
                    </label>
                    <input
                      type="text"
                      id="location"
                      value={formData.location}
                      onChange={handleInputChange}
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Location"
                      required
                    />
                  </div>
                </dl>
              </div>
            </div>
          </div>
          <button
            onClick={handleSubmit}
            disabled={loading || emailCheckLoading}
            className="w-full h-12 px-6 text-indigo-100 transition-colors duration-150 bg-indigo-700 rounded-lg focus:shadow-outline hover:bg-indigo-800"
          >
            {loading || emailCheckLoading ? "Checking..." : "Create Profile"}
          </button>
          {error && <p className="text-red-500">Error: {error.message}</p>}
          {data && <p className="text-green-500">Profile created successfully!</p>}
        </div>
      </div>
    </section>
  );
}

export default ProfileCreationForm;