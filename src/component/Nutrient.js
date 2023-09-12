import React from 'react'


export default function Nutrient({data}) {
  return <div>
    {/* Nutrient #{data?.nutrientId},  */}
    <p className="nutrient name"> {data?.nutrientName} </p>
    
    {data?.value} {data?.unitName}
  </div>
}