import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sparkles, User, Scroll } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function CreateFighterPage() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [preview, setPreview] = useState(null)
  const navigate = useNavigate()

  const examples = [
    "A patient warrior who waits for the perfect moment, then strikes with devastating precision",
    "An aggressive berserker who grows stronger as the battle intensifies",
    "A calculating robot that analyzes opponent patterns and adapts in real-time",
    "A defensive master inspired by ancient kung fu, using the opponent's energy against them",
    "A lightning-fast striker who overwhelms enemies with relentless combinations",
  ]

  const handleGenerate = async () => {
    if (prompt.length < 10) {
      toast.error('Please provide a more detailed description (at least 10 characters)')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/fighters', { prompt })
      setPreview(response.data)
      toast.success('🎉 Warrior forged successfully!')
    } catch (error) {
      toast.error('Failed to create fighter: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const handleConfirm = () => {
    if (preview) {
      toast.success(`⚔️ ${preview.name} has entered the arena!`)
      navigate('/roster')
    }
  }

  const handleCancel = () => {
    setPreview(null)
    setPrompt('')
  }

  return (
    <div className="max-w-5xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold text-gold-400 mb-4 text-embossed font-trajan">
          FORGE YOUR CHAMPION
        </h1>
        <p className="text-xl text-gold-200">
          Describe your warrior, and the AI will bring them to life
        </p>
      </motion.div>

      {!preview ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="glass p-8 rounded-lg bronze-border"
        >
          <div className="mb-6">
            <label className="flex items-center text-gold-300 text-lg mb-3">
              <Scroll className="mr-2" />
              Describe Your Warrior
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="A patient fighter who waits for the perfect moment to strike..."
              className="w-full h-40 bg-stone-900/50 border-2 border-gold-600/30 rounded-lg p-4 text-gold-100 placeholder-gold-300/40 focus:border-gold-500 focus:outline-none resize-none"
              disabled={loading}
            />
            <div className="text-sm text-gold-300/60 mt-2">
              {prompt.length} characters (minimum 10)
            </div>
          </div>

          <div className="mb-6">
            <div className="text-gold-300 mb-3">💡 Need inspiration? Try these:</div>
            <div className="grid gap-2">
              {examples.map((example, i) => (
                <button
                  key={i}
                  onClick={() => setPrompt(example)}
                  className="text-left p-3 bg-stone-900/30 hover:bg-gold-600/20 border border-gold-600/20 rounded text-gold-200 text-sm transition-all"
                >
                  "{example}"
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || prompt.length < 10}
            className="w-full py-4 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-lg rounded-lg glow-gold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                >
                  <Sparkles />
                </motion.div>
                <span>Forging Warrior...</span>
              </>
            ) : (
              <>
                <Sparkles />
                <span>⚔️ FORGE WARRIOR</span>
              </>
            )}
          </button>
        </motion.div>
      ) : (
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="glass p-8 rounded-lg bronze-border"
        >
          <div className="text-center mb-8">
            <User size={80} className="mx-auto text-gold-500 mb-4" />
            <h2 className="text-4xl font-bold text-gold-400 mb-2 font-trajan">
              {preview.name}
            </h2>
            <div className="text-sm text-gold-300/70 mb-4">Level {preview.level} Gladiator</div>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div>
              <h3 className="text-gold-400 font-bold mb-2 flex items-center">
                <Scroll className="mr-2" size={20} />
                Backstory
              </h3>
              <p className="text-gold-200/80 text-sm italic">{preview.backstory}</p>
            </div>

            <div>
              <h3 className="text-gold-400 font-bold mb-2">Personality</h3>
              <p className="text-gold-200/80 text-sm">{preview.personality}</p>
            </div>

            <div>
              <h3 className="text-gold-400 font-bold mb-2">Special Trait</h3>
              <p className="text-gold-200/80 text-sm">✨ {preview.special_trait}</p>
            </div>

            <div>
              <h3 className="text-gold-400 font-bold mb-2">Preferred Moves</h3>
              <div className="flex flex-wrap gap-2">
                {preview.preferred_moves.map((move, i) => (
                  <span key={i} className="px-3 py-1 bg-gold-600/20 text-gold-300 rounded-full text-xs">
                    {move.replace('_', ' ')}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              { label: 'Power', value: preview.power },
              { label: 'Technique', value: preview.technique },
              { label: 'Health', value: preview.max_health },
              { label: 'Stamina', value: preview.max_stamina },
            ].map((stat, i) => (
              <div key={i} className="text-center p-4 bg-stone-900/30 rounded-lg">
                <div className="text-2xl font-bold text-gold-400">{stat.value}</div>
                <div className="text-sm text-gold-300/70">{stat.label}</div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="text-center p-4 bg-stone-900/30 rounded-lg">
              <div className="text-lg font-bold text-gold-400">{(preview.aggression_level * 100).toFixed(0)}%</div>
              <div className="text-xs text-gold-300/70">Aggression</div>
            </div>
            <div className="text-center p-4 bg-stone-900/30 rounded-lg">
              <div className="text-lg font-bold text-gold-400">{(preview.defense_bias * 100).toFixed(0)}%</div>
              <div className="text-xs text-gold-300/70">Defense</div>
            </div>
            <div className="text-center p-4 bg-stone-900/30 rounded-lg">
              <div className="text-lg font-bold text-gold-400 capitalize">{preview.reaction_speed}</div>
              <div className="text-xs text-gold-300/70">Speed</div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleConfirm}
              className="flex-1 py-4 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-lg rounded-lg glow-gold"
            >
              ✅ ACCEPT WARRIOR
            </button>
            <button
              onClick={handleCancel}
              className="flex-1 py-4 glass text-gold-400 font-bold text-lg rounded-lg border-2 border-gold-600"
            >
              ❌ FORGE AGAIN
            </button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
