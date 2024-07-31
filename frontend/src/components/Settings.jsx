import React, { useContext } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { LuSettings } from "react-icons/lu";
import { Switch } from "@/components/ui/switch"
import { useTheme } from "@/components/theme-provider"
import { RiMoonClearFill } from "react-icons/ri";
import { Separator } from '@/components/ui/separator';
import "../index.css";
import { AppContext } from '../App';

const Settings = () => {
  const {theme, setTheme} = useTheme();
  const {isHardMode, setIsHardMode} = useContext(AppContext);
  
  const onCheckedChange = () => {
    if (theme === 'dark') {
      setTheme('light');
    } else {
      setTheme('dark');
    }
  };
  
  return (
    <Dialog>
        <DialogTrigger>
          <div className='header-button border-slate-700 hover:bg-slate-100 hover:bg-opacity-50'>
            <div>
              <LuSettings className='text-3xl text-slate-600'/>
            </div> 
            <h3 className='text-sm'>Settings</h3>
          </div>
        </DialogTrigger>
        <DialogContent className='overflow-y-scroll max-h-screen'>
          <DialogHeader className='text-2xl font-bold'>
            Settings
          </DialogHeader>
          <DialogTitle>
          </DialogTitle>
          <div className='flex flex-col space-y-3'>
            <div className='flex justify-between items-center'>
              <div className='flex flex-col'>
                <h3>Hard Mode</h3>
                <p className='text-muted-foreground'>Solution's weight class will not be shown.</p>  
              </div>
              <Switch 
                checked={isHardMode}
                onCheckedChange={() => {setIsHardMode(!isHardMode)}}
              />
            </div>
            <Separator />
            <div className='flex justify-between'>
              <div className='flex items-baseline space-x-2'>
                <RiMoonClearFill className='text-xl pt-1'/>
                <h3>Dark Theme</h3>
              </div>
              <Switch 
                checked={theme === 'dark'}
                onCheckedChange={() => {onCheckedChange()}}
              />
            </div>
            <Separator />
            <div>
              <p className='text-base text-muted-foreground'>Questions? Bugs? Ideas? <a className="underline hover:text-destructive" href="https://forms.gle/s4rGBUxU9VMh4ZzAA" target='_blank' rel='nofollow'>Contact us.</a></p>
              <p className='text-base text-muted-foreground'>Enjoy Blessdle? <a className="underline hover:text-destructive" href="https://ko-fi.com/moonwater0" target='_blank' rel='nofollow'>Support us.</a></p>
            </div>
          </div>
        </DialogContent>
    </Dialog>
  )
}

export default Settings