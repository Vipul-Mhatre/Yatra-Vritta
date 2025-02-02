 import React from 'react'
import { Link } from 'react-router-dom';



const WeddingVenue = () => {
    return (
        <div className='bg-gray-700'>
        <div className='bg-teal-400'>
            <h1 className='pt-2 text-3xl font-bold'>Wedding Venue</h1>
            <br />
            <h3 className='pb-2 text-xl font-semibold'> Explore Wedding Venue by category</h3>
            </div>
        <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 bg-secondary'>
        <div class="max-w-sm mt-10 mb-5 ml-5 mr-5 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/WeddingVenue/Banquet">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Banquet Halls</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://www.oyorooms.com/blog/wp-content/uploads/2018/03/fe-34.jpg' alt='banquet image' />
    <br />
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the banquet halls near you of your choice.</p>
    
    <Link to="/WeddingVenue/Banquet" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start Searching Banquet Halls
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>
<div class="max-w-sm mt-10 mb-5 ml-5 mr-5 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/WeddingVenue/WeddingResort">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Resorts</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://images.squarespace-cdn.com/content/v1/52ed3507e4b041396187d22b/1630387551794-PFADBQ27VD6WFWOJLBMI/Temple%2Bbay%2BMahabalipuram%2B%2BTelugu%2BWedding10.jpeg' alt='resort image' />
    <br />
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the resorts near you of your choice.</p>
    <br />
    <Link to="/WeddingVenue/WeddingResort" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start Searching Wedding Resorts
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>

<div class="max-w-sm mt-10 mb-5 ml-5 mr-5 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/WeddingVenue/Mandapam">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Marriage Halls</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://im.hunt.in/cg/poun/puducherry/City-Guide/Marriage-Halls.jpg' alt='mandapam image' />
    <br />
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the kalyana mandapam of your choice.</p>
    <br />
    <Link to="/WeddingVenue/Mandapam" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start Searching Kalyana Mandapam
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>
</div>

</div>
    );
};

export default WeddingVenue;