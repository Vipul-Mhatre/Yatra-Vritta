import React from 'react';
import { Link } from 'react-router-dom';



const PlanningTool = () => {
    return (
        <div className='bg-gray-700'>
             <div>
            <div className='bg-teal-400'>
            <h1 className='pt-2 text-3xl font-bold'>Planning Tool</h1>
            <br />
            <h3 className='pb-2 text-xl font-semibold'> Explore Planning Tool </h3>
            </div>
            
        <div className='grid grid-cols-1 sm:grid-cols-2   gap-4 bg-secondary '>
    
           <div class="max-w-sm mt-10 mb-5 mr-5 ml-10 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/PlanningTool/Budget">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Budget</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://static.vecteezy.com/system/resources/previews/002/896/899/original/budget-plan-concept-symbol-illustration-in-flat-style-vector.jpg' alt='Photographer image' />
    <br />
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find your Wedding Plans according to your Budget!!!.</p>
    <br />
    <Link to="/PlanningTool/Budget" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start searching According to your Budget!!!
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div> 

        </div>
        
        </div>
        </div>
    );
};

export default PlanningTool;