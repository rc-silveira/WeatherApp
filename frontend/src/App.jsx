import { useState, useEffect } from "react"
import axios from "axios"

const API = "/api"

function App() {
  const [cities, setCities] = useState([])
  const [weather, setWeather] = useState([])
  const [newCity, setNewCity] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState([])

  useEffect(() => {
    fetchCities()
    fetchWeather()
  }, [])

  async function fetchCities() {
    const res = await axios.get(`${API}/cities`)
    setCities(res.data)
  }

  async function fetchWeather() {
    const res = await axios.get(`${API}/weather`)
    setWeather(res.data)
  }

  async function addCity() {
    if (!newCity.trim()) return
    await axios.post(`${API}/cities?name=${newCity}`)
    setNewCity("")
    fetchCities()
  }

  async function deleteCity(name) {
    await axios.delete(`${API}/cities/${name}`)
    fetchCities()
  }

  async function askAi() {
    const res = await axios.post(`${API}/ai/ask?question=${question}`)
    setAnswer([...answer, { question: question, answer: res.data.answer }])  }

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
      <h1>WeatherApp</h1>

      <h2>Cities</h2>
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          value={newCity}
          onChange={e => setNewCity(e.target.value)}
          placeholder="Add city..."
        />
        <button onClick={addCity}>Add</button>
      </div>
      <ul>
        {cities.map(city => (
          <li key={city.id}>
            {city.name}
            <button onClick={() => deleteCity(city.name)} style={{ marginLeft: 8 }}>
              Remover
            </button>
          </li>
        ))}
      </ul>
        <div style={{ marginBottom: 16 }}>
      <h2>Ask me anything</h2>

      <div style={{ marginBottom: 16 }}>
        {answer.map((item, index) => (
          <div key={index} style={{ marginBottom: 12 }}>
            <p><strong>You:</strong> {item.question}</p>
            <p><strong>AI:</strong> {item.answer}</p>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === "Enter" && askAi()}
          placeholder="Ask me anything..."
          style={{ flex: 1 }}
        />
        <button onClick={askAi}>Ask</button>
      </div>
    </div>
      <table border="1" cellPadding="8" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>City</th>
            <th>Temperature</th>
            <th>Description</th>
            <th>Humidity</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {weather.map(w => (
            <tr key={w.id}>
              <td>{w.city}</td>
              <td>{w.temperature}°C</td>
              <td>{w.description}</td>
              <td>{w.humidity}%</td>
              <td>{new Date(w.forecast_datetime).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App