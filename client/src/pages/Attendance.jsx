import { useState, useEffect, useRef } from 'react';
import api from '../api';

export default function Attendance() {
  const [value, setValue] = useState('');
  const [status, setStatus] = useState(null);
  const [records, setRecords] = useState([]);
  const inputRef = useRef();

  useEffect(() => { loadToday(); inputRef.current?.focus(); }, []);

  async function loadToday() {
    const { data } = await api.get('/attendance/today');
    setRecords(data);
  }

  async function handleRegister(e) {
    e.preventDefault();
    if (!value.trim()) return;
    try {
      const { data } = await api.post('/attendance', { value: value.trim() });
      if (data.tipo === 'completo') {
        setStatus({ type: 'gray', msg: `${data.alumno}: entrada y salida ya registradas hoy.` });
      } else {
        const label = data.tipo === 'entrada' ? 'Entrada' : 'Salida';
        const color = data.tipo === 'entrada' ? 'green' : 'yellow';
        setStatus({ type: color, msg: `${label}: ${data.alumno} — ${data.hora}` });
        loadToday();
      }
    } catch (err) {
      setStatus({ type: 'red', msg: err.response?.data?.error ?? 'Error al registrar.' });
    }
    setValue('');
    inputRef.current?.focus();
  }

  const statusColor = {
    green: 'text-green-400', yellow: 'text-yellow-400',
    red: 'text-red-400', gray: 'text-gray-400',
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">Registro de Asistencia</h2>

      <form onSubmit={handleRegister} className="flex items-center gap-3 bg-gray-900 p-4 rounded-xl mb-6">
        <span className="text-sm text-gray-300 whitespace-nowrap">ID o UID RFID del alumno:</span>
        <input
          ref={inputRef}
          value={value}
          onChange={e => setValue(e.target.value)}
          placeholder="Ej: 3 o UID de tarjeta"
          className="bg-gray-800 text-white rounded-lg px-4 py-2 text-sm w-52 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors"
        >
          Registrar
        </button>
        {status && <span className={`text-sm font-medium ${statusColor[status.type]}`}>{status.msg}</span>}
      </form>

      <div className="bg-gray-900 rounded-xl overflow-hidden">
        <div className="grid grid-cols-4 bg-gray-800 px-4 py-2.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">
          <span>Alumno</span><span>Grupo</span><span>Entrada</span><span>Salida</span>
        </div>
        {records.length === 0 ? (
          <p className="text-center text-gray-500 py-8 text-sm">Sin registros hoy.</p>
        ) : (
          records.map((r, i) => (
            <div key={i} className="grid grid-cols-4 px-4 py-3 border-t border-gray-800 text-sm hover:bg-gray-800/50">
              <span>{r.alumno}</span><span>{r.grupo}</span>
              <span className="text-green-400">{r.fecha_entrada}</span>
              <span className={r.fecha_salida === '—' ? 'text-gray-500' : 'text-yellow-400'}>{r.fecha_salida}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
