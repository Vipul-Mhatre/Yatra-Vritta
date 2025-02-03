import { Alert, Button, Label, Spinner, TextInput } from "flowbite-react";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { HiInformationCircle } from "react-icons/hi";
import { useDispatch, useSelector } from "react-redux";
import { signInFailure, signInStart, signInSuccess } from "../Redux/Slice/userSlice.jsx";

const Signin = () => {
  const [formData, setFormData] = useState({});
  const dispatch = useDispatch();
  const { loading, error: errorMessage } = useSelector((state) => state.user);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value.trim() });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      return dispatch(signInFailure("Please fill out the fields"));
    }
    try {
      dispatch(signInStart());
      const response = await fetch('http://localhost:8888/api/auth/login-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      
      if (data.success === false) {
        return dispatch(signInFailure(data.message));
      }
      if (response.ok) {
        localStorage.setItem('Token', data.token);
        dispatch(signInSuccess(data));
        alert(data.message);
        navigate('/');
      }
    } catch (error) {
      alert("Please enter a valid username/password");
    }
  };

  return (
    <div className="min-h-screen mt-50">
      <div>
        <div>
          <div className="text-3xl font-semibold dark:text-white">
            <span className="px-2 py-1 bg-gradient-to-r from bg-pink-600 via-purple-500 to from-indigo-600 text-transparent bg-clip-text">
              Yatra Vritta
            </span>
          </div>
          <p className="text-m mt-6">
            You can sign up with your Email and password. This is a Demo Project***.
          </p>
          <br />
        </div>
      </div>
      <div className="flex-1">
        <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
          <div>
            <Label className="mx-5" value="Email" />
            <TextInput
              className="mx-5"
              type="email"
              placeholder="name@company.com"
              id="email"
              onChange={handleChange}
            />
          </div>
          <div>
            <Label value="Password" className="mx-5" />
            <TextInput
              className="mx-5"
              type="password"
              placeholder="Enter Your Password"
              id="password"
              onChange={handleChange}
            />
          </div>
          {errorMessage && (
            <Alert color="failure" icon={HiInformationCircle} className="mt-5">
              <span className="font-medium me-2">🥴 OOPS!</span>{errorMessage}
            </Alert>
          )}
          <Button className="mx-5" type="submit">
            Login
          </Button>
        </form>
        <div className="flex gap-2 text-sm mt-6">
          <span>Don't Have An Account?</span>
          <Link to="/Signup" className="font-semibold text-blue-700">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Signin;
