
import React, { useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'flowbite-react' 
import {  Tooltip, TextInput } from 'flowbite-react';
import { Link } from 'react-router-dom';



const Mandapam = () => {
    const [text] = useState('+91 1234567890');

const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };
    return (
        <div>
<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full bg-fuchsia-300 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/8273/3_2/1280/jpg/660a9150-77d8-43d6-9c1b-473068c4bd82_15_188273.webp" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">RS Mahal</h5>
        </Link>
        <br />
        <p>RS Mahal is a banquet hall located in Nagarbhavi which is situated in West Bangalore. The wedding is a great occasion among the most valuable and unique events in a person's life and it is imperative that everything is perfect on this fantastic day. Ideating and organising an ideal wedding also incorporate picking the right venue according to your prerequisites. </p>
        <div class="flex items-center mt-24">
            <div class="flex items-center space-x-1 rtl:space-x-reverse">
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
            </div>
            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
        </div>
        <br />
        <div class="flex items-center justify-between" >
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.100000</span>
    
            <Button onClick={toggleModal} className='sm:ml-80'>
              Request Order
            </Button>
            <Modal show={isOpen} onClose={toggleModal} >
              <ModalHeader className='mb-6 bg-stone-300'>
                Enter Details
              </ModalHeader>
              <ModalBody>
                <div className="relative flex items-center space-x-2 ring-offset-blue-600">
                  <label for="Date">Contact:</label>
                  <TextInput
                    type="text"
                    value={text}
                    className="font-bold"
                  />
                  <br />
                  <label for="Date">Date:</label>
                  <input type="date" id="Date" name="Date" />
                  <br />
                  <Button
                  
                    color="primary"
                    className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                  >
                    Register
                  </Button>
                </div>
              </ModalBody>
              <ModalFooter>
                <Button onClick={toggleModal}>
                  Close
                </Button>

              </ModalFooter>
            </Modal>
    
  
  </div>

        </div>
</div>

<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full   bg-fuchsia-300 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/8602/3_2/960/jpg/weddingvenues-bhushan-banquet-hall-banquethall-3_15_428602-166737477526098.webp" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Riya Hall </h5>
        </Link>
        <br />
        <p>Riya Hall is a beautiful wedding venue located in Koregaon, Mumbai. Look no further if you are looking for a banquet hall while planning your wedding in town. The decor and ambience of the place offer a perfect blend of simplicity and comfort. It would be best if you definitely had the ideal venue to organise a grand and flawless wedding. If you are looking for a great platform to host any of your wedding functions, then Bhushan Banquet Hal is the choice that you should definitely make.</p>
        <div class="flex items-center mt-24">
            <div class="flex items-center space-x-1 rtl:space-x-reverse">
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
            </div>
            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
        </div>
        <br />
        <div class="flex items-center justify-between" >
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.2,00000</span>
             
            <Button onClick={toggleModal} className='sm:ml-80'>
              Request Order
            </Button>
            <Modal show={isOpen} onClose={toggleModal} >
              <ModalHeader className='mb-6 bg-stone-300'>
                Enter Details
              </ModalHeader>
              <ModalBody>
                <div className="relative flex items-center space-x-2 ring-offset-blue-600">
                  <label for="Date">Contact:</label>
                  <TextInput
                    type="text"
                    value={text}
                    className="font-bold"
                  />
                  <br />
                  <label for="Date">Date:</label>
                  <input type="date" id="Date" name="Date" />
                  <br />
                  <Button
                  
                    color="primary"
                    className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                  >
                    Register
                  </Button>
                </div>
              </ModalBody>
              <ModalFooter>
                <Button onClick={toggleModal}>
                  Close
                </Button>

              </ModalFooter>
            </Modal>
        </div>
    </div>
</div>

<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full  bg-fuchsia-300 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/6803/original/1280/jpg/banquet-hall-hyath-mahal-banquet-hall-1_15_356803-161365567526515.webp" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">KBS Mahal</h5>
        </Link>
        <br />
        <p>KBS Mahal is a wedding venue based in Chennai. The management team and the service staff is only there to assist and help you, as they provide you with full flexibility to host your event your way. With numerous picture-perfect and pocket-friendly wedding planning packages, your dreams are met by a team of dedicated, professional and motivated individuals loving what they do. You can host all of your special occasions with ease and comfort at Hyath Mahal and be assured that they would offer you all the facilities and amenities that you might need to host all of your functions with ease.</p>
        <div class="flex items-center mt-24">
            <div class="flex items-center space-x-1 rtl:space-x-reverse">
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
                <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
            </div>
            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
        </div>
        <br />
        <div class="flex items-center justify-between" >
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.2,50,000</span>
             

            <Button onClick={toggleModal} className='sm:ml-80'>
              Request Order
            </Button>
            <Modal show={isOpen} onClose={toggleModal} >
              <ModalHeader className='mb-6 bg-stone-300'>
                Enter Details
              </ModalHeader>
              <ModalBody>
                <div className="relative flex items-center space-x-2 ring-offset-blue-600">
                  <label for="Date">Contact:</label>
                  <TextInput
                    type="text"
                    value={text}
                    className="font-bold"
                  />
                  <br />
                  <label for="Date">Date:</label>
                  <input type="date" id="Date" name="Date" />
                  <br />
                  <Button
                  
                    color="primary"
                    className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                  >
                    Register
                  </Button>
                </div>
              </ModalBody>
              <ModalFooter>
                <Button onClick={toggleModal}>
                  Close
                </Button>

              </ModalFooter>
            </Modal>
    
</div>
        
    </div>
</div>
</div>

       
    );
};

export default Mandapam;