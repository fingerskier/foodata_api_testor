import {useEffect, useState} from 'react'
import Nutrient from './Nutrient'
import {useFoodContext} from '../lib/foodContext'
import { weightToGrams } from '../lib/helpers'


export default function Food({data}) {
  const {eat} = useFoodContext()
  
  const [eating, setEating] = useState(false)
  const [nutrients, setNutrients] = useState([])
  
  
  const eatFood = (event)=>{
    event.preventDefault()
    
    const values = {}
    const formData = new FormData(event.target)
    
    formData.forEach((val,key)=>{
      values[key] = val
    })
    
    console.log('formdata', values)
    
    const grams = weightToGrams(values.quantity, values.unit)
    
    eat(data, grams)
    
    setEating(false)
    
    event.target.reset()
    
    return false
  }
  
  
  useEffect(() => {
    setNutrients(data.foodNutrients || [])
  }, [data.foodNutrients])
  
  
  function NutrientItem(el, I) {
    return <>
      <Nutrient key={I} data={el} />
      <hr />
    </>
  }
  
  
  function EatForm() {
    return <form onSubmit={eatFood}>
      <input type="hidden" name="id" value={data?.fdcId} />
      <input type="num" name="quantity" />
      
      <select name="unit">
        <option value="g">g</option>
        <option value="kg">kg</option>
        <option value="lb">lb</option>
        <option value="oz">oz</option>
        <option value="mg">mg</option>
      </select>
      
      <button>Ate</button>
    </form>
  }
  
  
  return <p className='food row'>
    <div className='food title'>
      {data?.brandName} {data?.description}
      <br />
      {data?.servingSize} {data?.servingSizeUnit}
    </div>
    
    {eating? <EatForm /> : <button onClick={E=>setEating(true)}>Eat</button> }
    
    <details className='nutrient details'>
      <summary>Nutrients</summary>
      
      {nutrients.map(NutrientItem)}
    </details>
  </p>
}