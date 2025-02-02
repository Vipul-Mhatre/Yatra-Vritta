import { Alert, Button, TextInput } from 'flowbite-react';
import React, { useState } from 'react';
import { AiOutlineSearch } from "react-icons/ai";
import { Link, useNavigate } from 'react-router-dom';




const Home = () => {
   

  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSearch = (event) => {
    event.preventDefault();
    const searchTermLower = searchTerm.toLowerCase();

    if (searchTermLower === 'budget') {
      navigate('/budget');
    } else if (searchTermLower === 'wedding photographer' || searchTermLower === 'photographer' || searchTermLower === 'photo') {
      navigate('/WeddingVendor/WeddingPhotographers');
    } else if (searchTermLower === 'wedding videographer' || searchTermLower === 'videographer' || searchTermLower === 'video') {
      navigate('/WeddingVendor/Weddingvideographers');
    } else if (searchTermLower === 'caterers' || searchTermLower === 'catering') {
      navigate('/WeddingVendor/Caterers');
    } else if (searchTermLower === 'wedding planners' || searchTermLower === 'planners') {
      navigate('/WeddingVendor/WeddingPlanners');
    } else if (searchTermLower === 'banquet') {
      navigate('/WeddingVenue/Banquet');
    } else if (searchTermLower === 'wedding resort' || searchTermLower === 'resort') {
      navigate('/WeddingVenue/WeddingResort');
    } else if (searchTermLower === 'mandapam' || searchTermLower === 'mahal' || searchTermLower === 'marriage hall') {
      navigate('/WeddingVenue/Mandapam');
    } else if (searchTermLower === 'mehndi artists' || searchTermLower === 'mehndi') {
      navigate('/Bride/MehndiArtists');
    } else if (searchTermLower === 'makeup artists' || searchTermLower === 'makeup') {
      navigate('/Bride/MakeupArtists');
    } else if (searchTermLower === 'dress' || searchTermLower === 'sherwani') {
      navigate('/Groom/Dress');
    } else if (searchTermLower === 'makeup' || searchTermLower === 'groom makeup') {
      navigate('/Groom/GroomMakeup');
    } else {
      alert(`🚫🚫 ErrorMessage 🚫🚫 \nSearched Term not Found ❌❌`);
      navigate('/');
    }
  };

    
    
    return (
        <div className='bg-gray-700'>
            <div className='flex flex-wrap border-2 bg-blue-400 dark:bg-zinc-600'>
            <div className="flex-col ml-2 flex-grow">
            <h1 className='font-bold text-4xl mt-10'>Everything you need to <br />plan your event...</h1>
            <br />
            <br />
            <h3 className='flex'>Search local professionals with pricing, and more...</h3>
            <br />
            <br />
            <form onSubmit={handleSearch}>
            <TextInput
              type="text"
              placeholder="Search..."
              rightIcon={AiOutlineSearch}
              className='w-72'
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
             
        />
      </form>
      </div>
      <div className='flex justify-center items-center sm:ml-0 mt-3'>
<img className="rounded-full max-w-full h-auto " src="https://png.pngtree.com/png-vector/20230912/ourmid/pngtree-cute-black-in-love-couple-png-image_10023144.png" alt="image description" />
</div>
            </div>


            <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 bg-secondary'>
            <div className="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to ="/WeddingVenue">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Venues</h5>
    </Link>
    <img className='mt-3 h-60' src='https://www.wedding-spot.com/blog/sites/wsblog/files/images/migrated/78-Fitroy%2Bwedding%2Bvenue.jpg' alt='wedding image' />
    <br />
    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Photos, reviews, and so much more... get in touch from here!</p>
    <br />
    <Link to="/WeddingVenue" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Explore venues
        <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>

<div className="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/WeddingVendor">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Wedding Vendors</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://www.brides.com/thmb/x5JqyLehHlFFjfSYhwqYQkMGZZ4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-1177485677-c89e88c4ce934e0092ba52f6aa6e29b9.jpg' alt='Vendor image' />
    <br />
    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Find the top-rated wedding vendors near you in every category.</p>
    <br />
    <Link to="/WeddingVendor" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Start Searching Your Vendor
        <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>


<div className="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/Bride">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Bride</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://images.shaadisaga.com/shaadisaga_production/photos/pictures/000/805/153/new_medium/fotoart_by_sami_irani.jpg?1554793567' alt='Bride image' />
    <br />
    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">The bride is the heart of every wedding, bringing grace, beauty, and joy to the occasion..</p>
    
    <Link to="/Bride" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Click here 
        <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>

<div className="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/Grrom">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Groom</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://i.pinimg.com/736x/6c/05/a4/6c05a4a0d81cc20bc8980a65e226edf7.jpg' alt='Groom image' />
    <br />
    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Look your best on your big day with our bespoke groom attire and expert grooming services!</p>
    <br />
    <Link to="/Groom" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Check here 
        <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>

<div className="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/invitation">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Invitation Card</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://myshadicards.com/wp-content/uploads/2021/09/Creative-Invitation-Card-7111-Cardset.webp' alt='Groom image' />
    <br />
    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Make your first impression unforgettable with our elegant and unique wedding invitation cards!</p>
    <br />
    <Link to="/invitation" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Explore cards
        <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>

<div className="max-w-sm mt-10 mb-5 ml-6 mr-3 p-6 hover:bg-violet-300 bg-white border border-gray-200 rounded-lg shadow  dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-black"  >
    <Link to="/PlanningTool">
        <h5 className
        ="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white hover:text-blue-500 dark:hover:text-blue-500  " >Planning Tool</h5>
    </Link>
    <img className='mt-3 h-60 w-96' src='https://static.vecteezy.com/system/resources/previews/001/879/416/non_2x/planning-monthly-budget-for-shopping-and-purchase-manage-financial-plan-with-calculator-financial-consulting-software-banking-accounting-platform-illustration-of-website-banner-software-poster-free-vector.jpg' alt='PlanningTool image' />
    <br />
    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Custom planning tools to manage your budget and vendors.</p>
    <br />
    <Link to="/PlanningTool" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-950 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Discover over Tools
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Link>
</div>


</div>

        </div>
        
        
    );
};

export default Home;