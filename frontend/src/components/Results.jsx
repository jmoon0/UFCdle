import React, { useContext, useState, useEffect } from 'react'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog"
import { AppContext } from '../App'
import GuessChart from './charts/GuessChart'
import WinsChart from './charts/WinsChart'
import ConfettiExplosion from 'react-confetti-explosion';

const Results = () => {
    const {gameOver, solution, guesses} = useContext(AppContext);
    const [dialogOpen, setDialogOpen] = useState(gameOver.isOver);
    const [isExploding, setIsExploding] = React.useState(true);

    useEffect(() => {
      setDialogOpen(gameOver.isOver)
    }, [gameOver])

    const solutionLoaded = solution && solution.fighter && solution.fighter.name;

  return (
    <Dialog open={dialogOpen} onOpenChange={(open) => {setDialogOpen(open)}}>
        <DialogTrigger>
        </DialogTrigger>
        <DialogContent className="overflow-y-scroll max-h-[85vh] max-w-[85%]">
            <DialogHeader>
                <DialogTitle className="text-2xl font-bold" >Results</DialogTitle>
            </DialogHeader>
            {solutionLoaded ? (<div>
              <h3 className='mb-2'>Today's Fighter: <span className='underline text-primary'>{solution.fighter.name}</span></h3>
              {gameOver.isCorrect ? (
                  <div>
                    {isExploding && <div className='flex justify-center items-center'>
                        <ConfettiExplosion duration={2200} force={0.6} particleCount={40} width={400} onComplete={() => setIsExploding(false)} zIndex={300}/>
                      </div>}
                    <p>Congratulations! &#129395; You got it in <span className='text-green-400 font-semibold'>{guesses.length} guesses.</span></p>
                    <p>Come back tomorrow to see if you can get it again!</p>
                  </div>
                ) : (
                  <div>
                    <p>You lost! &#128531;</p>
                    <p>Come back tomorrow to try again!</p>
                  </div>
                )}
                <div>
                  <p className='text-sm text-muted-foreground'>Questions? Bugs? Ideas? <a className="underline hover:text-destructive" href="https://forms.gle/s4rGBUxU9VMh4ZzAA" target='_blank' rel='nofollow'>Contact us.</a></p>
                  <p className='text-sm text-muted-foreground'>Want to support the site? <a className="underline hover:text-destructive" href="https://ko-fi.com/moonwater0" target='_blank' rel='nofollow'>Send a kofi.</a></p>
                </div>
                <div className='mt-2 flex flex-col space-y-3'>
                  <WinsChart />
                  <GuessChart />
                </div>
            </div>) : (<div>Loading...</div>)}
        </DialogContent>
    </Dialog>
  )
}

export default Results