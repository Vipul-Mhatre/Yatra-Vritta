import React, { useState } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'flowbite-react'
import { TextInput } from 'flowbite-react';
import { Link } from 'react-router-dom';


const Budget = () => {
  const [text] = useState('+91 1234567890');

  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };

  return (

    <div className='bg-gray-700 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3'>

      <div class="max-w-sm mt-10 mb-5 ml-6 p-6 hover:bg-red-200 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
        <Link to="/PlanningTool/Budget/Offerone">
          <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Combo in Two Lakhs</h5>
        </Link>
        <img className='mt-3 h-60 w-96' src='https://www.shutterstock.com/image-illustration/2-lakhs-word-on-white-260nw-1623800752.jpg' alt='twolakh image' />
        <br />
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          We have list of top planners & organisers for a hassle free wedding event planning. <br />Get a complete list of best wedding photographer,makeup,catering and much more in two lakh for your dream wedding in your budget.
        </p>
        <br />
        <Link to="/PlanningTool/Budget/Offerone" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Find your wedding combo in two lakhs
          <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
          </svg>
        </Link>
        <br />
        <br />
        <Button onClick={toggleModal} >
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

      <div class="max-w-sm mt-10 mb-5 ml-6 p-6 hover:bg-red-200 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
        <Link to="/PlanningTool/Budget/Offertwo">
          <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Combo in Four lakhs</h5>
        </Link>
        <img className='mt-3 h-60 w-96' src='https://www.shutterstock.com/image-illustration/4-lakhs-word-on-white-260nw-1623800740.jpg' alt='fourlakh image' />
        <br />
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          We have list of top planners & organisers for a hassle free wedding event planning.<br></br>Get a complete list of best wedding photographer,makeup,catering and much more in four lakh for your dream wedding in your budget.
        </p>
        <br />
        <Link to="/PlanningTool/Budget/Offertwo" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Find your wedding combo in four lakhs
          <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
          </svg>
        </Link>
        <br />
        <br />
        <Button onClick={toggleModal} >
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

      <div class="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-red-200 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
        <Link to="/PlanningTool/Budget/Offerthree">
          <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Combo in Six Lakhs</h5>
        </Link>
        <img className='mt-3 h-60 w-96' src='https://www.shutterstock.com/image-illustration/6-lakhs-word-on-white-260nw-1623800758.jpg' alt='sixlakh image' />
        <br />
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          We have list of top planners & organisers for a hassle free wedding event planning.<br></br> Get a complete list of best wedding photographer,makeup,catering and much more in six lakh for your dream wedding in your budget.
        </p>
        <br />
        <Link to="/PlanningTool/Budget/Offerthree" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Find your wedding combo in six lakhs
          <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
          </svg>
        </Link>
        <br />
        <br />
        <Button onClick={toggleModal} >
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
  );
};

export default Budget;