import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { User, ArrowLeft, Scroll } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function FighterDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [fighter, setFighter] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFighter()
  }, [id])

  const loadFighter = async () => {
    try {
      const response = await axios.get(`/api/fighters/${id}`)
      setFighter(response.data)
    } catch (error) {
      toast.error('Fighter not found')
      navigate('/roster')
    } finally {
      setLoading(false)
    }
  }

  if (loading || !fighter) {
    return (
      <div className="text-center py-20">
        <User size={60} className="text-gold-500 mx-auto animate-pulse" />
        <p className="text-gold-300 mt-4">Loading warrior...</p>
      </div>
    )
  }

  const winRate = ((fighter.wins / (fighter.wins + fighter.losses + fighter.draws || 1)) * 100).toFixed(1)

  return (
    <div className="max-w-4xl mx-auto">
      <button
        onClick={() => navigate('/roster')}
        className="flex items-center space-x-2 text-gold-400 hover:text-gold-300 mb-8"
      >
        <ArrowLeft size={20} />
        <span>Back to Roster</span>
      </button>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass p-8 rounded-lg bronze-border"
      >
        <div className="text-center mb-8">
          <User size={100} className="mx-auto text-gold-500 mb-4" />
          <h1 className="text-5xl font-bold text-gold-400 mb-2 font-trajan">
            {fighter.name}
          </h1>
          <div className="text-xl text-gold-300/70">Level {fighter.level} Gladiator</div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-8">
          <div>
            <h3 className="text-gold-400 font-bold mb-3 flex items-center text-lg">
              <Scroll className="mr-2" />
              Backstory
            </h3>
            <p className="text-gold-200/80 italic">{fighter.backstory}</p>
          </div>

          <div>
            <h3 className="text-gold-400 font-bold mb-3 text-lg">Personality</h3>
            <p className="text-gold-200/80">{fighter.personality}</p>
          </div>
        </div>

        <div className="mb-8 p-6 bg-stone-900/30 rounded-lg">
          <h3 className="text-gold-400 font-bold mb-3 text-lg">✨ Special Trait</h3>
          <p className="text-gold-200/80">{fighter.special_trait}</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Power', value: fighter.power, max: 100 },
            { label: 'Technique', value: fighter.technique, max: 100 },
            { label: 'Health', value: fighter.max_health, max: 150 },
            { label: 'Stamina', value: fighter.max_stamina, max: 150 },
          ].map((stat, i) => (
            <div key={i} className="text-center p-4 bg-stone-900/30 rounded-lg">
              <div className="text-3xl font-bold text-gold-400">{stat.value}</div>
              <div className="text-sm text-gold-300/70 mb-2">{stat.label}</div>
              <div className="w-full bg-stone-700 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-gold-600 to-gold-400 h-2 rounded-full"
                  style={{ width: `${(stat.value / stat.max) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="text-center p-4 bg-stone-900/30 rounded-lg">
            <div className="text-2xl font-bold text-gold-400">
              {(fighter.aggression_level * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gold-300/70">Aggression</div>
          </div>
          <div className="text-center p-4 bg-stone-900/30 rounded-lg">
            <div className="text-2xl font-bold text-gold-400">
              {(fighter.defense_bias * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gold-300/70">Defense</div>
          </div>
          <div className="text-center p-4 bg-stone-900/30 rounded-lg">
            <div className="text-2xl font-bold text-gold-400 capitalize">
              {fighter.reaction_speed}
            </div>
            <div className="text-sm text-gold-300/70">Speed</div>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="text-gold-400 font-bold mb-3 text-lg">⚔️ Preferred Moves</h3>
          <div className="flex flex-wrap gap-3">
            {fighter.preferred_moves.map((move, i) => (
              <span
                key={i}
                className="px-4 py-2 bg-gold-600/20 text-gold-300 rounded-lg border border-gold-600/40 font-semibold"
              >
                {move.replace('_', ' ').toUpperCase()}
              </span>
            ))}
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center p-6 glass rounded-lg border border-gold-600/30">
            <div className="text-4xl font-bold text-green-400">{fighter.wins}</div>
            <div className="text-gold-300/70">Victories</div>
          </div>
          <div className="text-center p-6 glass rounded-lg border border-gold-600/30">
            <div className="text-4xl font-bold text-red-400">{fighter.losses}</div>
            <div className="text-gold-300/70">Defeats</div>
          </div>
          <div className="text-center p-6 glass rounded-lg border border-gold-600/30">
            <div className="text-4xl font-bold text-gold-400">{winRate}%</div>
            <div className="text-gold-300/70">Win Rate</div>
          </div>
        </div>

        <div className="mt-8 p-6 bg-stone-900/30 rounded-lg">
          <div className="text-gold-300/70 text-sm mb-2">Experience Progress</div>
          <div className="w-full bg-stone-700 rounded-full h-4">
            <div
              className="bg-gradient-to-r from-gold-600 to-gold-400 h-4 rounded-full flex items-center justify-center text-xs text-stone-900 font-bold"
              style={{ width: `${(fighter.experience / (fighter.level * 100)) * 100}%` }}
            >
              {fighter.experience}/{fighter.level * 100}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
