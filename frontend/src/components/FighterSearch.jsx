import {useState, useEffect, useContext, useCallback} from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { AppContext } from '../App';
import debounce from 'lodash.debounce';
import { toast } from 'sonner'

const FighterSearch = () => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const {setGuesses, guesses, gameOver, setGameOver, setStats, stats} = useContext(AppContext);

  const onChange = (e) =>{
    setQuery(e.target.value);
  }

  const searchFighters = useCallback(
    debounce( async (searchQuery) => {
      if (searchQuery.length < 2) {
        setSuggestions([]);
        return;
      }

      setIsLoading(true);
      try {
        const response = await fetch(`https://ufcdle.onrender.com/api/search?q=${encodeURIComponent(searchQuery)}`);
        const data = await response.json();
        setSuggestions(data);
      } catch (error) {
        setSuggestions(["No fighters found."])
      } finally {
        setIsLoading(false);
      }
    }, 200),
    [],
  );
  
  const handleClick = (fighter) => {
    setQuery(fighter);
    setSuggestions([]);
  }

  const handleKeyDown = (e) => {
    if (suggestions.length === 0) return;
  
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prevIndex => 
          prevIndex < suggestions.length - 1 ? prevIndex + 1 : prevIndex
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prevIndex => prevIndex > 0 ? prevIndex - 1 : 0);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0) {
          handleClick(suggestions[selectedIndex]);
        } else if (suggestions.length > 0) {
          handleClick(suggestions[0]);
        }
        break;
    }
  };

  useEffect(() => {
    searchFighters(query);
    setSelectedIndex(-1);  
  }, [query, searchFighters])

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (query === "") {
      toast.error("Please insert a fighter.")
      return;
    }

    let selectedFighter = query;

    if (suggestions.length > 0 && selectedIndex === -1){
      selectedFighter = suggestions[0];
    } else if (selectedIndex >= 0){
      selectedFighter = suggestions[selectedIndex]
    }

    const url = "https://ufcdle.onrender.com/api/guess"
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 'name': selectedFighter }),
    }

    try {
      const response = await fetch(url, options);
      const data = await response.json();

      if (!data) {
        throw new Error('No data received from server');
      }  

      if (response.status === 404) {
        toast.error('Fighter not found.');
        return;
      }
      
      const newGuess = { "name": query, "comparison": data };
      setGuesses(prevGuesses => [...prevGuesses, newGuess]);
      setQuery("");

    } catch (error) {
      toast.error(error.message)
    }
  }

  // Effect to check and handle game over conditions
  useEffect(() => {
    if (guesses.length === 0 || gameOver.isOver) return; // Skip on initial render or if game is already over

    const latestGuess = guesses[guesses.length - 1];
    const attempts = guesses.length;

    if(latestGuess["comparison"]["name"]==="correct"){
      setGameOver({isOver: true, isCorrect: true,})
      setStats((prevStats) => {
        return {
          ...prevStats, 
          gamesPlayed: prevStats.gamesPlayed + 1,
          wins: prevStats.wins + 1,
          guessDistribution: {
            ...prevStats.guessDistribution,
            [attempts]: (prevStats.guessDistribution[attempts] || 0) + 1
          }
        }
      })

      if(stats.currentStreak == stats.longestStreak){
        setStats((prevStats) => {
          return {
            ...prevStats, 
            currentStreak: prevStats.currentStreak + 1,
            longestStreak: prevStats.longestStreak + 1,
          }
        })
      }

    } else if(guesses.length == 8 ){
      setGameOver({isOver: true, isCorrect: false})
      setStats((prevStats) => {
        return {
          ...prevStats,
          gamesPlayed: prevStats.gamesPlayed + 1,
          currentStreak: 0,
        }
      })
    }
  }, [guesses, setGameOver, setStats]);

  return (
    <div className='mt-14 mb-5'>
      <form onSubmit={handleSubmit} className='flex items-center justify-center space-x-4'>
        <div className='w-3/5 relative'>
          <Input 
            className="text-xl py-6"
            type="text"
            value={query}
            placeholder="Guess a fighter..." 
            onChange={onChange}
            disabled={gameOver.isOver}
            onKeyDown={(e) => handleKeyDown(e)}
          />
          {(suggestions.length > 0 || isLoading) && 
            <ul className='bg-background absolute w-full max-h-52 mt-1 overflow-y-scroll drop-shadow flex flex-col z-10'>
              {isLoading && <li className='text-xl p-2'>Loading...</li>}
              {suggestions.map((fighter, index) =>(
                <li 
                  key={index} 
                  className={`text-xl p-2 hover:bg-muted hover:font-semibold cursor-pointer ${index === selectedIndex ? 'bg-muted font-semibold' : ''}`}
                  onClick={() => handleClick(fighter)}
                  >{fighter}
                </li>
              ))}
            </ul>  
          }
        </div>
        <Button type="submit" className="text-xl p-6 w-1/6 hover:bg-red-700 drop-shadow-md" disabled={gameOver.isOver} >Guess</Button>
      </form>
    </div>
  )
}

export default FighterSearch