import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const NAV = [
  { to: '/attendance', label: 'Asistencia' },
  { to: '/students',   label: 'Alumnos' },
  { to: '/groups',     label: 'Grupos' },
  { to: '/tutors',     label: 'Tutores' },
  { to: '/messaging',  label: 'Mensajes' },
];

export default function Sidebar() {
  const { admin, logout } = useAuth();

  return (
    <aside className="w-52 min-h-screen bg-gray-900 flex flex-col">
      <div className="px-5 pt-6 pb-4">
        <h1 className="text-white text-xl font-bold">AccessFlow</h1>
        <p className="text-gray-400 text-sm mt-1">{admin?.nombre}</p>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {NAV.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `block px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-3 pb-5">
        <button
          onClick={logout}
          className="w-full px-4 py-2 rounded-md text-sm font-medium bg-red-700 hover:bg-red-800 text-white transition-colors"
        >
          Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
