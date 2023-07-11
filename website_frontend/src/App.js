// import logo from './logo.svg';
import './App.css';
import Nav from './components/Nav';
import Home from './components/Home';
import Item from './components/Item';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Nav />
          <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="/items" element={<Item/>} />
          </Routes>
          <p>
            Orbital Website
          </p>
        </header>
      </div>
    </Router>
  );
}

export default App;
