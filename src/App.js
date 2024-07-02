import './App.css'
import Search from './component/Search'
import FoodContextProvider from './lib/foodContext'


export default function App() {
  return <div className="App">
    <FoodContextProvider>
      <Search />
    </FoodContextProvider>
  </div>
}