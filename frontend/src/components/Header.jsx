import React from 'react'
import Help from './Help'
import Stats from './Stats'
import Settings from './Settings';
import "../index.css"

const Header = () => {
  return (
    <header className='flex flex-col sm:flex-row justify-between items-center my-4 border-b-2 border-[--foreground]'>
        <div className='flex flex-col sm:flex-row items-center space-x-4 pb-4 pt-2'>
            <div className='border-b-2 pb-2 sm:border-b-0 sm:border-r-2 sm:pb-0 border-[--foreground]'>
                <h1 className='font-serif text-red-900 pr-3 text-4xl'>Blessdle</h1>
            </div> 
            <div className='pt-2 sm:pt-0'>
                <h2>A <a className='text-red-500 hover:text-red-300 pr-1 italic underline' href='https://www.ufc.com/' target='_blank' rel='nofollow'>UFC</a> fighter </h2>
                <h2>guessing game.</h2>
            </div>
        </div>
        <div className='flex justify-center items-center space-x-3 pr-2'>
            <Help />
            <Stats />
            <Settings />
        </div>
    </header>
  )
}

export default Header