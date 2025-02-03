
import React, { useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'flowbite-react'
import { Tooltip, TextInput } from 'flowbite-react';
import { Link } from 'react-router-dom';



const Banquet = () => {
  const [text] = useState('+91 1234567890');

  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };
  return (
    <div>
      <div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full bg-fuchsia-300 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        <Link to="#">
          <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/1791/3_2/1280/jpeg/neelams-grande-render-1-2_15_71791-170792023653514.webp" alt="Photography image" />
        </Link>
        <div class="px-5 pb-5 ">
          <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Neelam The Grand</h5>
          </Link>
          <br />
          <p>Neelam The Grand stands as a remarkable architectural marvel in Goa, boasting a contemporary ambience that captivates visitors. Infused with the charm of old Goan Portuguese hospitality, the resort exudes a unique allure reflected in the demeanour of its staff and the management's approach. Every member of the team is meticulously trained and consistently courteous, ensuring they cater to all your needs and desires, particularly during wedding functions and ceremonies. Your special occasions are handled with utmost care and attention, promising an unforgettable experience immersed in the rich cultural heritage of Goa. </p>
          <div class="flex items-center mt-24">
            <div class="flex items-center space-x-1 rtl:space-x-reverse">
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
            </div>
            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
          </div>
          <br />
          <div class="flex items-center justify-between" >
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.2000</span>

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
          <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/8754/3_2/1280/jpeg/whatsapp-image-2023-01-13-at-4-26-43-pm_15_58754-167379000694836.webp" alt="Photography image" />
        </Link>
        <div class="px-5 pb-5 ">
          <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Aquarius Resort </h5>
          </Link>
          <br />
          <p>Aquarius Resort is a hotel in Pune. It is located near the Khadakwasla Dam and the Sinhgad Fort, known for their world-class facilities and efficient services. Aquarius Resort will be an ideal location for your biggest event with its wonderful ambience and great hospitality. It is one of Pune's leading hotels for business and leisure travellers and a fabulous destination for auspicious ceremonies. With the decor designing and venue decoration as per your choices and wants, their hardworking team will ensure that your wedding is the grandest and most memorable event of your life. </p>
          <div class="flex items-center mt-24">
            <div class="flex items-center space-x-1 rtl:space-x-reverse">
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
            </div>
            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
          </div>
          <br />
          <div class="flex items-center justify-between" >
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.1500</span>

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

      <div class="my-2 flex flex-col lg:flex-row w-full h-max max-w-full bg-fuchsia-300 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        <Link to="#">
          <img class="p-8 rounded-t-lg h-96 max-w-96" src="https://cdn0.weddingwire.in/vendor/4331/original/1280/jpg/utthan-8_15_244331-169098468264635.webp" alt="Photography image" />
        </Link>
        <div class="px-5 pb-5 ">
          <Link to="#">
            <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white mt-7">Hotel Millennium Inn</h5>
          </Link>
          <br />
          <p>Hotel Millennium Inn is a venue located in the city of Ghaziabad that can be an ideal location to host any of your special occasions, especially your wedding or any of its other related functions, which you can be assured would be planned and hosted with perfection and in the most beautiful manner. Choosing the right venue is one of the most critical choices a bride and groom would make for their wedding. It speaks volumes about the kind of celebrations you would be having and binds all of your festivity together.</p>
          <div class="flex items-center mt-24">
            <div class="flex items-center space-x-1 rtl:space-x-reverse">
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
              <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" />
              </svg>
            </div>
            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
          </div>
          <br />
          <div class="flex items-center justify-between" >
            <span class="text-xl text-gray-900 font-light dark:text-white">From Rs.3000</span>


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

export default Banquet;