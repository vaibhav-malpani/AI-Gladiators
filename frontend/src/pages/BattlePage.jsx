import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Swords, Users } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'

export default function BattlePage() {
  const [fighters, setFighters] = useState([])
  const [fighter1, setFighter1] = useState(null)
  const [fighter2, setFighter2] = useState(null)
  const [battling, setBattling] = useState(false)
  const [battleResult, setBattleResult] = useState(null)
  const [currentRound, setCurrentRound] = useState(0)

  useEffect(() => {
    loadFighters()
  }, [])

  const loadFighters = async () => {
    try {
      const response = await axios.get('/api/fighters')
      setFighters(response.data)
    } catch (error) {
      toast.error('Failed to load fighters')
    }
  }

  const startBattle = async () => {
    if (!fighter1 || !fighter2) {
      toast.error('Select two fighters!')
      return
    }

    if (fighter1.fighter_id === fighter2.fighter_id) {
      toast.error('A fighter cannot battle themselves!')
      return
    }

    setBattling(true)
    setBattleResult(null)
    setCurrentRound(0)

    try {
      const response = await axios.post('/api/battle', {
        fighter1_id: fighter1.fighter_id,
        fighter2_id: fighter2.fighter_id
      })

      // Animate through rounds
      for (let i = 0; i < response.data.battle_log.length; i++) {
        setCurrentRound(i + 1)
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      setBattleResult(response.data)
      toast.success(`Victory to ${response.data.winner_name || 'none'}!`)
      loadFighters()
    } catch (error) {
      toast.error('Battle failed: ' + (error.response?.data?.detail || error.message))
    } finally {
      setBattling(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold text-gold-400 mb-4 text-embossed font-trajan">
          ⚔️ BATTLE ARENA ⚔️
        </h1>
        <p className="text-xl text-gold-200">Select your champions and watch them fight!</p>
      </motion.div>

      {!battleResult ? (
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {[
            { selected: fighter1, setter: setFighter1, label: 'Fighter 1' },
            { selected: fighter2, setter: setFighter2, label: 'Fighter 2' }
          ].map((slot, i) => (
            <div key={i} className="glass p-6 rounded-lg bronze-border">
              <h3 className="text-2xl font-bold text-gold-400 mb-4 text-center">
                {slot.label}
              </h3>

              {slot.selected ? (
                <div className="text-center">
                  <Users size={60} className="mx-auto text-gold-500 mb-4" />
                  <h4 className="text-xl font-bold text-gold-300 mb-2">{slot.selected.name}</h4>
                  <div className="text-sm text-gold-200/70 mb-4">
                    Level {slot.selected.level} • {slot.selected.wins}W/{slot.selected.losses}L
                  </div>
                  <button
                    onClick={() => slot.setter(null)}
                    className="px-4 py-2 glass border border-gold-600 text-gold-400 rounded"
                  >
                    Change Fighter
                  </button>
                </div>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {fighters.map(f => (
                    <button
                      key={f.fighter_id}
                      onClick={() => slot.setter(f)}
                      disabled={battling}
                      className="w-full p-3 glass border border-gold-600/30 rounded hover:border-gold-600 hover:bg-gold-600/20 text-left disabled:opacity-50"
                    >
                      <div className="font-bold text-gold-300">{f.name}</div>
                      <div className="text-xs text-gold-200/70">
                        Lvl {f.level} • {f.wins}W/{f.losses}L • {f.personality.slice(0, 40)}...
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="glass p-8 rounded-lg bronze-border mb-8"
        >
          <div className="text-center mb-8">
            <h2 className="text-4xl font-bold text-gold-400 mb-4 font-trajan">
              🏆 {battleResult.winner_name || 'DRAW'} 🏆
            </h2>
            <div className="text-gold-200">
              Battle lasted {battleResult.battle_log.length} rounds
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-8">
            {[
              { name: fighter1.name, stats: battleResult.fighter1_stats },
              { name: fighter2.name, stats: battleResult.fighter2_stats }
            ].map((f, i) => (
              <div key={i} className="text-center p-6 bg-stone-900/30 rounded-lg">
                <h3 className="text-2xl font-bold text-gold-400 mb-4">{f.name}</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gold-300/70">Final Health:</span>
                    <span className="text-gold-200">{f.stats.health}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gold-300/70">New Record:</span>
                    <span className="text-gold-200">{f.stats.wins}W - {f.stats.losses}L</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gold-300/70">Level:</span>
                    <span className="text-gold-200">{f.stats.level}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-stone-900/30 p-6 rounded-lg mb-6">
            <div className="text-gold-200/80 prose prose-invert prose-gold max-w-none">
              <ReactMarkdown
                components={{
                  h1: ({node, ...props}) => <h1 className="text-3xl font-bold text-gold-300 mb-4 mt-6" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-2xl font-bold text-gold-400 mb-3 mt-5" {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-xl font-semibold text-gold-500 mb-2 mt-4" {...props} />,
                  h4: ({node, ...props}) => <h4 className="text-lg font-semibold text-gold-500 mb-2 mt-3" {...props} />,
                  p: ({node, ...props}) => <p className="text-gold-200/90 mb-3 leading-relaxed" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc list-inside text-gold-200/90 mb-3 space-y-1" {...props} />,
                  ol: ({node, ...props}) => <ol className="list-decimal list-inside text-gold-200/90 mb-3 space-y-1" {...props} />,
                  li: ({node, ...props}) => <li className="text-gold-200/90 ml-4" {...props} />,
                  strong: ({node, ...props}) => <strong className="font-bold text-gold-300" {...props} />,
                  em: ({node, ...props}) => <em className="italic text-gold-300/90" {...props} />,
                  blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-gold-500 pl-4 italic text-gold-300/80 my-3" {...props} />,
                  code: ({node, inline, ...props}) => 
                    inline 
                      ? <code className="bg-stone-800 text-gold-400 px-1.5 py-0.5 rounded text-sm" {...props} />
                      : <code className="block bg-stone-800 text-gold-400 p-3 rounded my-3 overflow-x-auto" {...props} />,
                  hr: ({node, ...props}) => <hr className="border-gold-600/30 my-4" {...props} />,
                }}
              >
                {battleResult.commentary}
              </ReactMarkdown>
            </div>
          </div>

          <button
            onClick={() => {
              setBattleResult(null)
              setFighter1(null)
              setFighter2(null)
            }}
            className="w-full py-4 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-lg rounded-lg glow-gold"
          >
            ⚔️ NEW BATTLE
          </button>
        </motion.div>
      )}

      {!battleResult && (
        <div className="text-center">
          <button
            onClick={startBattle}
            disabled={!fighter1 || !fighter2 || battling}
            className="px-12 py-5 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-xl rounded-lg glow-gold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-3 mx-auto"
          >
            {battling ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity }}
                >
                  <Swords />
                </motion.div>
                <span>
                  {currentRound === 0 ? '⚔️ Preparing Battle...' : `⚔️ Round ${currentRound}...`}
                </span>
              </>
            ) : (
              <>
                <Swords />
                <span>⚔️ BEGIN BATTLE</span>
              </>
            )}
          </button>
        </div>
      )}
    </div>
  )
}
