const API_KEY = process.env.REACT_APP_API_KEY


/**
 * FoodCentral Data API search
 * @param {*} query 
 * @param {*} type 
 * @returns 
 */
export async function search(query, type) {
  const url = `https://api.nal.usda.gov/fdc/v1/foods/search?api_key=${API_KEY}`
  
  const payload = {
    query: query,
  }
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
  
  const data = await response.json()
  
  return data
}