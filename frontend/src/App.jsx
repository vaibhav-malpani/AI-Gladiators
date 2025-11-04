import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import HomePage from './pages/HomePage'
import CreateFighterPage from './pages/CreateFighterPage'
import RosterPage from './pages/RosterPage'
import BattlePage from './pages/BattlePage'
import RankingsPage from './pages/RankingsPage'
import FighterDetailPage from './pages/FighterDetailPage'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#292524',
            color: '#fef3c7',
            border: '1px solid #d97706',
            fontFamily: 'Cinzel, serif',
          },
        }}
      />
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreateFighterPage />} />
          <Route path="/roster" element={<RosterPage />} />
          <Route path="/fighter/:id" element={<FighterDetailPage />} />
          <Route path="/battle" element={<BattlePage />} />
          <Route path="/rankings" element={<RankingsPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
