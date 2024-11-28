import { Link } from "react-router-dom";
import React, { useState } from "react";
import { useMutation, useLazyQuery } from "@apollo/client";
import { CHECK_EMAIL_EXISTS } from "../GraphQL/queries";
import { CREATE_USER } from "../GraphQL/mutations";

function UserCreationForm() {
  const [formData, setFormData] = useState({
    firstName: "",
    name: "",
    email: "",
    password: "",
    dateOfBirth: "",
    gender: "",
    location: {
      country: "",
      city: "",
      cityCode: "",
      street: "",
      houseNumber: "",
    },
  });
  const [passwordVisible, setPasswordVisible] = useState(false);
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const [createUser, { loading, error, data }] = useMutation(CREATE_USER);
  const [checkEmailExists, { loading: emailCheckLoading }] = useLazyQuery(CHECK_EMAIL_EXISTS, {
    fetchPolicy: "network-only",
  });

  const handleInputChange = (e) => {
    const { id, value } = e.target;

    if (id === "email") {
      if (!emailRegex.test(value)) {
        e.target.setCustomValidity("Please enter a valid email address.");
      } else {
        e.target.setCustomValidity("");
      }
    }

    if (id.startsWith("location.")) {
      const field = id.split(".")[1];
      
      if (field === "cityCode" && !/^\d*$/.test(value)) {
        return; // Allow only numeric input
      }

      setFormData((prev) => ({
        ...prev,
        location: {
          ...prev.location,
          [field]: value,
        },
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [id]: value,
      }));
    }
  };

  const handlePasswordVisibilityToggle = () => {
    setPasswordVisible(!passwordVisible);
  };

  const handleSubmit = async () => {
    const { firstName, name, email, password, dateOfBirth, gender, location } = formData;

    // Ensure required fields are filled
    if (
      !firstName ||
      !name ||
      !email ||
      !password ||
      !dateOfBirth ||
      !gender ||
      !location.country ||
      !location.city ||
      !location.cityCode
    ) {
      alert("Please fill in all required fields.");
      return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    // Check if the email exists
    try {
      const { data: emailData } = await checkEmailExists({ variables: { email } });

      if (emailData?.userByEmail) {
        alert("Email is already in use. Please use a different email.");
        return;
      }

      // Create the profile
      await createUser({
        variables: {
          firstName,
          name,
          email,
          password,
          dateOfBirth,
          gender,
          location,
        },
      });
      alert("Profile created successfully!");
    } catch (err) {
      console.error("Error checking email or creating profile:", err);
    }
  };

  return (
    <section className="w-full overflow-hidden dark:bg-gray-900 flex-grow">
      <div className="flex flex-col h-screen">
        <div className="sm:w-[80%] xs:w-[90%] mx-auto flex py-6">
          <h1 className="w-full text-left my-4 sm:mx-4 xs:pl-4 text-gray-800 dark:text-white lg:text-4xl md:text-3xl sm:text-3xl xs:text-xl font-serif">
            Create your profile
          </h1>
        </div>
        <div className="overflow-y-auto flex-grow">
          <form>
            <div className="xl:w-[80%] lg:w-[90%] md:w-[90%] sm:w-[92%] xs:w-[90%] mx-auto flex flex-col gap-4 relative lg:-top-8 md:-top-6 sm:-top-4 xs:-top-4 p-4">
              <div className="w-full my-auto py-6 flex flex-col justify-center gap-2">
                <div className="w-full">
                  <dl className="text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
                    {[
                      { id: "firstName", label: "First Name", type: "text", placeholder: "First Name" },
                      { id: "name", label: "Last Name", type: "text", placeholder: "Last Name" },
                      { id: "email", label: "Email", type: "email", placeholder: "Email" },
                      { id: "dateOfBirth", label: "Date of Birth", type: "date", placeholder: "" },
                    ].map((field) => (
                      <div key={field.id} className="flex flex-col py-3">
                        <label
                          htmlFor={field.id}
                          className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                        >
                          {field.label}
                        </label>
                        <input
                          id={field.id}
                          type={field.type}
                          value={formData[field.id]}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder={field.placeholder}
                          required
                        />
                      </div>
                    ))}

                    <div className="flex flex-col py-3">
                      <label
                        htmlFor="gender"
                        className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                      >
                        Gender
                      </label>
                      <select
                        id="gender"
                        value={formData.gender}
                        onChange={handleInputChange}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        required
                      >
                        <option value="" disabled>
                          Select Gender
                        </option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                      </select>
                    </div>

                    {/* Password with Show/Hide Toggle */}
                    <div className="flex flex-col py-3">
                      <label
                        htmlFor="password"
                        className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                      >
                        Password
                      </label>
                      <div className="relative">
                        <input
                          id="password"
                          type={passwordVisible ? "text" : "password"}
                          value={formData.password}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder="Password"
                          required
                        />
                        <button
                          type="button"
                          onClick={handlePasswordVisibilityToggle}
                          className="absolute top-1/2 right-3 transform -translate-y-1/2 text-gray-500"
                        >
                          {passwordVisible ? "Hide" : "Show"}
                        </button>
                      </div>
                    </div>

                    {/* Location Fields */}
                    {[
                      { id: "location.country", label: "Country", placeholder: "Country" },
                    ].map((field) => (
                      <div key={field.id} className="flex flex-col py-3">
                        <label
                          htmlFor={field.id}
                          className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                        >
                          {field.label}
                        </label>
                        <input
                          id={field.id}
                          type="text"
                          value={formData.location[field.id.split(".")[1]] || ""}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder={field.placeholder}
                          required
                        />
                      </div>
                    ))}

                    {/* City and City Code in Flexbox */}
                    <div className="flex gap-4">
                      <div className="flex flex-col py-3 flex-1">
                        <label
                          htmlFor="location.city"
                          className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                        >
                          City
                        </label>
                        <input
                          id="location.city"
                          type="text"
                          value={formData.location.city}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder="City"
                          required
                        />
                      </div>
                      <div className="flex flex-col py-3 flex-1">
                        <label
                          htmlFor="location.cityCode"
                          className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                        >
                          City Code
                        </label>
                        <input
                          id="location.cityCode"
                          type="text"
                          value={formData.location.cityCode}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder="City Code"
                          required
                        />
                      </div>
                    </div>

                    {/* Optional Street and House Number */}
                    <div className="flex gap-2">
                      <div className="flex flex-col py-3 flex-1">
                        <label
                          htmlFor="location.street"
                          className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                        >
                          Street (Optional)
                        </label>
                        <input
                          id="location.street"
                          type="text"
                          value={formData.location.street}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder="Street"
                        />
                      </div>
                      <div className="flex flex-col py-3 flex-1">
                        <label
                          htmlFor="location.houseNumber"
                          className="mb-1 text-gray-500 md:text-lg dark:text-gray-400"
                        >
                          House Number (Optional)
                        </label>
                        <input
                          id="location.houseNumber"
                          type="text"
                          value={formData.location.houseNumber}
                          onChange={handleInputChange}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder="House Number"
                        />
                      </div>
                    </div>
                  </dl>
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
          </form>
        </div>
      </div>
    </section>
  );
}

export default UserCreationForm;
