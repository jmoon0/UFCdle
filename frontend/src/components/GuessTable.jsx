import {useContext} from 'react'
import { AppContext } from '../App';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { GiPerspectiveDiceSixFacesRandom } from "react-icons/gi";
import { IoMdArrowRoundDown, IoMdArrowRoundUp } from "react-icons/io";

const GuessTable = () => {
  const {solution, guesses} = useContext(AppContext);
  const bonusStat = solution.bonusStat;
  const bonusStats = {
    "winsByKo": "KO/TKO Win %",
    "winsBySub": "Submission Win %",
    "sigStrikesAccuracy": "Strike Accuracy %",
    "sigStrikesDefense": "Strikes Defense %",
    "takedownDefense": "TD Defense %",
  };
  const bonusStatLabel = bonusStats[bonusStat];

  const getClassName = (comparisonResult) => {
    if(comparisonResult=="none" || comparisonResult==null){
      return;
    }

    if(comparisonResult=="correct"){
      return "bg-green-400 bg-opacity-65 border-b-2";
    } else if(comparisonResult.includes("close")){
      return "bg-yellow-400 bg-opacity-65 border-b-2";
    } else{
      return "bg-muted bg-opacity-65 border-b-2";
    }
  }

  const getArrow = (comparisonResult) => {
    if(comparisonResult.includes("higher")){
      return (<IoMdArrowRoundUp className='inline pb-1'/>)
    } else if(comparisonResult.includes("lower")){
      return (<IoMdArrowRoundDown className='inline pb-1'/>)
    } else{
      return null;
    }
  }

  return (
    <Table className="mt-3 overflow-x-auto">
      <TableCaption className="text text-left sm:text-center sm:text-lg">Guess {guesses.length} of 8.</TableCaption>
      <TableHeader className='text-lg border-b-2 text-[--foreground]'>
        <TableRow className="border-b-2 border-[--border] w-full relative font-bold">
          <TableHead className="w-1/5" >Name</TableHead>
          <TableHead className="w-[10%]" >Wins</TableHead>
          <TableHead className="w-[10%]" >Losses</TableHead>
          <TableHead className="w-1/5" >Weight Class</TableHead>
          <TableHead className="w-[10%]" >Height</TableHead>
          <TableHead className="w-[10%]" >Age</TableHead>
          <TableHead className="w-1/5 text-rose-500" ><GiPerspectiveDiceSixFacesRandom className="inline pr-1 text-3xl pb-1" />{bonusStatLabel}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {guesses.map((guess, index) => {
          const stat = guess["comparison"]["guess"];
          const result = guess["comparison"]

          return (
            <TableRow key={index} className="w-full relative font-semibold text-lg text-center">
              <TableCell className={`w-1/5 border-b-2 ${getClassName(result["name"])}`}>
                {guess["name"]}
              </TableCell>
              <TableCell className={`w-[10%] ${getClassName(result["wins"])}`}>
                {stat["wins"]} {getArrow(result["wins"])}
              </TableCell>
              <TableCell className={`w-[10%] ${getClassName(result["losses"])}`}>
                {stat["losses"]} {getArrow(result["losses"])}
              </TableCell>
              <TableCell className={`w-1/5 ${getClassName(result["weightClass"])}`}>
                {stat["weightClass"]} {getArrow(result["weightClass"])}
              </TableCell>
              <TableCell className={`w-[10%] ${getClassName(result["height"])}`}>
                {stat["height"]} {getArrow(result["height"])}
              </TableCell>
              <TableCell className={`w-[10%] ${getClassName(result["age"])}`}>
                {stat["age"]} {getArrow(result["age"])}
              </TableCell>
              <TableCell className={`w-1/5 ${getClassName(result["bonus_stat"])}`}>
                {stat["bonusStats"][bonusStat]}%{getArrow(result["bonus_stat"])}
              </TableCell>
            </TableRow>
          )   
        })}
        {

        }
      </TableBody>
    </Table>
  )
}

export default GuessTable