import React, {useState, createContext, useEffect} from 'react'
import Header from './components/Header';
import FighterSearch from './components/FighterSearch';
import GuessTable from './components/GuessTable';
import Footer from './components/Footer'
import Results from './components/Results'
import { ThemeProvider } from "@/components/theme-provider"
import { toast, Toaster } from 'sonner'

export const AppContext = createContext();

const App = () => {
  const [solution, setSolution] = useState(() => {
    const savedSolution = JSON.parse(localStorage.getItem("solution"));
    return savedSolution ? savedSolution : {};
  })

  const [guesses, setGuesses] = useState(() => {
    const savedGuesses = JSON.parse(localStorage.getItem("guesses"));
    return savedGuesses ? savedGuesses : [];
  });

  const [gameOver, setGameOver] = useState(() => {
    const savedGameOver = JSON.parse(localStorage.getItem("gameOver"));
    return savedGameOver ? savedGameOver : {isOver: false, isCorrect: false};
  });

  const [stats, setStats] = useState(() => {
    const savedStats = JSON.parse(localStorage.getItem("stats"));
    return savedStats ? savedStats : {gamesPlayed: 0, wins: 0, currentStreak: 0, longestStreak: 0, guessDistribution: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,}};
  })

  const fetchSolution = async () => {
    try{
      const response = await fetch("http://127.0.0.1:5000/api/daily-fighter")
      const dailyFighter = await response.json();
      localStorage.setItem("solution", JSON.stringify(dailyFighter));
      localStorage.setItem("solutionDate", getESTDate());
      setSolution(dailyFighter)
    } catch(error){
      toast.error(`Error fetching fighter: ${error}`)
    }
    
  }

  const getESTDate = () => {
    const now = new Date();
    return new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' })).toDateString();
  };

  //Reset solution, guesses, and gameOver states if its a new day (est)
  useEffect(() => {
    const today = getESTDate(); 
    const solutionDate = localStorage.getItem("solutionDate") || today;

    if (solutionDate !== today || Object.keys(solution).length == 0) {
      fetchSolution();
      setGuesses([]);
      setGameOver({ isOver: false, isCorrect: false });
      localStorage.setItem("solutionDate", today)
    }

  }, []);
  
  //Save state to local storage
  useEffect(() => {
    localStorage.setItem("guesses", JSON.stringify(guesses));
  }, [guesses])
  
  useEffect(() => {
    localStorage.setItem("gameOver", JSON.stringify(gameOver));
  }, [gameOver])

  useEffect(() => {
    localStorage.setItem("stats", JSON.stringify(stats));
  }, [stats]);

  return (
    <AppContext.Provider value = {{solution, guesses, setGuesses, gameOver, setGameOver, stats, setStats}} >
      <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <Toaster richColors expand={false} position='top-center' visibleToasts={1} closeButton={true} toastOptions={{classNames:{title: 'text-lg'}}}/>
        <div className='max-w-screen-lg mx-auto my-1 min-h-screen flex flex-col px-4'>
          <div className='flex-grow'>
            <Header />
            <FighterSearch />
            <GuessTable />
            <Results />
          </div>
          <Footer />    
        </div>
        </ThemeProvider>
    </AppContext.Provider>
  )
}

export default App