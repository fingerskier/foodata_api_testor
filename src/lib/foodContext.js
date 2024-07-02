import {createContext, useContext, useState} from 'react'
import useLocalStorage from './../hook/useLocalStorage'


export const FoodContext = createContext()


export function useFoodContext() {
  return useContext(FoodContext)
}


export default function FoodContextProvider({children}) {
  const [eaten, setEaten] = useLocalStorage('foods', [])
  const [feedings, setFeedings] = useLocalStorage('feedings', [])
  
  
  function eat(food, grams) {
    setFeedings([
      ...feedings, 
    {
      id: food.id,
      grams: grams,
    }])
    
    setEaten([
      ...eaten,
      food,
    ])
  }
  
  
  const state = {
    eat,
    eaten: feedings,
  }
  
  
  return <FoodContext.Provider value={state}>
    {children}
  </FoodContext.Provider>
}