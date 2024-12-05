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
import UserProfile from "./components/UserProfile";
import CompanyProfile from "./components/CompanyProfile";
import Profiles from "./components/Profiles";
import Vacancies from "./components/Vacancies";
import EmptyPage from "./components/EmptyPage";
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);

  
  const userclient = new ApolloClient({
    uri: " http://127.0.0.1:5000/getusers", // Replace with your GraphQL API endpoint
    cache: new InMemoryCache({
      addTypename: false, // Disable __typename
    }),
  });

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
              path="/createCompany"
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
                <ApolloProvider client={userclient}>
                    <Profiles />
                </ApolloProvider>
              }
            />
            <Route
              exact
              path="/companyProfile/:id"
              element={
                <>
                    <CompanyProfile />
                </>
              }
            />
            <Route
              exact
              path="/userProfile/:id"
              element={
                <>
                    <UserProfile />
                </>
              }
            />
            <Route
              exact
              path="/vacancies"
              element={
                <>
                  {isLoggedIn ? (
                    <>
                      <Vacancies />
                    </>
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
