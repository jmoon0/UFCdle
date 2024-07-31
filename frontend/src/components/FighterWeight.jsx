import React, { useContext } from 'react'
import { AppContext } from '../App'

const FighterWeight = () => {
    const {solution} = useContext(AppContext);
  return (
    <div className='text-center mt-8'>
        <h2>Today's weight class: <span className='text-primary'>{solution.fighter ? solution.fighter.weightClass : "Loading..."}</span></h2>
    </div>
  )
}

export default FighterWeight