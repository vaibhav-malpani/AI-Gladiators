import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Users, Trash2, Dumbbell, Eye } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function RosterPage() {
  const [fighters, setFighters] = useState([])
  const [loading, setLoading] = useState(true)

  const loadFighters = async () => {
    try {
      const response = await axios.get('/api/fighters')
      setFighters(response.data)
    } catch (error) {
      toast.error('Failed to load fighters')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadFighters()
  }, [])

  const handleDelete = async (fighterId, fighterName) => {
    if (!confirm(`Delete ${fighterName}? This cannot be undone!`)) return

    try {
      await axios.delete(`/api/fighters/${fighterId}`)
      toast.success(`${fighterName} has been removed from the arena`)
      loadFighters()
    } catch (error) {
      toast.error('Failed to delete fighter')
    }
  }

  const handleTrain = async (fighterId, fighterName) => {
    toast.loading(`Training ${fighterName}...`)

    try {
      const response = await axios.post(`/api/fighters/${fighterId}/train`)
      toast.dismiss()

      if (response.data.leveled_up) {
        toast.success(`🎉 ${fighterName} leveled up to ${response.data.new_level}!`, { duration: 4000 })
      } else {
        toast.success(`Training complete! Won ${response.data.wins}/3 sessions`)
      }

      loadFighters()
    } catch (error) {
      toast.dismiss()
      toast.error('Training failed')
    }
  }

  if (loading) {
    return (
      <div className="text-center py-20">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="inline-block"
        >
          <Users size={60} className="text-gold-500" />
        </motion.div>
        <p className="text-gold-300 mt-4">Loading warriors...</p>
      </div>
    )
  }

  if (fighters.length === 0) {
    return (
      <div className="text-center py-20">
        <Users size={80} className="text-gold-500/30 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-gold-400 mb-4">No Warriors Yet</h2>
        <p className="text-gold-200 mb-8">Create your first gladiator to begin!</p>
        <Link to="/create">
          <button className="px-8 py-4 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-lg rounded-lg glow-gold">
            ⚔️ CREATE WARRIOR
          </button>
        </Link>
      </div>
    )
  }

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold text-gold-400 mb-4 text-embossed font-trajan">
          YOUR WARRIORS
        </h1>
        <p className="text-xl text-gold-200">
          {fighters.length} Gladiator{fighters.length !== 1 ? 's' : ''} ready for battle
        </p>
      </motion.div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {fighters.map((fighter, i) => (
          <motion.div
            key={fighter.fighter_id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="glass p-6 rounded-lg bronze-border hover:scale-105 transition-transform duration-300"
          >
            <div className="text-center mb-4">
              <h3 className="text-2xl font-bold text-gold-400 mb-1 font-trajan">
                {fighter.name}
              </h3>
              <div className="text-sm text-gold-300/70">Level {fighter.level} Gladiator</div>
            </div>

            <div className="space-y-2 mb-4 text-sm">
              <div className="flex justify-between">
                <span className="text-gold-300/70">Personality:</span>
                <span className="text-gold-200 text-right">{fighter.personality.slice(0, 30)}...</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gold-300/70">Record:</span>
                <span className="text-gold-200">
                  {fighter.wins}W - {fighter.losses}L - {fighter.draws}D
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gold-300/70">Win Rate:</span>
                <span className="text-gold-400 font-bold">
                  {((fighter.wins / (fighter.wins + fighter.losses + fighter.draws || 1)) * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            <div className="grid grid-cols-4 gap-2 mb-4">
              {[
                { label: 'PWR', value: fighter.power },
                { label: 'TEC', value: fighter.technique },
                { label: 'HP', value: fighter.max_health },
                { label: 'ST', value: fighter.max_stamina },
              ].map((stat, j) => (
                <div key={j} className="text-center p-2 bg-stone-900/30 rounded">
                  <div className="text-lg font-bold text-gold-400">{stat.value}</div>
                  <div className="text-xs text-gold-300/50">{stat.label}</div>
                </div>
              ))}
            </div>

            <div className="flex gap-2">
              <Link to={`/fighter/${fighter.fighter_id}`} className="flex-1">
                <button className="w-full py-2 glass border border-gold-600 text-gold-400 rounded hover:bg-gold-600/20 flex items-center justify-center space-x-1">
                  <Eye size={16} />
                  <span className="text-sm">View</span>
                </button>
              </Link>
              <button
                onClick={() => handleTrain(fighter.fighter_id, fighter.name)}
                className="flex-1 py-2 glass border border-gold-600 text-gold-400 rounded hover:bg-gold-600/20 flex items-center justify-center space-x-1"
              >
                <Dumbbell size={16} />
                <span className="text-sm">Train</span>
              </button>
              <button
                onClick={() => handleDelete(fighter.fighter_id, fighter.name)}
                className="py-2 px-3 glass border border-red-600 text-red-400 rounded hover:bg-red-600/20"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
