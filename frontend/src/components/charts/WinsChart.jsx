import {useContext} from 'react'
import { ChartContainer, ChartTooltipContent, ChartTooltip } from "@/components/ui/chart"
import { Bar, BarChart, XAxis, YAxis } from "recharts"
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
import { Separator } from "@/components/ui/separator"

const WinsChart = () => {
    const {stats} = useContext(AppContext);
    const wr = stats.gamesPlayed !== 0 ? 100*((stats.wins + 0.0)/ stats.gamesPlayed) : "0.0";

    const chartData = [
        {category: "Games Played", amount: stats.gamesPlayed,},
        {category: "Wins", amount: stats.wins,},
    ];
    
    const chartConfig = {
        amount: {
            label: "Amount:",
            color: "hsl(var(--destructive))"
        }
    };

  return (
    <Card>
        <CardHeader className="m-0 p-0">
            <CardTitle></CardTitle>
            <CardDescription></CardDescription>
        </CardHeader>
        <CardContent>
            <div>
                <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
                    <BarChart 
                        accessibilityLayer
                        data={chartData}
                        layout='vertical'
                    >
                        <XAxis type="number" dataKey="amount" hide/>
                        <YAxis 
                            dataKey="category"
                            type="category"
                            tickLine={false}
                            axisLine={false}
                        />
                        <ChartTooltip content={<ChartTooltipContent />} />
                        <Bar dataKey="amount" fill="hsl(var(--destructive))" radius={4} barSize={30} />
                    </BarChart>
                </ChartContainer>
            </div>
        </CardContent>
        <CardFooter>
        <div className="flex w-full items-center gap-2">
              <div className="grid flex-1 auto-rows-min gap-0.5">
                <div className="text-sm text-muted-foreground">Current Streak</div>
                <div className="flex items-baseline gap-1 text-2xl font-bold tabular-nums leading-none">
                  {stats.currentStreak}
                  <span className="text-xs font-normal text-muted-foreground">
                     games
                  </span>
                </div>
              </div>
              <Separator orientation="vertical" className="mx-2 h-10 w-px" />
              <div className="grid flex-1 auto-rows-min gap-0.5">
                <div className="text-sm text-muted-foreground">Longest Streak</div>
                <div className="flex items-baseline gap-1 text-2xl font-bold tabular-nums leading-none">
                  {stats.longestStreak}
                  <span className="text-xs font-normal text-muted-foreground">
                     games
                  </span>
                </div>
              </div>
              <Separator orientation="vertical" className="mx-2 h-10 w-px" />
              <div className="grid flex-1 auto-rows-min gap-0.5">
                <div className="text-sm text-muted-foreground">Win Percentage</div>
                <div className="flex items-baseline gap-1 text-2xl font-bold tabular-nums leading-none">
                  {wr}
                  <span className="text-sm font-normal text-muted-foreground">
                    %
                  </span>
                </div>
              </div>
            </div>
        </CardFooter>
    </Card>
  )
}

export default WinsChart