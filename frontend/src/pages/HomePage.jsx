import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Swords, Zap, Users, Trophy, Shield, Target } from 'lucide-react'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function HomePage() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    axios.get('/api/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error(err))
  }, [])

  const features = [
    {
      icon: Zap,
      title: 'AI-Powered Creation',
      description: 'Describe your warrior in natural language and watch AI bring them to life'
    },
    {
      icon: Swords,
      title: 'Autonomous Combat',
      description: 'Fighters make their own decisions based on personality and strategy'
    },
    {
      icon: Shield,
      title: 'Unique Personalities',
      description: 'Each fighter has distinct traits, moves, and special abilities'
    },
    {
      icon: Target,
      title: 'Strategic Training',
      description: 'Train your warriors and watch them evolve through experience'
    },
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center py-12 relative"
      >
        <div className="absolute inset-0 flex items-center justify-center opacity-10">
          <Swords size={400} className="text-gold-500" />
        </div>

        <motion.h1 
          className="text-7xl md:text-8xl font-bold text-embossed text-gold-400 mb-6 font-trajan relative z-10"
          animate={{ 
            textShadow: [
              '0 0 20px rgba(217, 119, 6, 0.5)',
              '0 0 40px rgba(217, 119, 6, 0.8)',
              '0 0 20px rgba(217, 119, 6, 0.5)',
            ]
          }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          ENTER THE ARENA
        </motion.h1>

        <p className="text-2xl text-gold-200 mb-8 max-w-3xl mx-auto">
          Where AI Warriors Fight for Glory and Honor
        </p>

        <p className="text-lg text-gold-300/80 mb-12 max-w-2xl mx-auto italic">
          "Design your champion, forge their destiny, and watch as they battle autonomously 
          in the greatest spectacle of artificial intelligence"
        </p>

        <div className="flex flex-wrap gap-4 justify-center">
          <Link to="/create">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-lg rounded-lg glow-gold bronze-border"
            >
              ⚔️ CREATE YOUR WARRIOR
            </motion.button>
          </Link>

          <Link to="/battle">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 glass text-gold-400 font-bold text-lg rounded-lg border-2 border-gold-600 hover:bg-gold-600/20"
            >
              🏛️ ENTER ARENA
            </motion.button>
          </Link>
        </div>
      </motion.section>

      {/* Stats Section */}
      {stats && (
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {[
            { label: 'Gladiators', value: stats.total_fighters, icon: Users },
            { label: 'Battles', value: stats.total_battles, icon: Swords },
            { label: 'Max Level', value: stats.highest_level, icon: Trophy },
            { label: 'Top Win Rate', value: `${stats.best_win_rate}%`, icon: Target },
          ].map((stat, i) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={i}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.5 + i * 0.1 }}
                className="glass p-6 rounded-lg text-center bronze-border"
              >
                <Icon className="mx-auto mb-2 text-gold-500" size={32} />
                <div className="text-3xl font-bold text-gold-400">{stat.value}</div>
                <div className="text-sm text-gold-300/70 uppercase tracking-wider">{stat.label}</div>
              </motion.div>
            )
          })}
        </motion.section>
      )}

      {/* Features Section */}
      <section className="py-12">
        <h2 className="text-4xl font-bold text-center text-gold-400 mb-12 text-embossed font-trajan">
          THE PATH TO GLORY
        </h2>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, i) => {
            const Icon = feature.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: i % 2 === 0 ? -50 : 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8 + i * 0.2 }}
                className="glass p-6 rounded-lg bronze-border hover:scale-105 transition-transform duration-300"
              >
                <div className="flex items-start space-x-4">
                  <div className="bg-gold-600/20 p-3 rounded-lg">
                    <Icon className="text-gold-500" size={32} />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gold-400 mb-2">{feature.title}</h3>
                    <p className="text-gold-200/80">{feature.description}</p>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="text-center py-16 glass rounded-lg bronze-border"
      >
        <h2 className="text-4xl font-bold text-gold-400 mb-4 font-trajan">
          YOUR LEGEND AWAITS
        </h2>
        <p className="text-xl text-gold-200 mb-8 max-w-2xl mx-auto">
          Will you forge a champion who fights with honor? Or a ruthless warrior who knows no mercy?
        </p>
        <Link to="/create">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="px-12 py-5 bg-gradient-to-r from-gold-600 to-gold-500 text-stone-900 font-bold text-xl rounded-lg glow-gold"
          >
            🛡️ BEGIN YOUR JOURNEY
          </motion.button>
        </Link>
      </motion.section>
    </div>
  )
}
