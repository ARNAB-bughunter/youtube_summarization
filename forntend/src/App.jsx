import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import UrlForm from './components/UrlForm'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
     <UrlForm />
    </>
  )
}

export default App
