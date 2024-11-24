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

function App() {
  return (
    <>
      <Router>
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
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
