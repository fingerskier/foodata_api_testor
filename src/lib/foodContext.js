import {createContext, useContext, useState} from 'react'
import useLocalStorage from './../hook/useLocalStorage'


export const FoodContext = createContext()


export function useFoodContext() {
  return useContext(FoodContext)
}


export default function FoodContextProvider({children}) {
  const [eaten, setEaten] = useLocalStorage('eatings', [])
  
  
  function eat(id, grams) {
    setEaten([...eaten, {
      id: id,
      grams: grams,
    }])
  }
  
  
  const state = {
    eat,
    eaten,
  }
  
  
  return <FoodContext.Provider value={state}>
    {children}
  </FoodContext.Provider>
}