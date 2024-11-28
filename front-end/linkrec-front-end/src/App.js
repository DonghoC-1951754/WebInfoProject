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
import ProfileCreationForm from "./components/ProfileCreationForm";
import Profiles from "./components/Profiles";
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
              path="/profile-creation"
              element={
                <>
                  <ProfileCreationForm />
                </>
              }
            />
            <Route
              exact
              path="/profiles"
              element={
                <>
                  <Profiles />
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
