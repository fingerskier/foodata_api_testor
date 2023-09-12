import {useEffect, useState} from 'react'
import Nutrient from './Nutrient'


export default function Food({data}) {
  const [nutrients, setNutrients] = useState([])


  useEffect(() => {
    setNutrients(data.foodNutrients || [])
  }, [data.foodNutrients])
  

  function NutrientItem(el, I) {
    return <>
      <Nutrient key={I} data={el} />
      <hr />
    </>
  }


  return <p className='food row'>
    {/* #{data?.fdcId},  */}
    <div className='food title'>
      {data?.brandName} {data?.description}
      <br />
      {data?.servingSize} {data?.servingSizeUnit}
    </div>
    
    <details className='nutrient details'>
      <summary>Nutrients</summary>
      
      {nutrients.map(NutrientItem)}
    </details>
  </p>
}