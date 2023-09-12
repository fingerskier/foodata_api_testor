import {useEffect, useState} from 'react'
import {search} from '../lib/api'
import Food from './Food'



export default function Search() {
  const [query, setQuery] = useState()
  const [meta, setMeta] = useState()
  const [foods, setFoods] = useState()


  const doSearch = async(event)=>{
    let result = await search(query)
    
    console.log('SEARCH RESULT', result)
    setMeta({
      totalHits: result.totalHits,
      currentPage: result.currentPage,
      totalPages: result.totalPages,
      pageList: result.pageList,
      criteria: result.foodSearchCriteria,
    })
    setFoods(result.foods)
  }


  function FoodItem(el, I) {
    return <Food key={I} data={el} />
  }


  return <div>
    Search

    <label>
      Query String

      <input
        onChange={E=>setQuery(E.target.value)}
        type="text"
        value={query}
      />
    </label>

    <button onClick={doSearch}>Search</button>

    <pre>
      {JSON.stringify(meta, null, 2)}
    </pre>

    {foods? foods.map(FoodItem): null}}
  </div>
}
