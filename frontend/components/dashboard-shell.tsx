'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'
import { BookOpen, ChevronDown, FilePlus2, FileText, LayoutDashboard, Library, Menu, Moon, Settings, Sparkles, Sun, UserRound, X } from 'lucide-react'
import { cn } from '@/lib/utils'

const nav = [
  { href: '/dashboard', label: 'Overview', icon: LayoutDashboard },
  { href: '/dashboard/cvs', label: 'My CVs', icon: FileText },
  { href: '/dashboard/create-cv', label: 'Create CV', icon: FilePlus2 },
  { href: '/dashboard/designs', label: 'Design library', icon: Library },
  { href: '/dashboard/ats', label: 'ATS analysis', icon: Sparkles },
]

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [dark, setDark] = useState(false)
  const current = nav.find((item) => pathname === item.href)?.label ?? (pathname.includes('profile') ? 'Profile' : pathname.includes('settings') ? 'Settings' : 'Overview')
  const sidebar = <aside className={cn('dashboard-sidebar', mobileOpen && 'is-open')}>
    <div className="sidebar-brand"><span className="brand-mark"><Sparkles size={16} /></span><span>HireMe<span className="brand-accent">AI</span></span><button className="icon-button mobile-close" onClick={() => setMobileOpen(false)} aria-label="Close navigation"><X size={18} /></button></div>
    <div className="workspace-switcher"><span className="workspace-avatar">JD</span><span className="workspace-name">Jordan&apos;s workspace</span><ChevronDown size={14} /></div>
    <nav className="sidebar-nav" aria-label="Dashboard navigation">
      <p className="nav-label">Workspace</p>
      {nav.map((item) => <Link key={item.href} href={item.href} onClick={() => setMobileOpen(false)} className={cn('nav-item', pathname === item.href && 'active')}><item.icon size={17} /><span>{item.label}</span>{item.label === 'Create CV' && <span className="nav-plus">+</span>}</Link>)}
      <p className="nav-label nav-label-spaced">Account</p>
      <Link href="/dashboard/profile" className={cn('nav-item', pathname.includes('profile') && 'active')}><UserRound size={17} /><span>Profile</span></Link>
      <Link href="/dashboard/settings" className={cn('nav-item', pathname.includes('settings') && 'active')}><Settings size={17} /><span>Settings</span></Link>
    </nav>
    <div className="sidebar-bottom"><div className="help-card"><BookOpen size={16} /><div><strong>Need a hand?</strong><span>Read the quick guide</span></div></div><div className="sidebar-user"><span className="avatar">JD</span><div><strong>Jordan Davis</strong><span>jordan@example.com</span></div><ChevronDown size={14} /></div></div>
  </aside>
  return <div className={cn('app-frame', dark && 'dark-mode')}><div className="mobile-backdrop" onClick={() => setMobileOpen(false)} />{sidebar}<main className="dashboard-main"><header className="dashboard-header"><button className="icon-button mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open navigation"><Menu size={20} /></button><div><p className="eyebrow">Workspace / {current}</p><h1>{current}</h1></div><div className="header-actions"><button className="theme-button" onClick={() => setDark(!dark)} aria-label="Toggle theme">{dark ? <Sun size={17} /> : <Moon size={17} />}</button><Link href="/dashboard/create-cv" className="primary-button"><FilePlus2 size={16} /> Create CV</Link></div></header><div className="dashboard-content">{children}</div></main></div>
}
