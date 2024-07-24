import {useContext} from 'react'
import { ChartContainer, ChartTooltipContent, ChartTooltip } from "@/components/ui/chart"
import { Bar, BarChart, XAxis, CartesianGrid } from "recharts"
import { AppContext } from '../../App';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
import "../../index.css"

const GuessChart = () => {
    const {stats} = useContext(AppContext);

    const chartData = [
        {category: "1", amount: stats.guessDistribution[1],},
        {category: "2", amount: stats.guessDistribution[2],},
        {category: "3", amount: stats.guessDistribution[3],},
        {category: "4", amount: stats.guessDistribution[4],},
        {category: "5", amount: stats.guessDistribution[5],},
        {category: "6", amount: stats.guessDistribution[6],},
        {category: "7", amount: stats.guessDistribution[7],},
        {category: "8", amount: stats.guessDistribution[8],},
    ];
    
    const chartConfig = {
        amount: {
            label: "Amount",
            color: "hsl(var(--primary))"
        }
    };

  return (
    <Card className="w-full max-w-[100vw]">
        <CardHeader>
            <CardTitle className="text-2xl font-bold" >Guess Distribution</CardTitle>
            <CardDescription></CardDescription>
        </CardHeader>
        <CardContent>
            <div>
                <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
                    <BarChart accessibilityLayer data={chartData}>
                        <CartesianGrid vertical={false} />
                        <XAxis 
                            dataKey="category"
                            type="category"
                            tickLine={false}
                            axisLine={false}
                        />
                        <ChartTooltip content={<ChartTooltipContent />} />
                        <Bar dataKey="amount" fill="hsl(var(--primary))" radius={4}/>
                    </BarChart>
                </ChartContainer>
            </div>
        </CardContent>
        <CardFooter>
        </CardFooter>
    </Card>
  )
}

export default GuessChart