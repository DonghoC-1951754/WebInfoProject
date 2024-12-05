import { Link } from "react-router-dom";

function LoginForm() {
  return (
    <div className="font-sans bg-gradient-to-r from-blue-500 to-purple-600 text-white flex items-center justify-center h-screen">
      <div className="w-full max-w-4xl px-6 py-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="text-center md:text-left">
            <h2 className="lg:text-6xl text-4xl font-extrabold text-white leading-tight">
              Welcome to LinkRec
            </h2>
            <p className="text-lg mt-6 text-white opacity-80">
              The best networking platform for professionals. Let's get you started!
            </p>
          </div>

          <form className="flex items-center justify-center">
            <div className="bg-white p-4 rounded-xl shadow-2xl dark:bg-gray-800 w-80">
              <Link to="http://localhost:5000/login">
                <button
                  type="button"
                  className="w-full py-3 text-lg font-semibold rounded-lg bg-blue-700 hover:bg-blue-800 focus:outline-none transition duration-300 text-white"
                >
                  Get Started
                </button>
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginForm;
