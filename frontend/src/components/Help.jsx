import React from 'react'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
 } from "@/components/ui/dialog"

 import { LuHelpCircle, } from "react-icons/lu";
 import "../index.css"

const Help = () => {
  return (
    <Dialog>
        <DialogTrigger>
          <div className='header-button border-blue-800 hover:bg-blue-500 hover:bg-opacity-25'>
            <div>
              <LuHelpCircle className='text-3xl text-blue-700 font-bold'/>
            </div> 
            <h3 className='text-lg'>Help</h3>
          </div>
        </DialogTrigger>
        <DialogContent className='overflow-y-scroll max-h-[90vh]'>
            <DialogHeader>
              <DialogTitle className='text-2xl font-bold mb-0 pb-0'>
                How to Play
              </DialogTitle>
            </DialogHeader>
            <DialogTitle>
            </DialogTitle>
            <div className='text-lg space-y-1'>
              <p>1. Guess the fighter in 8 guesses.</p>
              <p>2. <span className='font-semibold bg-green-500 px-2 py-[2px]'>Green</span> indicates an exact match.</p>
              <p>3. <span className='font-semibold bg-yellow-500 px-2 py-[2px]'>Yellow</span> indicates a close match where:</p>
              <ul className='pl-6 list-disc'>
                <li>
                  <span className='font-semibold italic'>Wins, losses, age,</span> or <span className='font-semibold italic'>height</span> are off by at most <b>3</b> (years, inches, etc.).
                </li>
                <li>
                  <span className='font-semibold italic'>Weight class</span> is <b>adjacent</b> to the solution (ex: LW &lt; WW &lt; MW)
                </li>
                <li>
                  <span className='font-semibold text-rose-500'>Bonus stat</span> is off by at most <b>5</b>.
                </li>
              </ul>
              <p>4. Fighter's weight class is based on the one they competed at in their last fight.</p>
              <p>5. New fighter and bonus stat is released everyday at midnight (EST).</p>
              <p>Possible <span className='font-semibold text-rose-500'>Bonus Stats</span>: KO/TKO win %, submission win %, strike accuracy %, strike defense %, takedown defense %.</p>
              <div className='pt-4 text-base text-muted-foreground space-y-1'>
                <p className='text-lg'>Questions? Bugs? Ideas? <a className="underline" href="https://forms.gle/s4rGBUxU9VMh4ZzAA" target='_blank' rel='nofollow'>Contact us.</a></p>
                <p className='text-lg'><span className='text-red-800 font-seirf font-semibold'>Blessdle</span> is named after the BMF, Max "Blessed" Holloway.</p>
                <p>*Fighters from <u>women's divisions</u> are currently not supported.</p>
                <p>*Fighter stats are updated every <u>Monday</u>, so they may be inaccurate the day after an event.</p>
              </div>    
            </div>
        </DialogContent>
    </Dialog>
  )
}

export default Help