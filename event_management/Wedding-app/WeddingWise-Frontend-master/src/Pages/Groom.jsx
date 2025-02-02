import React from 'react';
import { Link } from 'react-router-dom';



const Groom = () => {
    return (
        <div className='bg-gray-700'>
        <div className='bg-teal-400'>
            <h1 className='pt-2 text-3xl font-bold'>Groom</h1>
            <br />
            <h3 className='pb-2 text-xl font-semibold'> Explore Groom by category</h3>
            </div>
        <div className='grid grid-cols-1 sm:grid-cols-2 gap-3 bg-secondary' >
        <div class="max-w-sm mt-10 ml-10 mr-10 justify-evenly mb-5 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/Groom/Dress">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Sherwani</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://image.wedmegood.com/resized-nw/700X/wp-content/uploads/2020/02/1554111478_2.jpg' alt='sherwani image' />
    <br />
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the Sherwani Stores near you of your choice.</p>
    <br />
    <Link to="/Groom/Dress" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start Searching  Sherwani Stores
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>
<div class="max-w-sm mt-10 mb-5 ml-9 mr-10 p-6 hover:bg-violet-300   bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/Groom/GroomMakeup">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Groom Makeup Artists</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://www.skulptmakeupbar.com/chennai-wedding-makeup-artist/wp-content/uploads/2017/08/pre-groom-wedding-facial.jpg' alt='groom makeup image' />
    <br />
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the Makeup Artists near you to turn flawless on your special day.</p>
    <br />
    <Link to="/Groom/GroomMakeup" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start Searching Groom Makeup Artists
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>
</div>
</div>
    );
};

export default Groom;