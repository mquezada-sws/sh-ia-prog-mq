import { Button } from "@/components/ui/button"
import { ChevronDown, Monitor, FolderOpen, Users, Shield } from "lucide-react"
import Image from "next/image"

export default function Component() {
  return (
    <div className="min-h-screen bg-white">
      {/* Promotional Header */}
      <div className="bg-gray-900 text-white px-4 py-2 text-center text-sm">
        <span className="inline-flex items-center gap-2">
          ⚡ <strong>NUEVA FECHA DATA ENGINEERING</strong> ⚡ Descuento especial <strong>25% OFF</strong> disponible
          hasta el 27/7 🔥 Código: <strong>EARLYBIRD</strong> 🔥
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex items-center justify-between px-6 py-4 border-b">
        <div className="flex items-center gap-8">
          {/* Henry Logo */}
          <div className="flex items-center gap-1">
            <div className="grid grid-cols-2 gap-1">
              <div className="w-3 h-3 bg-yellow-400"></div>
              <div className="w-3 h-3 bg-gray-900"></div>
              <div className="w-3 h-3 bg-gray-900"></div>
              <div className="w-3 h-3 bg-yellow-400"></div>
            </div>
            <span className="ml-2 text-xl font-bold tracking-wider">HENRY</span>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-6">
            <button className="flex items-center gap-1 text-gray-700 hover:text-gray-900">
              Para estudiantes
              <ChevronDown className="w-4 h-4" />
            </button>
            <button className="flex items-center gap-1 text-gray-700 hover:text-gray-900">
              Para empresas
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Auth Buttons */}
        <div className="flex items-center gap-4">
          <Button variant="ghost" className="text-gray-700">
            Ingresar
          </Button>
          <Button className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold">Aplicar</Button>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-6 py-16">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Comienza o acelera
                <br />
                tu carrera en
                <br />
                tecnología
              </h1>

              <p className="text-xl text-gray-700 leading-relaxed">
                Estudia Full Stack Development, Data,
                <br />
                Inteligencia Artificial o Ciberseguridad
              </p>
            </div>

            {/* Features */}
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Monitor className="w-5 h-5 text-purple-600" />
                </div>
                <span className="text-gray-700">Online, en vivo y flexible</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <FolderOpen className="w-5 h-5 text-purple-600" />
                </div>
                <span className="text-gray-700">Basado en proyectos</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Users className="w-5 h-5 text-purple-600" />
                </div>
                <span className="text-gray-700">Basado en cohortes</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Shield className="w-5 h-5 text-purple-600" />
                </div>
                <span className="text-gray-700">Inversión sin riesgo</span>
              </div>
            </div>

            <Button className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold text-lg px-8 py-3 h-auto">
              Aplicar
            </Button>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden">
              <Image
                src="/hero-image.png"
                alt="Estudiante sonriente trabajando en computadora con código"
                width={600}
                height={600}
                className="w-full h-auto object-cover"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="text-center py-16">
        <h2 className="text-3xl font-bold text-gray-900">Mucho más que un bootcamp</h2>
      </div>
    </div>
  )
}
