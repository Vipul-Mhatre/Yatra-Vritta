import React from 'react';
import { Link } from 'react-router-dom';


const WeddingVendor = () => {
    return (
        <div className='bg-gray-700'>
            <div className='bg-teal-400'>
                <h1 className='pt-2 text-3xl font-bold'>Wedding Vendor</h1>
                <br />
                <h3 className='pb-2 text-xl font-semibold'> Explore Wedding Vendors by category</h3>
            </div>

            <div className='grid grid-cols-1 sm:grid-cols-2   gap-4 bg-secondary '>

                <div class="max-w-sm mt-10 mb-5 mr-5 ml-10 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
                    <Link to="/WeddingVendor/WeddingPhotographers">
                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Photographers</h5>
                    </Link>
                    <img className='mt-3 h-60 w-96' src='https://theurbanhousewife.com/wp-content/uploads/2019/08/Capturing-Your-Big-Day-How-to-Find-the-Best-Wedding-Photographer.jpg' alt='Photographer image' />
                    <br />
                    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the top-rated wedding photographer near you for your dream wedding!!!.</p>
                    <br />
                    <Link to="/WeddingVendor/WeddingPhotographers" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Start searching your wedding photographer!!!
                        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
                        </svg>
                    </Link>
                </div>

                <div class="max-w-sm mt-10 mb-5 mr-5 ml-10 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
                    <Link to="/WeddingVendor/Weddingvideographers">
                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Videographers</h5>
                    </Link>
                    <img className='mt-3 h-60 w-96' src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzBWo5-jaloQSzlRe5hNRqrf0BfHxqnxqgvA&s' alt='Videographer image' />
                    <br />
                    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the top-rated wedding videographer near you to capture the dreamy moments of your dreamy day!!!.</p>
                    <br />
                    <Link to="/WeddingVendor/Weddingvideographers" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Start searching your wedding videographer!!!
                        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
                        </svg>
                    </Link>
                </div>
                <div class="max-w-sm mt-10 mb-5 mr-5 ml-10 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
                    <Link to="/WeddingVendor/WeddingPlanners">
                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Planners</h5>
                    </Link>
                    <img className='mt-3 h-60 w-96' src='https://badhaihoevents.in/wp-content/uploads/2022/07/mandap-fi-1.jpeg' alt='Planner image' />
                    <br />
                    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the top-rated wedding planner near you to organise your dreamy day!!!.</p>
                    <br />
                    <Link to="/WeddingVendor/WeddingPlanners" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Start searching your wedding planner!!!
                        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
                        </svg>
                    </Link>
                </div>

                <div class="max-w-sm mt-10 mb-5 mr-5 ml-10 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
                    <Link to="/WeddingVendor/Caterers">
                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Caterers</h5>
                    </Link>
                    <img className='mt-3 h-60 w-96' src='https://mehroliacaterers.com/wp-content/uploads/2021/02/chasse-sauvage-zlUGL4hBHcw-unsplash-1536x1026.jpg' alt='caterers image' />
                    <br />
                    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the best wedding caterers to fulfil your guests' tastebuds.</p>
                    <br />
                    <Link to="/WeddingVendor/Caterers" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Start searching your wedding caterers!!!
                        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
                        </svg>
                    </Link>
                </div>
            </div>
        </div>


    );
};

export default WeddingVendor;