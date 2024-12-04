import logo from "./logo.svg";
import "./App.css";
import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Header from "./components/Header";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import UserCreationForm from "./components/UserCreationForm";
import CompanyCreationForm from "./components/CompanyCreationForm";
import Users from "./components/Users";
import Vacancies from "./components/Vacancies";
import EmptyPage from "./components/EmptyPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);

  useEffect(() => {
    const userToken = localStorage.getItem("userToken");
    if (userToken) {
      setIsLoggedIn(true);
    }
  }, []);

  const login = () => {
    localStorage.setItem("userToken", "exampleToken");
    setIsLoggedIn(true);
  };

  // Logout Function
  const logout = () => {
    localStorage.removeItem("userToken");
    setIsLoggedIn(false);
  };

  return (
    <>
      <Router>
        <div class="flex flex-col h-screen">
          <Header />
          <Routes>
            <Route
              exact
              path="/"
              element={
                <>
                  <LoginForm />
                </>
              }
            />
            <Route
              exact
              path="/registration"
              element={
                <>
                  <RegisterForm />
                </>
              }
            />
            <Route
              exact
              path="/createUser"
              element={
                <>
                  <UserCreationForm />
                </>
              }
            />
            <Route
              exact
              path="/createBusiness"
              element={
                <>
                  <CompanyCreationForm />
                </>
              }
            />
            <Route
              exact
              path="/profiles"
              element={
                <>
                  <Users />
                </>
              }
            />
            <Route
              exact
              path="/vacancies"
              element={
                <>
                  {isLoggedIn ? (
                    <Vacancies/>
                  ) : (
                    <EmptyPage/>
                  )}
                </>
              }
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
