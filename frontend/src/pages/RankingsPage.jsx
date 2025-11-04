import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Medal } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function RankingsPage() {
  const [rankings, setRankings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadRankings()
  }, [])

  const loadRankings = async () => {
    try {
      const response = await axios.get('/api/rankings')
      setRankings(response.data)
    } catch (error) {
      toast.error('Failed to load rankings')
    } finally {
      setLoading(false)
    }
  }

  const getMedalEmoji = (rank) => {
    if (rank === 0) return '🥇'
    if (rank === 1) return '🥈'
    if (rank === 2) return '🥉'
    return `${rank + 1}.`
  }

  if (loading) {
    return (
      <div className="text-center py-20">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity }}
        >
          <Trophy size={60} className="text-gold-500 mx-auto" />
        </motion.div>
        <p className="text-gold-300 mt-4">Loading rankings...</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <Trophy size={80} className="mx-auto text-gold-500 mb-4" />
        <h1 className="text-5xl font-bold text-gold-400 mb-4 text-embossed font-trajan">
          HALL OF CHAMPIONS
        </h1>
        <p className="text-xl text-gold-200">
          The greatest warriors of the arena
        </p>
      </motion.div>

      {rankings.length === 0 ? (
        <div className="text-center py-20 glass rounded-lg bronze-border">
          <Medal size={60} className="mx-auto text-gold-500/30 mb-4" />
          <p className="text-gold-300">No warriors have entered the arena yet</p>
        </div>
      ) : (
        <div className="space-y-4">
          {rankings.map((fighter, i) => {
            const winRate = ((fighter.wins / (fighter.wins + fighter.losses + fighter.draws || 1)) * 100).toFixed(1)
            const isTopThree = i < 3

            return (
              <motion.div
                key={fighter.fighter_id}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                className={`glass p-6 rounded-lg ${isTopThree ? 'bronze-border glow-gold' : 'border border-gold-600/20'}`}
              >
                <div className="flex items-center space-x-6">
                  <div className={`text-4xl font-bold ${isTopThree ? 'text-gold-400' : 'text-gold-300/70'} w-16 text-center`}>
                    {getMedalEmoji(i)}
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-2xl font-bold text-gold-400 font-trajan">
                        {fighter.name}
                      </h3>
                      <div className="text-sm text-gold-300/70">
                        Level {fighter.level}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <div className="text-gold-300/70">Record</div>
                        <div className="text-gold-200 font-bold">
                          {fighter.wins}W - {fighter.losses}L - {fighter.draws}D
                        </div>
                      </div>
                      <div>
                        <div className="text-gold-300/70">Win Rate</div>
                        <div className="text-gold-400 font-bold">{winRate}%</div>
                      </div>
                      <div>
                        <div className="text-gold-300/70">Power</div>
                        <div className="text-gold-200 font-bold">{fighter.power}</div>
                      </div>
                      <div>
                        <div className="text-gold-300/70">Technique</div>
                        <div className="text-gold-200 font-bold">{fighter.technique}</div>
                      </div>
                    </div>

                    <div className="mt-3 text-gold-200/70 text-sm italic">
                      {fighter.personality}
                    </div>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}
    </div>
  )
}
