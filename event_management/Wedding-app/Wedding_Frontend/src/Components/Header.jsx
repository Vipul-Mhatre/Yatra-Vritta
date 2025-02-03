import React from "react";
import { Link, useLocation } from "react-router-dom";

import { FaMoon, FaSun } from "react-icons/fa";
import {
  Avatar,
  Button,
  Dropdown,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  Navbar,
  NavbarCollapse,
  TextInput,
} from "flowbite-react";
import { useDispatch, useSelector } from "react-redux";
import { toggleTheme } from "../Redux/Slice/themeSlice";
import { signOutSuccess } from "../Redux/Slice/userSlice";


const Header = () => {
  const path = useLocation().pathname;
  const dispatch = useDispatch();
  const { currentuser } = useSelector((state) => state.user);
   const { theme } = useSelector((state)=>state.theme);
    const handleSignout = ()=>{
        dispatch(signOutSuccess())
        localStorage.removeItem("token")
    }

  return (
    <Navbar className="border-b-2 dark:bg-black bg-blue-100">
      <Link
        to="/"
        className="self-center whitespace-nowrap text-sm sm:text-xl font-semibold dark:text-white mr-auto"
      >
        <span className="px-2 py-1   font-bold text-2xl bg-gradient-to-r from bg-blue-500 to from-indigo-600 text-transparent bg-clip-text">
          WeddingWise
        </span>
      </Link>
      
      <div className="flex gap-5 order-2 ml-auto">
        {currentuser ? (
          <Dropdown
            arrowIcon={false}
            inline
            label={
              <Avatar
                alt="user"
                img={currentuser.rest.profilePicture}
                rounded
              />
            }
          >
            <DropdownHeader>
              <span className="block text-sm"> 👤<strong>{currentuser.rest.username}</strong></span>
              <br />
              <span className="block text-sm"> 📧<strong>{currentuser.rest.email}</strong></span>
            </DropdownHeader>

            
              
            
            <DropdownDivider />
            <Link to="/Signin">
            <DropdownItem onClick={handleSignout}> ⬅️ <strong className="text-red-700">Sign out</strong></DropdownItem>
            </Link>
          </Dropdown>
        ) : (
          <Link to="/Signin">
            <Button gradientMonochrome="cyan">SignIn</Button>
          </Link>
        )}
        
        <Navbar.Toggle />
      </div>
      <NavbarCollapse>
        <div className="relative group ">
          <Navbar.Link active={path === "/PlanningTool"} as={"div"}>
            <Link to="/PlanningTool" className="font-bold">PlanningTool</Link>
          </Navbar.Link>

          <div className="md:absolute left-0 top-full hidden group-hover:flex flex-col mt-2 bg-white shadow-lg">
            <Link
              to="/PlanningTool/Budget"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Budget
            </Link>
           
          </div>
        </div>
        <div className="relative group">
          <Navbar.Link active={path === "/WeddingVendor"} as={"div"}>
            <Link to="/WeddingVendor" className="font-bold">WeddingVendor</Link>
          </Navbar.Link>
          <div className=" md:absolute left-0 top-full hidden group-hover:flex flex-col mt-2 bg-white shadow-lg">
            <Link
              to="/WeddingVendor/WeddingPhotographers"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Wedding Photographers
            </Link>
            <Link
              to="/WeddingVendor/WeddingVideographers"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Wedding Videographers
            </Link>
            <Link
              to="/WeddingVendor/WeddingPlanners"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Wedding Planners
            </Link>
            <Link
              to="/WeddingVendor/Caterers"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Caterers
            </Link>
          </div>
        </div>
        <div className="relative group">
          <Navbar.Link active={path === "/WeddingVenue"} as={"div"}>
            <Link to="/WeddingVenue" className="font-bold">WeddingVenue</Link>
          </Navbar.Link>
          <div className=" md:absolute left-0 top-full hidden group-hover:flex flex-col mt-2 bg-white shadow-lg">
            <Link
              to="/WeddingVenue/Banquet"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Banquet Halls
            </Link>
            <Link
              to="/WeddingVenue/WeddingResort"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Wedding Resorts
            </Link>
            <Link
              to="/WeddingVenue/Mandapam"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Kalyana Mandapams
            </Link>
          </div>
        </div>
        <div className="relative group">
          <Navbar.Link active={path === "/Bride"} as={"div"}>
            <Link to="/Bride" className="font-bold">Bride</Link>
          </Navbar.Link>
          <div className=" md:absolute left-0 top-full hidden group-hover:flex flex-col mt-2 bg-white shadow-lg">
            <Link
              to="/Bride/MehndiArtists"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Mehndi Artists
            </Link>
            <Link
              to="/Bride/MakeupArtists"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Bridal Makeup Artists
            </Link>
          </div>
        </div>
        <div className="relative group">
          <Navbar.Link active={path === "/Groom"} as={"div"}>
            <Link to="/Groom" className="font-bold ">Groom</Link>
          </Navbar.Link>
          <div className=" md:absolute left-0 top-full hidden group-hover:flex flex-col mt-2 bg-white shadow-lg">
            <Link
              to="/Groom/Dress"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Sherwani
            </Link>
            <Link
              to="/Groom/GroomMakeup"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Groom Makeup Artists
            </Link>
          </div>
        </div>
      </NavbarCollapse>
    </Navbar>
  );
};

export default Header;
