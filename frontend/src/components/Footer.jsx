import React from 'react'

const Footer = () => {
  return (
    <footer className='flex flex-col items-end justify-evenly text-xs text-[--muted-foreground]'>
        <p>*Not affiliated with the UFC.</p>
        <p>&copy; Blessdle 2024.</p>
        <div className="underline space-x-1">
          <a href="https://forms.gle/s4rGBUxU9VMh4ZzAA" target='_blank' rel='nofollow' className='hover:text-muted-foreground'>Contact</a> 
          <a href="https://ko-fi.com/moonwater0" target='_blank' rel='nofollow' className='hover:text-muted-foreground'>Support</a>
        </div>
    </footer>
  )
}

export default Footer