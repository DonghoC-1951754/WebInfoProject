import React from 'react';
import { Link } from 'react-router-dom';

function RegisterForm() {
  return (
    <section className="bg-gray-50 dark:bg-gray-900 flex-grow">
      <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
          <div className="p-6 space-y-6 md:space-y-8 sm:p-8">
            <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white text-center">
              Choose your kind of profile
            </h1>
            <div className="flex flex-col gap-4">
              <Link to="/createUser">
                <button
                  className="w-full text-white bg-blue-800 hover:bg-blue-900 focus:ring-4 focus:outline-none focus:ring-blue-500 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-800 dark:hover:bg-blue-900 dark:focus:ring-blue-600"
                >
                  A Person
                </button>
              </Link>
              <Link to="/createBusiness">
                <button
                  className="w-full text-white bg-blue-800 hover:bg-blue-900 focus:ring-4 focus:outline-none focus:ring-blue-500 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-800 dark:hover:bg-blue-900 dark:focus:ring-blue-600"
                >
                  A Business
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default RegisterForm;
