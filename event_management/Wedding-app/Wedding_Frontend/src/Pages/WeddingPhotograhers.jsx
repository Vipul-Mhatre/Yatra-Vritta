
import React, { useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'flowbite-react' 
import {  Tooltip, TextInput } from 'flowbite-react';
import { Link } from 'react-router-dom';



const WeddingPhotograhers = () => {
    const [text] = useState('+91 1234567890');

const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };
    return (
        <div>
<div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full bg-fuchsia-200 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <Link to="#">
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/9168/3_2/960/jpg/wedding-photography-studiosix-by-chennai-wedding-photography-couple-shot-23_15_79168-158392634222558.jpeg" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Pondy Photography</h5>
        </Link>
        <br />
        <p>Pondy Photography is full of hardworking photographers and videographers who capture all the rare and serene moments of your ceremonies and makes sure that you are satisfied with the final outcome. They cover your functions in both, candid and traditional, styles of photography and videography and are also ready to travel outstations and be a part of your occasion to cover it with the utmost perfection.They offer a wide array of packages and services which you can select and personalize as per your requirements and the budget. </p>
        <div class="flex items-center mt-24 ">
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
                <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
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
            <span class="text-xl text-gray-900 font-light dark:text-white">Rs.90,000</span>
    
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
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXUt_Y5GqmtE_AsHieyqNyFFEHfVZ6duskWw&s" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Wedding Studio</h5>
        </Link>
        <br />
        <p>The Wedding Studio is a photography company based in Udaipur. They offer the best solution related to wedding photography and videography. Their images are not only beautiful, but they are also always alive with intense emotions, vigour and brilliance. They know the importance of your big occasion and ensure that the images depict the celebration with authenticity and warmth. If you are looking for a fantastic photography company to shoot your nuptial ceremonies, then this is the choice to make. </p>
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
            <span class="text-xl text-gray-900 font-light dark:text-white">Rs.1,50,000</span>
             
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
        <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXUt_Y5GqmtE_AsHieyqNyFFEHfVZ6duskWw&s" alt="Photography image" />
    </Link>
    <div class="px-5 pb-5 ">
        <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Green Studio</h5>
        </Link>
        <br />
        <p>The Green Studio Photography is a distinguished wedding photographer based in Panchkula. Selecting the right wedding photographer is paramount, and Ankush Khurana Photography recognises the significance of preserving every cherished moment in your love story. With a dedication to excellence, they bring a unique blend of creativity and expertise to ensure your wedding day is immortalised in breathtaking visuals. </p>
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
            <span class="text-xl text-gray-900 font-light dark:text-white">Rs.50,000</span>
             

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

export default WeddingPhotograhers;