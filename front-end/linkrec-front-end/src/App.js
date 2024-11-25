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

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route
            exact
            path="/"
            element={
              <>
                <Header /> <LoginForm />
              </>
            }
          />
          <Route
            exact
            path="/registration"
            element={
              <>
                <Header /> <RegisterForm />
              </>
            }
          />
          <Route
            exact
            path="/profile-creation"
            element={
              <>
                <Header /> <ProfileCreationForm />
              </>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
