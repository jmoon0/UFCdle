import React, { useContext } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { LuBarChart3 } from "react-icons/lu";
import "../index.css"
import WinsChart from './charts/WinsChart';
import GuessChart from './charts/GuessChart';

const Stats = () => {

  return (
    <Dialog>
        <DialogTrigger>
          <div className='header-button border-amber-800 hover:bg-amber-500 hover:bg-opacity-50'>
            <div>
              <LuBarChart3 className='text-3xl text-amber-700'/>
            </div> 
            <h3 className='text-lg'>Stats</h3>
          </div>
        </DialogTrigger>
        <DialogContent className='overflow-y-scroll max-h-[90vh]'>
          <DialogHeader>
            <DialogTitle className='text-2xl font-bold'>
                Stats
            </DialogTitle>
          </DialogHeader>
          <div className='flex flex-col space-y-3'>
            <WinsChart />
            <GuessChart />
          </div>
        </DialogContent>
    </Dialog>
  )
}

export default Stats