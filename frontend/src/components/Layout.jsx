import { Link, useLocation } from 'react-router-dom'
import { Swords, Users, Trophy, Plus, Home } from 'lucide-react'
import { motion } from 'framer-motion'

export default function Layout({ children }) {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/create', icon: Plus, label: 'Create' },
    { path: '/roster', icon: Users, label: 'Roster' },
    { path: '/battle', icon: Swords, label: 'Battle' },
    { path: '/rankings', icon: Trophy, label: 'Rankings' },
  ]

  return (
    <div className="min-h-screen relative">
      {/* Animated background particles */}
      <div className="particles fixed inset-0 z-0">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-gold-500 rounded-full opacity-20"
            initial={{ 
              x: Math.random() * window.innerWidth, 
              y: Math.random() * window.innerHeight 
            }}
            animate={{ 
              y: [null, Math.random() * window.innerHeight],
              opacity: [0.1, 0.3, 0.1]
            }}
            transition={{ 
              duration: 10 + Math.random() * 10, 
              repeat: Infinity,
              ease: "linear"
            }}
          />
        ))}
      </div>

      {/* Header */}
      <header className="relative z-10 glass border-b border-gold-600/30">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-3 group">
              <motion.div
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
                className="text-gold-500"
              >
                <Swords size={36} />
              </motion.div>
              <div>
                <h1 className="text-3xl font-bold text-embossed text-gold-400 font-trajan">
                  AI GLADIATORS
                </h1>
                <p className="text-xs text-gold-300/70 tracking-widest">
                  WHERE WARRIORS FIGHT AUTONOMOUSLY
                </p>
              </div>
            </Link>

            <nav className="flex space-x-2">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                      isActive
                        ? 'bg-gold-600 text-stone-900 glow-gold'
                        : 'text-gold-300 hover:bg-gold-600/20 hover:text-gold-400'
                    }`}
                  >
                    <Icon size={20} />
                    <span className="font-semibold hidden md:inline">{item.label}</span>
                  </Link>
                )
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="relative z-10 container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="relative z-10 glass border-t border-gold-600/30 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-gold-300/60 text-sm">
            <p className="font-cinzel">
              ⚔️ Made with <span className="text-red-500">♥</span> in the Arena of AI ⚔️
            </p>
            <p className="text-xs mt-2 text-gold-300/40">
              "In the arena of AI, every fighter has a story, and every battle teaches a lesson."
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
