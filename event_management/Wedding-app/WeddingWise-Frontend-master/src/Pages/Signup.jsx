import { Alert, Button, Label, Spinner, TextInput } from "flowbite-react";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { HiInformationCircle } from "react-icons/hi";

const Signup = () => {
    const [formData, setFormData] = useState({});
    const [loading,setLoading] = useState(false)
    const [errorMessage,setErrorMessage] = useState(null)
   const navigate = useNavigate();
    const handleChange = (e) => {
      //console.log(e.target.value);
      setFormData({ ...formData, [e.target.id]: e.target.value.trim() });
      //console.log(formData);
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      if(!formData.username || !formData.email || !formData.password){
          return setErrorMessage("please fill out the fields");
      }
      try {
          setLoading(true);
          setErrorMessage(null);
          const response = await fetch('http://localhost:8888/api/auth/register-user',{
              method:'POST',
              headers:{
                  'Content-Type':'application/json'
              },
              body:JSON.stringify(formData)
          })
          const data = await response.json();
          if(data.success === false){
              return setErrorMessage(data.message)
          }
          if(response.ok){
            alert(data.message);
              navigate('/signin');
          }
      } catch (error) {
        setErrorMessage(error.message)
        setLoading(false)
      }
    };
  
  return (
    <div className="min-h-screen mt-50">
      <div>
        <div>
          <div className=" text-3xl font-semibold dark:text-white">
            <span className="text-black">
              WeddingWise
            </span>
          </div>
          <p className="text-m mt-6">
            You can sign up with your Email and password.This is an Demo Project***.
          </p>
        </div>
      </div>
      <br />
        <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <div>
              <Label value="Username" className="mx-5"/>
              <TextInput
              className="mx-5"
                type="text"
                placeholder="Enter your User Name"
                id="username"
                onChange={handleChange}
              />
            </div>
            <div>
              <Label value="Email" className="mx-5" />
              <TextInput
                type="email"
                className="mx-5"
                placeholder="name@company.com"
                id="email"
                onChange={handleChange}
              />
            </div>
            <div>
              <Label value="Password" className="mx-5"/>
              <TextInput
                type="password"
                className="mx-5"
                placeholder="Enter Your Password"
                id="password"
                onChange={handleChange}
              />
        </div>
        {errorMessage && (
          <Alert color="failure" icon={HiInformationCircle} className="mt-5 mx-2">
            <span className="font-medium me-2">🥴OOPS!</span>{errorMessage}
          </Alert>
          )}
        <Button className="mx-5" type="submit" disabled={loading}>
          {loading ? (
            <>
         <Spinner color="purple" aria-label="Purple spinner example" size='sm'/>
         <span className="pl-3">Loading...</span>
            
            </>
          ) :(
            'Register'
          )}
        </Button>
        <div>
          <Link to="/Signin">
            <span> Have an account Already ???</span>
            <Link className="font-semibold text-blue-700" to="/Signin">Login</Link>
          </Link>
        </div>
        
      </form>
    </div>
  );
};

export default Signup;
