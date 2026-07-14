export default function LandingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen" style={{ background: '#0f172a', color: '#f8fafc' }}>
      {children}
    </div>
  )
}
