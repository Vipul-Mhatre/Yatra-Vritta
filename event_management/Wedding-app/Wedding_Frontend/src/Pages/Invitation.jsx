
import React, { useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'flowbite-react' 
import {  Tooltip, TextInput } from 'flowbite-react';
import { Link } from 'react-router-dom';



const Invitation = () => {
    const [text] = useState('+91 1234567890');

const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };
    return (
        <div>
<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full  bg-fuchsia-200 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/1053/original/1280/jpg/evening-events.webp" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Miracle Wedding Cards</h5>
        </Link>
        <br />
        <p>Miracle Wedding Cards is a company based in the city of Chennai that specialises in premium and customised wedding invitation cards that you can choose for the biggest day in your life. Weddings are the new beginnings that are filled with love, compassion and festivities which marks the most special day in their life which they would remember for life. The first step of making such a grand event much more unique and everlasting is choosing the right kind of wedding invitation which would speak volumes about the kind of celebrations that you would be having. </p>
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
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.10</span>
    
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

<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full   bg-fuchsia-200 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/6579/original/1280/jpg/22550038-1509731929116881-5261351940483134530-n_15_186579.webp" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Wedding Invitation Cards </h5>
        </Link>
        <br />
        <p>Wedding Invitation Cards Chennai is a wedding card provider based in the city of Chennai. Wedding invitations are the beautiful and creative piece of information that first break the news of your wedding. It is imperative that if it is the first thing which your guests would be seeing in terms of your wedding preparations, it should be something unique and beautiful so that it can make a lasting impact on them, just like your wedding. If you are looking for a vendor who can provide you with that, then Wedding Invitation Cards Chennai is a name you should consider.</p>
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
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.8</span>
             
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

<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full  bg-fuchsia-200 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/6579/3_2/960/jpg/22492004-1509727852450622-8400186164059087962-n_15_186579.webp" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Shankesvar Cards</h5>
        </Link>
        <br />
        <p>Shankesvar Cards is an invitation company located in Mylapore which is situated in the city of Chennai. Offering a wide array of wedding card designs and patterns, they are a one-stop solution for each of your requirements for your wedding cards. They know the fact that your card is the main thing that connects with your guests and offers them your warm welcome to the great event and therefore, they guarantee to make it the best for you. If you are searching for a decent wedding card company to design and print astounding cards for you, then Shankesvar Cards is the go-to option for you.</p>
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
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs15</span>
             

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

export default Invitation;