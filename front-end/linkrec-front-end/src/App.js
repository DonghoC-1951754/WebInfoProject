import logo from "./logo.svg";
import "./App.css";
import Header from "./components/Header";
import LoginForm from "./components/LoginForm";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import RegisterForm from "./components/RegisterForm";
import ProfileCreationForm from "./components/ProfileCreationForm";
import Profiles from "./components/Profiles";

function App() {
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
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
