import React from "react";

function Header() {
  return (
    <header className="bg-gray-800 text-white py-4 ">
      <div className="max-w-8xl mx-auto px-12 flex items-center justify-between">
        {/* Logo */}
        <div className="text-2xl font-bold">
          <a href="/">LinkRec</a>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex space-x-8">
          <a href="/" className="hover:text-gray-400">
            Home
          </a>
          <a href="#about" className="hover:text-gray-400">
            About
          </a>
          <a href="/profiles" className="hover:text-gray-400">
            Profiles
          </a>
          <a href="#contact" className="hover:text-gray-400">
            Contact
          </a>
        </nav>
      </div>

      {/* Mobile Menu (Toggle for small screens) */}
      <div className="md:hidden flex items-center justify-between mt-4">
        <button className="text-white">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </div>
    </header>
  );
}

export default Header;
